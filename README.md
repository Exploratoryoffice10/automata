# Automata theory 

 > Q1: Convert Regular expression to NFA
 
 > Q2: Convert NFA to DFA
 
 > Q3: Convert DFA to Regular expression
 
 > Q4: DFA MINIMIZATION
 
---

# Q1

```
Converting regular expression to NFA. In the regex there is no special symbol for concatenation here for ease we are using `.` . 
First we take the given regular expression and add concatenation symbol. to it next we convert the expression to postfix based on
the precedence of star(*) > union(+) > concatenation(.) . Now we have the postfix expression. We make the final nfa similar to the 
way we solve a numeric postfix expression using stack. We are maintaining a nfa stack. Initially stack is empty. When we get a alphabet 
or numerical we create a NFA which accepts that symbol and we push it to the stack. 

If we get a `.` then it means we have to concatenate. so we pop the top two nfa.if top two nfa attribute to regexp a1, a2. a1 is top and 
a2 is penultimate. Then We have to perform a2.a1. So we create a new nfa whose start states are start states of a2 and whose final states 
are final states of a1. states of this new NFA will be union of states of the two nfa. transition function will be the union of transition 
functions of a1 and a2 along with epsilon-transitions from final states of a2 to start states of a1. in this way we handle concatenation. 

`+` signifies union. For union we pluck the top two nfa from the stack. for union the order doesnt matter as they result in the same 
expression either way. So we are creating a new state and we are putting epsilon transitions from the new states to the start states 
of both NFA's. The final states of the new nfa will be the union of the final states of the new nfa's. THe transition function contains 
the union of transition functions of both nfa's along with the epsilon transitions added. The state set is the union of state set of both 
nfa's along with the new state just added. and finally this new nfa is pushed in to the stack. 

Finally we have star operation. For this we pop the top most nfa from the stack. We add a new state and make it the start state of the 
new nfa. Now we add epsilon transitions from final states of the popped nfa to start state of the popped nfa. We add a epsilon transition 
from the new state added to the start state of the popped nfa. The final states of the new nfa will be same as the old nfa. The start state 
will be the new state we added. The transition function of the new nfa contains the transition function of the old nfa along with all the 
epsilon transition function states added. and when all operations are completed the stack will contain only one nfa which is the resultant 
nfa for the given regular expression. and finally for the letters we parse through the given regular expression and add all the letters 
and numericals to the letters set. By this we get the letter set. we already calculated the state set, start state, final state set and 
transition function. And finally we write this nfa to the new file.

```


---

# Q2

```

We are converting nfa to dfa. Let Q be the set of states of the nfa.Every  state of dfa is a subset of Q*. So for every r that belongs 
to state of dfa , We are taking the union of all gamma(r,a) (a is a letter) for every state of the nfa. In nfa we can have multiple 
states in the transition function result. So this union contains different states. So we rearrange the order to make it such it belongs 
to the state set. The final set of the dfa will be the states which contain a state of final states of the nfa as a state in the set of 
states (every set of the dfa is a set of states is a subset of states of the nfa). The state set of the dfa will be powerset of the 
state set of the nfa.


````

---

# Q3

```

This question is solved by using state reduction method. First step we are converting into gnfa. For this we are creating two new 
states start state(`qs`) and final state(`qf`). Next we add epsilon transition from new start states(`qs`) to old start states 
and old final state to new final state(`qf`). The edges are the regular expressions which take us to the other state. Now if 
there are multiple inputs for which we can go from one state we take union of all of that inputs. At first we are setting the 
edges. Now if pluck one state after other till there is only `qs` and `qf` left. the edge contains the regular expression for 
the nfa. So if there exists a edge between qi and qj via qrip. then we can go to qi to qrip and hop at qrip infinitely many 
times if we want and transition to qj from qrip or go directly to qj from qi directly. So if qi to qrip is R1 , qrip to qrip 
is R2 and qrip to qj is R3 and qi to qj is R4. then qi to qj will be (R1)(R2)*(R3)+R4. we can go to qj via qrip or going 
directly to qj if a edge exists. if a edge doesnt exist then R4 will be null. As there is no way we can do that. FIrst 
qrip is different from qi and qj. qi belongs to `Q'-{qs}` and qj belongs to `Q'-{qj}`. WHere `Q' = Q + {qs,qj}`. Where 
Q is the set of states of the dfa. By this method we remove state one by one and finally remove all the states. At every 
step we update the paths based on the above rule. SO after removal of each state we get new values.



```

---

# Q4

```

First step is to remove the unreachable states. For this we start with the start state and add the states to which we can 
go from the start state. now we have added new states to the element. So We add all the states we can reach from the states 
we added before and we continue this process until no states are added(the states which are added recently are already in 
the state set. So irrespective of the number of operations we do it will always have the same set). We use two set to 
achieve this before the states we can reach from the recently added states are added both state set are equalized. now 
we add new states to one of the set and we go on till this two sets have same length which implies no more states can 
be added. We got the reachable state. Now we update the final state and transition set so that unreachable state won't 
be present. We remove all the transitions from the unreachable states. We also remove unreachable states from the final states.

For now unreachable states are removed. Now we have to minimize the dfa. For minimization myhill nerode theorem is used. We create 
a table and initially mark if one of the pair of qi,qj belongs to F while other belongs to Q-F. and lets states a,b on passing a 
certain input go to c,d we see if pair (c,d) is marked if it is marked then we mark (a,b). We finally pick the unmarked states and 
merge them based on the pairs they can be formed. if two pairs have a element in common we merge them. All the states which are not 
in the union of all the unmarked pairs are independent states which means they cant be merged with any other. Finally we update the 
state set, start state and final states of the dfa. we update the transition based on the merging of states done before. For merging 
we take the first element of the state and go the resultant state based on the dictionary which stores values. Finally the final states are updated. 


```



### THE END 
