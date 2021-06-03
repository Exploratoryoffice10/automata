import json,sys

class DFA:
    def __init__(self, states=None, letters=None, tmat=None, start=None, final=None):
        self.states = states
        self.letters = letters
        self.start = start
        self.final = final
        self.trans = tmat
        self.state_mpr1 = dict()
        self.state_mpr2 = dict()
        self.new_s = '(QS)'
        self.new_f = '(QF)'
        self.fin_tr = list()
        self.ad_details()

    def gts(self,in_s,out_s):    # get transition state
        x = [self.trans[i][1] for i in range(len(self.trans)) if ((self.trans[i][0] == in_s) and (self.trans[i][2] == out_s))]
        return x    


    def ad_details(self):
        self.all_s = [self.new_s]+self.states+[self.new_f]
        for i in range(len(self.all_s)):
            self.state_mpr1[i] = self.all_s[i]
            self.state_mpr2[self.all_s[i]] = i
        for i in self.start:
            self.trans.append([self.new_s,'$',i])
        for i in self.final:
            self.trans.append([i,'$',self.new_f])
        self.n = len(self.states)+2
        self.fin_tr = [['' for i in range(self.n)] for j in range(self.n)]
        for i in self.all_s:
            for j in self.all_s:
                ind1 ,ind2 = self.state_mpr2[i],self.state_mpr2[j]
                pttp = self.gts(i,j)
                if len(pttp) > 1:
                    temp = ''
                    for tss in pttp:
                        temp += 'tss'
                    self.fin_tr[ind1][ind2] = tss
                elif len(pttp) == 1:
                    self.fin_tr[ind1][ind2] = pttp[0]               
        """
        for i in self.fin_tr:
            print(i)
        print('ddfdf')
        """


    def endgame(self):
        ssi = self.states+[self.new_s]
        ssj = self.states+[self.new_f]
        ripped_lst = list()
        for k in self.states:
            for i in ssi:
                for j in ssj:
                    ind1,ind2,ind3 = self.state_mpr2[i], self.state_mpr2[j],self.state_mpr2[k]
                    ckck = (i not in ripped_lst) and (j not in ripped_lst) and (ind1!=ind3) and  (ind3!=ind2)
                    if ckck:
                        aa1 = self.fin_tr[ind1][ind3]
                        aa2 = self.fin_tr[ind3][ind3]
                        aa3 = self.fin_tr[ind3][ind2]
                        aa4 = self.fin_tr[ind1][ind2]
                        if (len(aa1)!=0) and (len(aa3)!=0):
                            upt_with = ''
                            if  len(aa2) !=0:
                                if len(aa4)!=0: 
                                    upt_with = '('+self.fin_tr[ind1][ind3]+')('+self.fin_tr[ind3][ind3]+')*('+self.fin_tr[ind3][ind2] + ')+('+self.fin_tr[ind1][ind2]+')'
                                else:
                                    upt_with = '('+self.fin_tr[ind1][ind3]+')('+self.fin_tr[ind3][ind3]+')*('+self.fin_tr[ind3][ind2] + ')'
                            else:
                                if len(aa4)!=0: 
                                    upt_with = '('+self.fin_tr[ind1][ind3]+')('+self.fin_tr[ind3][ind2] + ')+('+self.fin_tr[ind1][ind2]+')'
                                else:
                                    upt_with = '('+self.fin_tr[ind1][ind3]+')('+self.fin_tr[ind3][ind2] + ')'
                            self.fin_tr[ind1][ind2] = upt_with
            ripped_lst.append(k)
        """
        print(self.fin_tr[0][self.n-1],'values')
        """
        return self.fin_tr[0][self.n-1]





if __name__ == '__main__':
    # print('number of args passed:',len(sys.argv))
    input_fn = sys.argv[1]  # input file
    output_fn = sys.argv[2] # output file
    with open(input_fn,'r') as f:
        data = json.load(f)
    cdfa = DFA(data['states'],data['letters'],data['transition_function'],data['start_states'],data['final_states'])
    fregex_exp = cdfa.endgame()
    ooo = dict()
    ooo['regex'] = fregex_exp
    with open(output_fn,'w') as f:  
        json.dump(ooo, f ,indent = 4)
    