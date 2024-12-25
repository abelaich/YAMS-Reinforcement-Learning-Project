class GameEnvironment:
    def __init__(self, nb_dices, nb_faces, nb_turns):
        self.dices = nb_dices
        self.faces = nb_faces
        self.turns = nb_turns
        self.S = {'somme_1': 0, 'somme_2': 0, 'somme_3': 0, 'brelan': 0, 'paire': 0, 'chance': 0}  # Game rules for scoring points

    def get_action(self, dice_state):
        """Generate the possible actions and their rewards based on the dice_state."""
        a = {}
        for s in self.S:
            R = 0
            if self.S[s] == 0:  # If the category is not yet filled
                if s == 'somme_1':
                    R = dice_state[0] * 1
                elif s == 'somme_2':
                    R = dice_state[1] * 2
                elif s == 'somme_3':
                    R = dice_state[2] * 3
                elif s == 'brelan':
                    R = 15 if np.any(dice_state >= 3) else 0
                elif s == 'paire':
                    R = 5 if np.any(dice_state >= 2) else 0
                elif s == 'chance':
                    R = dice_state.sum()

                if R > 0:
                    a[s] = R

        return a

    # Simulate a complete game episode
    def play_episode(self):
        total_reward = 0
        for turn in range(self.turns):  # Iterate over each turn
            # print(f"Turn {turn + 1}:")
            MyTurn = TurnEnvironment(self.dices, self.faces)
            for roll in range(3):  # 3 dice rolls per turn
                current_state = MyTurn.get_state_from_action(np.zeros((self.faces), dtype='int'))  # Initial state of the turn
                action, reward = self.choose_action()  # Choose an action based on the state
                total_reward += reward  # Add the reward obtained in this state to the total reward

                # print(f" Roll {roll + 1}: State {current_state}, Action {action}, Reward {reward}")
            # print(f" Total Reward after Turn {turn + 1}: {total_reward}\n")
        return total_reward

    # Play multiple consecutive episodes
    def play_multiple_episodes(self, num_episodes):
        total_rewards = []
        for episode in range(num_episodes):  # Loop for each episode
            total_reward = self.play_episode()
            total_rewards.append(total_reward)

            # Display the total reward every 100 episodes
            if (episode + 1) % 100 == 0:
                print(f"Total Reward for Episode {episode + 1}: {total_reward}\n")
        return total_rewards

    # Select an action at each step of the game
    def choose_action(self):
        MyTurn = TurnEnvironment(self.dices, self.faces)
        reward_table = np.zeros((len(MyTurn.S), 5))  # Table of possible rewards
        # Fill the table for each state
        for i, s in enumerate(MyTurn.S):
            Aa = self.get_action(s)
            for j, a in enumerate(Aa):
                reward_table[i, j] = Aa[a]
        # Compute the values for the states
        v_3 = reward_table.max(axis=1)
        # Compute the new state values
        v_2, Q_2 = MyTurn.One_step_backward(v_3)
        v_1, Q_1 = MyTurn.One_step_backward(v_2)
        # Initial state of the turn with all dice at zero
        s0 = MyTurn.get_state_from_action(np.zeros((self.faces), dtype='int'))
        # Choose the best action from the initial state
        a0, _ = MyTurn.choose_best_action(s0, Q_1)
        # Move to the next state and choose the best action again
        s1 = MyTurn.get_state_from_action(a0)
        a1, _ = MyTurn.choose_best_action(s1, Q_2)
        s2 = MyTurn.get_state_from_action(a1)
        # Get the possible actions
        Aa = self.get_action(s2)
        if not Aa:
            return [], 0
        # Choose the action with the highest reward
        action = max(Aa, key=Aa.get)
        return action, Aa[action]

    def choose_random_action(self, dice_state):
        """Choose a random action from the available ones."""
        possible_actions = self.get_action(dice_state)
        if not possible_actions:  # If no action is possible
            return None, 0
        action = random.choice(list(possible_actions.keys()))
        return action, possible_actions[action]
