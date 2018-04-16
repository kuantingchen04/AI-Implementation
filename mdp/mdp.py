#!/usr/bin/env python

class Markov:

    def __init__(self):
        self.mdp = dict()
        self.gamma = 0

    # Parser
    def add_state(self, states):
        self.mdp[states] = dict()

    def add_action(self, states, action):
        self.mdp[states][action] = {'transitions': [], 'reward': 0}

    def add_reward(self, states, action, reward):
        self.mdp[states][action]['reward'] = reward

    def add_transition(self, states, action, result_state, prob):
        if action not in self.mdp[states]:
            self.add_action(states, action)
        self.mdp[states][action]['transitions'].append( (result_state, prob) )

    def add_gamma(self, gamma):
        self.gamma = gamma

    # Access
    def states(self):
        return self.mdp.keys()

    def actions(self, state):
        return self.mdp[state].keys()

    def T(self, state, action): # return [ (result-states, prob) ]
        return self.mdp[state][action]['transitions']

    def R(self, state, action):
        return self.mdp[state][action]['reward']


# Parsers
def read_mdp(fname, mdp):
    """"""

    with open(fname, 'r') as f:

        # States
        f.readline()
        states = f.readline().rstrip('\n').replace(' ', '').split(',') # ['S0','S1']
        for x in states:
            mdp.add_state(x)

        # Actions
        f.readline()
        actions = f.readline().rstrip('\n').replace(' ', '').split(',')  # ['a0','a1']

        # Transition model
        f.readline()
        f.readline()

        for i in range(len(actions)): # action
            f.readline() # skip
            a = actions[i]
            for j in range(len(states)): # states
                s = states[j]

                transition = f.readline().rstrip('\n').replace(' ', '').split(',')
                for k, prob in enumerate(transition):
                    res_s = states[k]
                    mdp.add_transition(s, a, res_s, float(prob))

        # Rewards
        f.readline()
        for i in range(len(actions)*len(states)):
            s, a, reward = f.readline().rstrip('\n').replace(' ', '').split(',')
            mdp.add_reward(s,a, float(reward))

        # Discount
        f.readline()
        gamma = float(f.readline().rstrip('\n'))
        mdp.add_gamma(gamma)

        # Epsilon
        f.readline()
        esp = float(f.readline().rstrip('\n'))

        return esp

def value_iteration(mdp, esp):
    u_kk = { s: 0.0 for s in mdp.states() }
    gamma = mdp.gamma

    best_a = { s: None for s in mdp.states() } # policy

    while True:
        u_k = u_kk.copy()
        max_delta = 0 # get max delta among the states

        for s in mdp.states():
            # best_u = -float("inf") # for each s, find the best action
            cand_u, cand_a = [], []
            for a in mdp.actions(s):
                u = 0
                for res_s, prob in  mdp.T(s, a):
                    u += prob * (gamma * u_k[res_s] + mdp.R(s,a))
                cand_u.append(u)
                cand_a.append(a)

            u_kk[s], best_a[s] = max(zip(cand_u,cand_a), key=lambda pair: pair[0])

            max_delta = max(max_delta, abs(u_kk[s]-u_k[s]))
        if max_delta < esp * (1.0 - gamma) / gamma:
            return u_k, best_a

def write_policy(fname, utility, policy):
    with open(fname, 'w') as f:
        for s in sorted(policy):
            line = "%s: %s (%.2f)\n" % (s, policy[s], utility[s])
            f.write(line)

def main():
    mdp_file = "mdpinput.txt"
    out_file = "policy.txt"

    mdp = Markov()
    esp = read_mdp(mdp_file, mdp)

    # print mdp.mdp
    utility, policy = value_iteration(mdp, esp)
    write_policy(out_file, utility, policy)

if __name__ == '__main__':
    main()