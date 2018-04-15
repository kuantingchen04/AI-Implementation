#!/usr/bin/env python





# Parsers
def read_mdp(fname):
    """"""

    with open(fname, 'r') as f:

        # States
        f.readline()
        s = f.readline().rstrip('\n').replace(' ', '').split(',') # ['S0','S1']

        # Actions
        f.readline()
        a = f.readline().rstrip('\n').replace(' ', '').split(',')  # ['a0','a1']

        # Transition model
        f.readline()
        f.readline()

        for i in range(len(a)):
            f.readline()
            for j in range(len(s)):
                f.readline()

        # Rewards
        f.readline()
        for i in range(len(a)*len(s)):
            f.readline()

        # Discount
        f.readline()
        gamma = f.readline().rstrip('\n')

        # Epsilon
        f.readline()
        esp = f.readline().rstrip('\n')

        return s, a, gamma, esp


def main():
    mdp_file = "mdpinput.txt"
    print read_mdp(mdp_file)

if __name__ == '__main__':
    main()