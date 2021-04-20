import json,sys

class DFA:
    def __init__(self, states=None, letters=None, tmat=None, start=None, final=None):
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

class NFA:
    def __init__(self, states=None, letters=None, tmat=None, start=None, final=None):
        self.states = states
        self.letters = letters
        self.start = start
        self.final = final
        self.trans = tmat
        self.table = self.make_table(self.trans)

    def make_table(self,arr):
        ft = dict()
        for ele in arr: 
            ft[tuple(ele[:2])] = set()
        for ele in arr:
            ft[tuple(ele[:2])].add(ele[2])    
        return ft    


class NFA_to_DFA:   # return dfa
    def __init__(self,cnfa):
        self.cnfa = cnfa    # nfa to be converted 
        self.pset = self.power_set(cnfa.states)

    def power_set(self,arr):
        ps=[[]]
        for i in arr:
            for sar in ps:
                ps = ps + [list(sar)+[i]]
        return ps 

    def convert(self):
        ord = dict()
        j = 0
        for i in self.cnfa.states:
            ord[i] = j
            j+=1
        dfa_table = list()
        ini_st = list()
        ini_st.append([self.cnfa.start]) 
        ltrs = self.cnfa.letters
        ps = self.pset
        cd = dict()
        for x in ps:
            cd[tuple(sorted(x))] = 0
        cd[tuple(self.cnfa.start)] = 1
        for states in self.pset:
            for inp in self.cnfa.letters:        
                temp = set()
                for state in states:
                    ppp = self.cnfa.table.get((state,inp),set())
                    for i in ppp:   
                        temp.add(i) # union
                temp = list(temp)
                t1 = [ord[i] for i in temp] 
                t1.sort()
                temp = [self.cnfa.states[i] for i in t1]
                dfa_table.append([states,inp,temp])
        fin_st = []
        for sst in self.pset:
            for st in sst:
                if st in self.cnfa.final:
                    fin_st.append(sst)
                    continue
        fdfa = DFA(ps,ltrs,dfa_table,ini_st,fin_st)
        return fdfa




if __name__ == '__main__':
    # print('number of args passed:',len(sys.argv))
    input_fn = sys.argv[1]
    output_fn = sys.argv[2]
    with open(input_fn,'r') as f:
        data = json.load(f)
    infa = NFA(data['states'],data['letters'],data['transition_function'],data['start_states'],data['final_states'])
    converter = NFA_to_DFA(infa)
    final_dfa = converter.convert()
    ooo = final_dfa.to_dict()
    with open(output_fn,'w') as f:  
        json.dump(ooo, f ,indent = 4)