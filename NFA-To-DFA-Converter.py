class NFA:
    def __init__(self,states,sigma,delta,finals):
        self.states = states
        self.sigma = sigma
        self.delta = delta
        self.finals = finals
        self.landa_closure_list = []

    def landa_closure(self,qi):
        try:
            q = self.delta[f"{qi}landa"]
            self.landaset.add(q) 
        except:
            return
        else:
            self.landa_closure(q) 

    def landa_closure_single(self,qi,transet):
        try:
            q = self.delta[f"{qi}landa"]
            transet.add(q) 
        except:
            return transet
        else:
            self.landa_closure_single(q,transet)

    def get_landa_closure(self):
        for q in self.states:
            self.landaset = set()
            self.landaset.add(q)
            self.landa_closure(q)
            self.landa_closure_list.append(self.landaset)
        for i in range(len(self.landa_closure_list)):
            self.landa_closure_list[i] = list(self.landa_closure_list[i])
        self.landa_closure_dic = {}
        for i in range(len(self.landa_closure_list)):
            self.landa_closure_dic[f'q{i}'] = self.landa_closure_list[i]

    def get_landa_closure_list(self):
        self.get_landa_closure() 
        print(self.landa_closure_list)
        for i in range(len(self.landa_closure_list)):
            print(f"Landa_closure(q{i}): ",self.landa_closure_list[i]) 

    def transition_function(self):
        self.transition = {}
        for i in range(len(self.landa_closure_list)):
            for alpha in self.sigma:
                transet = set()
                for j in range(len(self.landa_closure_list[i])):
                    q = self.landa_closure_list[i][j]
                    try:
                        delt = delta[f'{q}{alpha}']
                        if type(delt) == list:
                            for k in delt:
                                tmp = self.landa_closure_list[int(k[1])]
                                for t in tmp: transet.add(t)
                        else:
                            tmp = self.landa_closure_list[int(delt[1])]
                            for t in tmp: transet.add(t) 
                    except:
                        pass
                self.transition[f'q{i}{alpha}'] = transet
        for key in self.transition:
            self.transition[key] = list(self.transition[key])

    def convert_nfa_to_dfa(self):
        nfa.get_landa_closure()
        nfa.transition_function()
        print('landa closure')
        print(self.landa_closure_dic)
        print('__________________________________________________________________')
        print('transition')
        print(self.transition)
        print('__________________________________________________________________')
        self.dfa_delta = {}
        self.dfa_states_list = [self.landa_closure_list[0]]
        self.get_dfa_delta(self.landa_closure_list[0])
        for k in range(len(self.dfa_states_list)):
            self.dfa_states_list[k] = set(self.dfa_states_list[k])
        self.dfa_states = []
        for i in self.dfa_states_list:
            if i not in self.dfa_states:
                self.dfa_states.append(i)
        for j in range(len(self.dfa_states)):
            self.dfa_states[j] = list(self.dfa_states[j])
        print('DFA sigma')
        print(self.sigma)
        print('__________________________________________________________________')
        print('DFA states')
        print(self.dfa_states)
        print('__________________________________________________________________')
        print('DFA q0')
        q0 = self.landa_closure_list[0]
        print(q0)
        print('__________________________________________________________________')
        print('DFA delta')
        print(self.dfa_delta)
        print('__________________________________________________________________')
        self.dfa_final_states = []
        self.get_dfa_final_states()
        print('DFA final states')
        print(self.dfa_final_states)
    
    def get_dfa_final_states(self):
        for i in self.finals:
            for j in self.dfa_states:
                if i in j:
                    self.dfa_final_states.append(j)

    def get_dfa_delta(self,new_states):
        tag = True
        for states in self.dfa_states_list:
            for alpha in self.sigma:
                try:
                    self.dfa_delta[f'{states}{alpha}']
                except:
                    tag = False
        if tag == True: 
            return
        else:
            for al in self.sigma:
                state_set = set()
                for st in self.dfa_states_list[-1]:
                    for q in self.transition[f'{st}{al}']:
                        state_set.add(q)
                self.dfa_delta[f'{new_states}{al}'] = list(state_set) 
            for sig in self.sigma:
                self.dfa_states_list.append(self.dfa_delta[f'{new_states}{sig}'])
                self.get_dfa_delta(self.dfa_states_list[-1])

    def __str__(self):
        s = '_____________________________________________________________' + '\n'
        s += 'NFA\n'
        s += 'States:' + str(self.states) + '\n'
        s += 'Sigma:' + str(self.sigma) + '\n'
        s += 'Delta:' + str(self.delta) + '\n'
        s += 'Final states:' + str(self.finals) + '\n'
        s += '_____________________________________________________________'
        return s
    
# states = input("enter states: ").split()
# sigma = input("enter sigma: ").split()

# delta = {}
# while True:
#     state_sigma_state = input("enter state-sigma-state: ")
#     if state_sigma_state == '0': break
#     state_sigma_state = state_sigma_state.split() 
#     delta[state_sigma_state[0]] = state_sigma_state[1]
# finals = input("enter final states: ").split()

# states = ['q0','q1','q2','q3','q4']
# sigma = ['a','b']
# delta = {"q0b":"q3","q0a":"q1","q0landa":"q1","q1a":"q2","q1landa":"q3","q2b":['q2','q4'],"q3a":['q3','q4'],"q3b":"q3","q4landa":"q1","q4a":"q4",'q4b':'q4'} 
# finals = ['q4'] 

states = ['q0','q1','q2']
sigma = ['a','b','c']
delta = {'q0a':['q0','q1','q2'],'q1b':'q1','q2c':'q2','q2landa':'q1'}
finals = ['q1']

nfa = NFA(states,sigma,delta,finals)

nfa.convert_nfa_to_dfa() 