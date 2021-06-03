import json,sys

class DFA:
    def __init__(self, states=None, letters=None, tmat=None, start=None, final=None):
        self.states = states
        self.letters = letters
        self.start = start
        self.final = final
        self.trans = tmat
        

    def gts(self,in_s,out_s):    # get transition state
        x = [self.trans[i][1] for i in range(len(self.trans)) if ((self.trans[i][0] == in_s) and (self.trans[i][2] == out_s))]
        return x    






class DFA_TO_RGX:
    def __init__(self,dfa):
        self.dfa = dfa


    def add_st_fn_st(self):
        stas= ['Q_S','Q_F']
        for i in self.dfa.final:
            self.dfa.trans.append([i,'$',stas[1]])
        for i in self.dfa.start:
            self.dfa.trans.append([stas[0],'$',i])
        self.dfa.start = stas[0]
        self.dfa.final = [stas[1]]  
        self.ns = self.dfa.states.copy()

    

    def convert(self):
        rstr = ""
        n = len(self.ns)
        """
        for k in range(len(self.ns)):
            for  i in range(len(self.ns)):
                for j in range(len(self.ns)):
        """
        ripped_st = list()
        for k in range(len(self.ns)):
            for  i in range(len(self.ns)):
                for j in range(len(self.ns)):
                    ckck = (i not in ripped_st) and (j not in ripped_st) and (k not in ripped_st)
                    if (i!=j) and (j!=k) and  (k!=i) and ckck:
                        aa1 = self.dfa.gts(i,k)
                        aa2 = self.dfa.gts(k,k)
                        aa3 = self.dfa.gts(k,j)
                        aa4 = self.dfa.gts(i,j)
            
            ripped_st.append(k)




if __name__ == '__main__':
    # print('number of args passed:',len(sys.argv))
    input_fn = sys.argv[1]  # input file
    output_fn = sys.argv[2] # output file
    with open(input_fn,'r') as f:
        data = json.load(f)
    infa = DFA(data['states'],data['letters'],data['transition_function'],data['start_states'],data['final_states'])
    #converter = NFA_to_DFA(infa)
    #final_dfa = converter.convert()
    #ooo = final_dfa.to_dict()
    #with open(output_fn,'w') as f:  
    #    json.dump(ooo, f ,indent = 4)
