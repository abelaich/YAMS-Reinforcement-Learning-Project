class GreedyAgent:
    def __init__(self, nb_dices, nb_faces, nb_turns):
        # Initialize the game environment
        self.game_env = GameEnvironment(nb_dices, nb_faces, nb_turns)

    def play_game_with_agent(self, agent_level):
        """
        Simulates a game with a greedy agent (always chooses the action with the highest immediate reward).
        :param agent_level: The number of rolls allowed (agent's level).
        :return: The total score of the agent at the end of the game.
        """
        total_score = 0
        for turn in range(self.game_env.turns):  # Loop through each turn of the game
            MyTurn = TurnEnvironment(self.game_env.dices, self.game_env.faces)
            current_state = MyTurn.get_state_from_action(np.zeros((self.game_env.faces), dtype='int'))  # Initialize state

            for roll in range(agent_level):  # The number of rolls in a turn, defined by agent_level
                action, reward = self.choose_greedy_action(current_state)
                if not action:  # If no action is possible, stop the turn
                    break
                current_state = MyTurn.get_state_from_action(action)  # Update state based on the action
                total_score += reward  # Add the reward for the turn to the total score
        return total_score

    def choose_greedy_action(self, dice_state):
        """
        Chooses the action that maximizes the immediate reward (greedy strategy).
        :param dice_state: The current state of the dice in the game.
        :return: The action to be taken and the associated reward.
        """
        possible_actions = self.game_env.get_action(dice_state)
        if not possible_actions:  # If no actions are possible
            return None, 0
        # Choose the action with the highest reward
        best_action = max(possible_actions, key=possible_actions.get)
        return best_action, possible_actions[best_action]

def simulate_greedy_agent(nb_dices=4, nb_faces=5, nb_turns=10, num_simulations=1000, agent_level=1):
    """
    Simulates games with a greedy agent and displays the results.
    :param nb_dices: Number of dice in the game.
    :param nb_faces: Number of faces on each die.
    :param nb_turns: Number of turns in the game.
    :param num_simulations: Number of simulations to run.
    :param agent_level: The level of the agent, i.e., how many rolls per turn.
    """
    agent = GreedyAgent(nb_dices, nb_faces, nb_turns)
    total_scores = []

    # Run the simulations
    for _ in range(num_simulations):
        total_score = agent.play_game_with_agent(agent_level)
        total_scores.append(total_score)

    # Calculate statistics
    max_score = max(total_scores)
    min_score = min(total_scores)
    avg_score = sum(total_scores) / len(total_scores)

    # Print results
    print(f"Agent Level {agent_level}")
    print(f"Max Score: {max_score}")
    print(f"Min Score: {min_score}")
    print(f"Average Score: {avg_score:.2f}")

    # Plot the histogram of scores
    plt.figure(figsize=(10, 6))
    plt.hist(total_scores, bins=30, color='blue', alpha=0.7)
    plt.axvline(max_score, color='green', linestyle='dashed', linewidth=1, label=f"Max: {max_score}")
    plt.axvline(min_score, color='red', linestyle='dashed', linewidth=1, label=f"Min: {min_score}")
    plt.axvline(avg_score, color='orange', linestyle='dashed', linewidth=1, label=f"Average: {avg_score:.2f}")
    plt.title(f"Score Distribution Over {num_simulations} Simulations (Agent Level {agent_level})")
    plt.xlabel("Total Score")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()

def compare_greedy_agents(nb_dices=5, nb_faces=6, nb_turns=10, num_simulations=1000):
    """
    Compares the performance of greedy agents at different levels and displays the results.
    :param nb_dices: Number of dice in the game.
    :param nb_faces: Number of faces on each die.
    :param nb_turns: Number of turns in the game.
    :param num_simulations: Number of simulations to run.
    """
    total_scores = {'Level 1': [], 'Level 2': [], 'Level 3': []}

    # Run simulations for agents at different levels
    for agent_level in range(1, 4):
        agent = GreedyAgent(nb_dices, nb_faces, nb_turns)
        for _ in range(num_simulations):
            total_score = agent.play_game_with_agent(agent_level)
            total_scores[f'Level {agent_level}'].append(total_score)

    # Calculate average scores for each agent level
    avg_scores = {level: sum(scores) / len(scores) for level, scores in total_scores.items()}

    # Print average scores for each agent level
    print("Average Scores per Agent Level:")
    for level, avg_score in avg_scores.items():
        print(f"{level} : {avg_score:.2f}")

    # Plot the histogram comparing agent levels
    plt.figure(figsize=(10, 6))
    for level, scores in total_scores.items():
        plt.hist(scores, bins=30, alpha=0.5, label=f"{level} (Average: {avg_scores[level]:.2f})")
    
    plt.title(f"Comparison of Greedy Agents Over {num_simulations} Simulations")
    plt.xlabel("Total Score")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()
