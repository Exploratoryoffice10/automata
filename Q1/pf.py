def  itp_ord(x):
    ord_dict = {
            '+' : 1,
            '.' : 2,
            '*' : 3,
            '(' : 0
    }
    return ord_dict.get(x,0)


def topostfix(st):
    fpexp = list()  # final string in postfix
    stk = list()    # stack
    # while (len(st) != n):
    ist = list()
    print('initial:',st)
    ist.append(st[0])
    for i in range(1,len(st)):
            a = st[i-1]
            b = st[i]
            if ((a.isalnum() and b.isalnum()) or (a.isalnum() and b=='(') or (a=='*' and b=='(') or (a == ')' and b.isalnum()) or ((a=='*') and b.isalnum())):   
                ist.append('.')
            ist.append(b)
    print('after',''.join(ist))
    for i in ist:
        if i.isalpha(): # is a alphabet
            fpexp.append(i)
        elif i == '(':   # should be a operator
            stk.append(i)
        elif i == ')':
            while(len(stk)>0 and (stk[-1] != '(')):
                fpexp.append(stk.pop())
            if ((len(stk) == 0) or (stk[-1] != '(')):
                print('wrong format')
                quit()
            else:
                stk.pop()
        else:
            while((len(stk)>0) and (itp_ord(i) <= itp_ord(stk[-1]))):  
                fpexp.append(stk.pop())
            stk.append(i)

    while len(stk)!=0:
        fpexp.append(stk.pop())
    return fpexp

# ad = topostfix("(ab)*+ba+c*")
ad = topostfix("(ab)+a")
print('final',''.join(ad))