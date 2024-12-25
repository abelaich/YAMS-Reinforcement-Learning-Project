class TurnEnvironment:
    def __init__(self, nb_dices, nb_faces):
        self.dices = nb_dices  # Number of dice
        self.faces = nb_faces  # Number of faces on each die
        self.Roll, self.Roll_P = self.get_states()  # Possible states of the dice and their probabilities
        self.S = self.Roll[0]  # Initialization of the starting states
        self.Aa = self.get_actions_list()  # List of possible actions

    # Generates all possible states
    def get_states(self):
        Roll = [[] for _ in range(self.dices)]  # List of states
        Roll_P = []  # Probabilities of the states

        # Generating all possible dice states
        for it in itertools.product(range(self.faces), repeat=self.dices):
            for d in range(self.dices):
                s = np.zeros((self.faces), dtype='int')
                for f in range(self.faces):
                    s[f] = it[d:].count(f)
                    if s.sum() == self.dices:
                        break
                Roll[d].append(s)

        # Calculating the probabilities of the states
        for d in range(self.dices):
            S, counts = np.unique(Roll[d], axis=0, return_counts=True)
            Roll[d] = list(S)
            Roll_P.append(counts / counts.sum())
        return Roll, Roll_P

    # Calculates possible actions for a given state
    def get_actions_from_state(self, s):
        nb_actions = np.prod(s + 1)  # Number of possible actions for each state
        A = np.zeros((nb_actions, self.faces), dtype='int')  # Action matrix
        l = []
        for f in range(self.faces):
            l.append(list(np.arange(s[f] + 1)))  # Possible actions for each face
        k = 0
        for i in itertools.product(*l):
            A[k, :] = np.array(i)
            k += 1
        return A

    # List of all possible actions from all possible states
    def get_actions_list(self):
        Aa = []
        for s in self.S:
            Aa += self.get_actions_from_state(s).tolist()
            Aa = list(np.unique(Aa, axis=0))  # Removing duplicate actions
        return Aa

    # Returns the index of state S in the list of states S
    def get_state_index(self, S):
        return np.argwhere((self.S == S).sum(axis=1) == self.faces)[0][0]

    # Returns the index of action a in the list of actions Aa
    def get_action_index(self, a):
        return np.argwhere((a == self.Aa).sum(axis=1) == self.faces)[0][0]

    # Determines the resulting states from a given action and the associated probabilities
    def get_states_from_action(self, a):
        if a.sum() == self.dices:
            return [a], np.array([1.])
        return np.array(self.Roll[a.sum()]) + a, self.Roll_P[a.sum()]

    # Computes new state values and Q-values from previous states
    def One_step_backward(self, v_out):
        v_in = np.zeros(len(self.S))  # Initializing the state values table
        a_in = np.zeros(len(self.Aa))  # Action values table
        Q_in = np.zeros((len(self.S), len(self.Aa)))  # Q-values table

        # Updating Q-values
        for a in self.Aa:
            i_a = self.get_action_index(a)
            Sr, Pr = self.get_states_from_action(a)
            for k in range(len(Pr)):
                i_sr = self.get_state_index(Sr[k])
                a_in[i_a] += Pr[k] * v_out[i_sr]

        # Calculating state values for the next round
        for s in self.S:
            A = self.get_actions_from_state(s)
            i_s = self.get_state_index(s)
            for a in A:
                i_a = self.get_action_index(a)
                Q_in[i_s][i_a] = a_in[i_a]
            v_in[i_s] = Q_in[i_s].max()

        return v_in, Q_in

    def get_state_from_action(self, a):
        r = self.dices
        dice_view = list(np.random.randint(0, high=self.faces, size=r))
        s = np.zeros((self.faces), dtype='int')
        for f in range(self.faces):
            s[f] = dice_view.count(f)
            if s.sum() == r:
                break
        return s

    def choose_best_action(self, s, Q):
        i_s = self.get_state_index(s)
        i_a = np.argmax(Q[i_s])
        return self.Aa[i_a], i_a