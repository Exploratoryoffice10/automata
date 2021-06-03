import sys, json, numpy

class DFA:
    def __init__(self, states=list(), letters=list(), tmat=list() ,start=list(), final=list()):
        self.states = states
        self.letters = letters
        self.start = start
        self.final = final
        self.trans = tmat
        self.rms()

    def gts(self,in_st,let):    # get transition state
        x = [self.trans[i][2] for i in range(len(self.trans)) if ((self.trans[i][0] == in_st) and (self.trans[i][1] == let))]
        return x[0]

    def rms(self):  # remove unreachable states
        Rs = set()
        Rs.add(self.start[0])
        Rr = set()
        while True:
            M = set()
            pt = Rs - Rr    # additional states added
            for i in pt:
                for l in self.letters:
                    M.add(self.gts(i,l))
            Rr = Rs.copy()
            for i in M:
                Rs.add(i)
            if len(Rs) == len(Rr):  # all the new states add already belong to the set so no new sets are added
                break
        
        self.states = list(Rs)
        for i in self.trans:    # removing transition function for unreachable stares
            if i[0] not in Rs:
                self.trans.remove(i)
        for i in self.final:    # removing unreachable final states    
            if i not in Rs:
                self.final.remove(i)
        return
        
    def to_dict(self):
        return {
            'states': self.states,
            'letters': self.letters,
            'transition_matrix': self.trans,
            'start': self.start,
            'final': self.final,
        }



if __name__ == '__main__':
    input_fn = sys.argv[1]
    output_fn = sys.argv[2]
    with open(input_fn,'r') as f:
        data = json.load(f)
    dfa = DFA(data['states'],data['letters'],data['transition_function'],data['start_states'],data['final_states'])
    x = dfa.states
    n = len(x) 
    sm = dict()     # state mapper maps states to integers 
    for i in range(len(x)):
        sm[x[i]] = i
    tbl = numpy.zeros((n,n))     # table of size nxn 
    for i in range(1,n):
        for j in range(n):
            if i > j:
                if (((x[i] in dfa.final) and (x[j] not in dfa.final)) or ((x[j] in dfa.final) and (x[i] not in dfa.final))):
                    tbl[i][j] = 1
    
    chk = 1
    while chk!=0:   # if no update happens then chk will be zero
        chk = 0        
        for i in range(1,n):
            for j in range(n):
                if (i > j) and (tbl[i][j] == 0):
                    for k in dfa.letters:
                        aa = sm[dfa.gts(x[i],k)]
                        bb = sm[dfa.gts(x[j],k)]
                        aa1 = max(aa,bb)
                        bb1 = min(aa,bb)
                        if tbl[aa1][bb1] == 1:
                            chk = 1
                            tbl[i][j] = 1
                            break
    
    """
        print('tbl')
        for i in tbl:
            print(i)
        print()
    """

    um_set = list()
    for i in range(1,n):
        for j in range(n):
            if ((i > j) and (tbl[i][j] == 0)):
                # print(x[i],x[j])
                um_set.append((x[i],x[j])) 



    dc = dict()
    for i in x:
        dc[i] = 0
    ii = 1
    for i,j in um_set:
        if (dc[i]!=0) and (dc[j]==0):
            dc[j] = dc[i]
        elif (dc[j]!=0) and (dc[i]==0):
            dc[i] = dc[j]
        elif (dc[i]==0) and (dc[j]==0):
            dc[i] = ii
            dc[j] = ii
            ii += 1

    ik = max(dc.values())
    states_list = list()

    pk = dict()
    for i in range(1,ik+1):
        aaa = list()
        for ss in x:
            if dc[ss] == i:
                aaa.append(ss)  
        if len(aaa)>0:
            states_list.append(aaa) # all states with same i are merged and same i correspond to i-1th element of the states_list 
    for ss in x:
        if dc[ss] == 0:
            states_list.append([ss])

    trans_fn = list()
    for pstate in states_list:
        for l in data['letters']:
            bb1 = pstate[0]
            cc1 = dfa.gts(bb1,l)
            dd1 = dc[cc1]   
            if dd1 != 0:    # 
                # print(states_list[dd1-1],'tutu')
                trans_fn.append([pstate,l,states_list[dd1-1]])
            else:
                trans_fn.append([pstate,l,[cc1]])


    final_st = list()
    for i in states_list:
        for j in i:
            if j in dfa.final: 
                final_st.append(i)  # state i is a final state. so going to check next state
                break

    # print('final',final_st)
    st_idx = dfa.start[0] 
    for i in states_list:
        if st_idx in i:
            ist_idx = i        
            break
    
    
    ooo = dict()
    ooo['states'] = states_list
    ooo['letters'] = data['letters']
    ooo['transition_function'] = trans_fn
    ooo['start_states'] = [ist_idx]
    ooo['final_states'] = final_st

    with open(output_fn,'w') as f:  
        json.dump(ooo, f ,indent = 4)
