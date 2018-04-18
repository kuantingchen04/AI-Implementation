#!/usr/bin/env python

"""Implementation Value Iteration of MDP"""


class MarkovDecisionProcess:
    """
    the mdp datastruture contains
    mdp {   state0: {
                action0: {
                    'transitions': [ (stateX, probX), (stateY, probY), ... ],
                    'reward': 0 },

                action1: {}
                action2: {}
            }
        }
    """

    def __init__(self):
        self.mdp = dict()
        self.gamma = 0

    # Parser
    def add_state(self, states):
        """Update a state"""
        self.mdp[states] = dict()

    def add_action(self, states, action):
        """Each action contains possible transitions and rewards (here only 1 reward)"""
        self.mdp[states][action] = {'transitions': [], 'reward': 0}

    def add_reward(self, states, action, reward):
        """Update the reward of a transition (s,a,s'). (here (s,a) only)"""
        self.mdp[states][action]['reward'] = reward

    def add_transition(self, states, action, result_state, prob):
        """Update the (result-states, prob) pairs, r-state with prob=0 will not be stored"""
        if action not in self.mdp[states]:
            self.add_action(states, action)
        self.mdp[states][action]['transitions'].append((result_state, prob))

    def add_gamma(self, gamma):
        """Discount factor"""
        self.gamma = gamma

    # Access
    def states(self):
        """Return list of states in MDP"""
        return self.mdp.keys()

    def actions(self, state):
        """Return list of actions of a given state"""
        return self.mdp[state].keys()

    def T(self, state, action):
        """Transition: Return a list of (result-states, prob) as a result of (s,a)"""
        return self.mdp[state][action]['transitions']

    def R(self, state, action):
        """Reward: Return the reward of (s,a)"""
        return self.mdp[state][action]['reward']


# Parsers
def read_mdp(fname, mdp):
    """Read and return mdp object"""

    with open(fname, 'r') as f:

        # States
        f.readline()
        states = f.readline().rstrip('\n').replace(', ', ',').split(',')  # ['S0','S1']
        for x in states:
            mdp.add_state(x)

        # Actions
        f.readline()
        actions = f.readline().rstrip('\n').replace(', ', ',').split(',')  # ['a0','a1']

        # Transition model
        f.readline()
        f.readline()

        for i in range(len(actions)):  # action
            f.readline()  # skip
            action = actions[i]
            for j in range(len(states)):  # states
                state = states[j]

                transition = f.readline().rstrip('\n').replace(', ', ',').split(',')
                for k, prob in enumerate(transition):
                    if float(prob) == 0.0:
                        continue
                    res_state = states[k]
                    mdp.add_transition(state, action, res_state, float(prob))

        # Rewards
        f.readline()
        for i in range(len(actions) * len(states)):
            state, action, reward = f.readline().rstrip('\n').replace(', ', ',').split(',')
            mdp.add_reward(state, action, float(reward))

        # Discount
        f.readline()
        gamma = float(f.readline().rstrip('\n'))
        mdp.add_gamma(gamma)

        # Epsilon
        f.readline()
        esp = float(f.readline().rstrip('\n'))

        return esp


def value_iteration(mdp, esp):
    """Main Program"""
    u_kk = {s: 0.0 for s in mdp.states()}
    gamma = mdp.gamma

    best_a = {s: None for s in mdp.states()}  # policy

    while True:
        u_k = u_kk.copy()
        max_delta = 0  # get max delta among the states

        for s in mdp.states():
            # best_u = -float("inf") # for each s, find the best action
            cand_u, cand_a = [], []
            for a in mdp.actions(s):
                u = 0
                for res_s, prob in mdp.T(s, a):
                    u += prob * (gamma * u_k[res_s] + mdp.R(s, a))
                cand_u.append(u)
                cand_a.append(a)

            u_kk[s], best_a[s] = max(
                zip(cand_u, cand_a), key=lambda pair: pair[0])

            max_delta = max(max_delta, abs(u_kk[s] - u_k[s]))
        if max_delta < esp * (1.0 - gamma) / gamma:
            return u_k, best_a


def write_policy(fname, utility, policy):
    """Write the results given policy and utilities"""
    with open(fname, 'w') as f:
        f.write("% Format:  State: Action (Value)\n")
        for s in sorted(policy):
            line = "%s: %s (%.2f)\n" % (s, policy[s], utility[s])
            f.write(line)


def main():
    """Read file, run program and write file"""
    mdp_file = "mdpinput.txt"
    out_file = "policy.txt"

    mdp = MarkovDecisionProcess()
    esp = read_mdp(mdp_file, mdp)

    # print mdp.mdp
    utility, policy = value_iteration(mdp, esp)
    write_policy(out_file, utility, policy)


if __name__ == '__main__':
    main()
