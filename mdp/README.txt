Implementation Value Iteration of MDP

- mdp structure

    {   state0: {
            action0: {
                'transitions': [ (stateX, probX), (stateY, probY), ... ],
                'reward': 0 },

            action1: {}
            action2: {}
        }
    }

- Usage
    - Run `python mdp.py`, you could specify input/output path in main() function