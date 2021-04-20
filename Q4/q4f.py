import sys, json, numpy

class DFA:
    def __init__(self, states=list(), letters=list(), start=list(), final=list(), tmat=list()):
        self.states = states
        self.letters = letters
        self.start = start
        self.final = final
        self.trans = tmat

    def gts(self,in_st,let):    # get transition state
        x = [self.trans[i][2] for i in range(len(self.trans)) if ((self.trans[i][0] == in_st) and (self.trans[i][1] == let))]
        return x[0]


if __name__ == '__main__':
    input_fn = sys.argv[1]
    output_fn = sys.argv[2]
    with open(input_fn,'r') as f:
        data = json.load(f)
    dfa = DFA(data['states'],data['letters'],data['transition_function'],data['start_states'],data['final_states'])
    x = data['states']
    n = len(x) 
    sm = dict()     # state mapper maps states to integers 
    for i in range(len(x)):
        sm[x[i]] = i
    tbl = numpy.zeros((n,n))     # table of size nxn 
    for i in range(1,n):
        for j in range(n):
            if i > j:
                if (((x[i] in data['final_states']) and (x[j] not in data['final_states'])) or ((x[j] in data['final_states']) and (x[i] not in data['final_states']))):
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
                        if tbl[aa][bb] == 1:
                            chk = 1
                            tbl[i][j] = 1
                            break


    um_set = list()
    for i in range(1,n):
        for j in range(n):
            if ((i > j) and (tbl[i][j] == 0)):
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
    for i in range(ik+1):
        aaa = list()
        for ss in x:
            if dc[ss] == i:
                aaa.append(ss)
        if len(aaa)>0:
            states_list.append(aaa)

    trans_fn = list()
    for pstate in states_list:
        for l in data['letters']:
            bb1 = pstate[0]
            cc1 = dfa.gts(bb1,l)
            dd1 = dc[cc1]
            trans_fn.append([pstate,l,states_list[dd1]])
    
    final_st = list()
    st_idx = data['start_states']
    
    for i in states_list:
        for j in i:
            if j in dfa.final: 
                final_st.append(i)
     
    for i in states_list:
        if st_idx in i:
            ist_idx = i        
            break


    ooo = dict()
    ooo['states'] = states_list
    ooo['letters'] = data['letters']
    ooo['transition_function'] = trans_fn
    ooo['start_states'] = ist_idx
    ooo['final_states'] = final_st

    with open(output_fn,'w') as f:  
        json.dump(ooo, f ,indent = 4)
