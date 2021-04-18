import json,sys


class NFA:
    def __init__(self, states = list(), letters=list(), tmat=list(), start=list(), final=list()):
        self.states = states
        self.letters = letters
        self.start = start
        self.final = final
        self.trans = tmat
        
    def to_dict(self):
        return  {
            'states': self.states,
            'letters': self.letters,
            'transition_function': self.trans,
            'start': self.start,
            'final': self.final,
        }


class regexp_to_NFA:
    def __init__(self,inp):
        self.exp = inp    # regexp to be converted 
        self.state_counter = 0
        self.nfa_stack = list()  
        self.charecters = list()
        for i in range(26):
            self.charecters.append(chr(ord('a')+i))
        for i in range(26):
            self.charecters.append(chr(ord('A')+i))
        for i in range(10):
            self.charecters.append(str(i))
        self.operands = ['+','.','*','(']

    def itp_ord(self,inp):
        ord_dict = {
            '+' : 1,
            '.' : 2,
            '*' : 3,
            '(' : 0
        }
        return ord_dict.get(inp,0)

    def is_albt(self,inp):
        return inp in self.charecters

    def topostfix(self,st):
        fpexp = list()  # final string in postfix
        stk = list()    # stack
        for i in st:
            if i.isalnum(): # is a alphabet
                fpexp.append(i)
            elif i == '(':   # should be a operator
                stk.append(i)
            elif i == ')':
                while(len(stk)>0 and (stk[-1] != '(')):
                    fpexp.append(stk.pop())
                if ((len(stk) == 0) or (stk[-1] != '(')):
                    exit('wrong reg-exp')
                else:
                    stk.pop()   # removing '('. concluding parenthesis
            else:
                while((len(stk)>0) and (self.itp_ord(i) <= self.itp_ord(stk[-1]))):     # should find one with less precedence
                    fpexp.append(stk.pop())
                stk.append(i)

        while len(stk)!=0:
            fpexp.append(stk.pop())
        return fpexp

    def add_new_nfa(self,ip):
        nnf = NFA()
        nnf.states,nnf.final,nnf.trans,nnf.start=[],[],[],[]
        for i in range(2):
            nnf.states.append(str(i+self.state_counter))
        nnf.start.append(str(self.state_counter))
        nnf.final.append(str(self.state_counter+1))
        nnf.trans.append([str(self.state_counter), ip, str(self.state_counter+1)])
        # print(ip,'initial\n',nnf.to_dict())
        self.nfa_stack.append(nnf)
        self.state_counter += 2


    def do_union(self):
        nnf = NFA()
        nnf.states,nnf.final,nnf.trans,nnf.start=[],[],[],[]
        n1f = self.nfa_stack.pop()
        n2f = self.nfa_stack.pop()  # n2f union n1f
        nnf.states += (n1f.states + n2f.states)
        for i in range(1):
            nnf.states.append(str(i+self.state_counter))
        nnf.start.append(str(self.state_counter))
        nnf.trans += (n1f.trans + n2f.trans)
        nnf.final += (n1f.final + n2f.final)
        for i in n2f.start:
            nnf.trans.append([str(self.state_counter),'$',i])
        for i in n1f.start:
            nnf.trans.append([str(self.state_counter),'$',i])
        self.state_counter += 1
        self.nfa_stack.append(nnf)
        

    def do_concat(self):    # done
        nnf = NFA()
        nnf.states,nnf.final,nnf.trans,nnf.start=[],[],[],[]
        n1f = self.nfa_stack.pop()
        n2f = self.nfa_stack.pop()  # n2f.n1f
        nnf.states += (n2f.states + n1f.states)    # n2f
        nnf.trans += (n2f.trans+n1f.trans)
        for i in n2f.final:
            for j in n1f.start:
                nnf.trans.append([i,'$',j])
        nnf.start += n2f.start
        nnf.final += n1f.final
        self.nfa_stack.append(nnf)
        return

    def do_star(self):  # done
        nnf = NFA()
        nnf.states,nnf.final,nnf.trans,nnf.start=[],[],[],[]
        n1f = self.nfa_stack.pop()
        nnf.states += n1f.states
        for i in range(1):
            nnf.states.append(str(i+self.state_counter))
        nnf.start.append(str(self.state_counter))
        nnf.trans += (n1f.trans)
        nnf.final.append(str(self.state_counter))
        for i in n1f.final:
            for j in n1f.start:
                nnf.trans.append([i,'$',j]) # epsilon
        for i in n1f.start:
            nnf.trans.append([str(self.state_counter),'$',i])
        nnf.final += (n1f.final)
        self.nfa_stack.append(nnf)
        self.state_counter += 1       
        return


    def convert(self):
        rgexp = list()
        ltrs_nfa = set() # letters
        rgexp.append(self.exp[0])
        for i in range(1,len(self.exp)):
            a = self.exp[i-1]
            b = self.exp[i]
            if ((a.isalnum() and b.isalnum()) or (a.isalnum() and b=='(') or (a=='*' and b=='(') or ((a == ')' and b.isalnum())) or (a=='*' and b.isalnum())):   
                rgexp.append('.')
            rgexp.append(b)
        rgexp = self.topostfix(rgexp)   # converted to postfix
        #print(''.join(rgexp),'final')
        for i in rgexp:
            if i.isalnum():
                ltrs_nfa.add(i)
                self.add_new_nfa(i)
                # print(self.nfa_stack[-1].states,'for',i)
            elif i == '.': # concat
                self.do_concat()
            elif i == '+': # union
                self.do_union()
            elif i == '*': # star
                self.do_star()
            #print(i,'at end for\n',self.nfa_stack[-1].to_dict())
        final_nfa = self.nfa_stack.pop()
        # final_nfa.states = list(set(final_nfa.states))
        final_nfa.letters = list(ltrs_nfa)
        return final_nfa 

if __name__ == '__main__':
    input_fn = sys.argv[1]      # input file name
    output_fn = sys.argv[2]     # output file name
    with open(input_fn,'r') as f:
        data = json.load(f)
    rgx_exp = data['regex']
    converter = regexp_to_NFA(rgx_exp)
    fnfa = converter.convert()
    ooo = fnfa.to_dict()
    with open(output_fn,'w') as f:  
        json.dump(ooo, f ,indent = 4)