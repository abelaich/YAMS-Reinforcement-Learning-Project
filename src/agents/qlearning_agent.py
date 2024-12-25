class DiceGameGreedyQlearning:
    def __init__(self, nb_dices=4, nb_faces=5, epsilon=0.4, alpha=0.4, gamma=0.9, max_rounds=10, action_strategy='greedy'):
        self.nb_dices = nb_dices
        self.nb_faces = nb_faces
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.state_space = self.calculate_unique_combinations()
        self.q_table = self.initialize_q_table()
        self.max_rounds = max_rounds
        self.current_round = 0
        self.action_strategy = action_strategy

    def calculate_unique_combinations(self):
        combinations = list(combinations_with_replacement(range(1, self.nb_faces + 1), self.nb_dices))
        return combinations

    def initialize_q_table(self):
        return np.random.uniform(low=0, high=1, size=(len(self.state_space), 2 ** self.nb_dices))

    def get_state_index(self, state):
        return self.state_space.index(state)

    def get_best_action(self, state_index):
        if self.action_strategy == 'random':
            return random.choice(range(2 ** self.nb_dices))
        elif self.action_strategy == 'greedy':
            return np.argmax(self.q_table[state_index])
        else:
            raise ValueError("Invalid action strategy. Choose 'greedy' or 'random'.")

    def roll_dice(self, keep=[]):
        dice = [random.randint(1, self.nb_faces) for _ in range(self.nb_dices)]
        for i in range(self.nb_dices):
            if i not in keep:
                dice[i] = random.randint(1, self.nb_faces)
        return tuple(sorted(dice))

    def play_round_with_action(self, state, action):
        keep = [i for i in range(self.nb_dices) if action[i] == '1']
        final_dice = self.roll_dice(keep)
        return sum(final_dice)

    def play_game_with_agent(self, nb_rounds=10):
        total_score = 0

        for _ in range(nb_rounds):
            self.current_round += 1
            state = self.state_space[random.randint(0, len(self.state_space) - 1)]
            state_index = self.get_state_index(state)
            action_index = self.get_best_action(state_index)
            action = bin(action_index)[2:].zfill(self.nb_dices)

            reward = self.play_round_with_action(state, action)
            total_score += reward

            next_state = self.roll_dice([i for i in range(self.nb_dices) if action[i] == '1'])
            next_state_index = self.get_state_index(next_state)
            best_next_action_index = np.argmax(self.q_table[next_state_index])

            self.q_table[state_index, action_index] += self.alpha * (
                reward + self.gamma * self.q_table[next_state_index, best_next_action_index] - self.q_table[state_index, action_index])

        return total_score

    def train_and_evaluate(self, num_episodes=1000):
        scores = []
        for _ in tqdm(range(num_episodes), desc="Training Progress"):
            self.current_round = 0
            total_score = self.play_game_with_agent(nb_rounds=self.max_rounds)
            scores.append(total_score)

        window_size = 500
        average_scores = [np.mean(scores[i:i+window_size]) for i in range(len(scores)-window_size)]
        
        plt.figure(figsize=(10,6))
        plt.plot(range(len(average_scores)), average_scores, label="Score moyen")
        plt.xlabel('Épisodes')
        plt.ylabel('Score moyen')
        plt.title('Performance de l\'agent Q-learning pendant l\'entraînement')
        plt.legend()
        plt.grid(True)
        plt.show()

        print(f"Paramètres de l'agent Q-learning :")
        print(f"  - Nombre de dés: {self.nb_dices}")
        print(f"  - Nombre de faces par dé: {self.nb_faces}")
        print(f"  - Epsilon (exploration): {self.epsilon}")
        print(f"  - Alpha (taux d'apprentissage): {self.alpha}")
        print(f"  - Gamma (facteur de discount): {self.gamma}")
        print(f"  - Nombre maximal de tours par partie: {self.max_rounds}")
        print(f"  - Stratégie d'action: {self.action_strategy}")

        return scores