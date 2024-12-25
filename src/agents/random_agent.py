import numpy as np
import matplotlib.pyplot as plt

# Class for RandomAgent
class RandomAgent:
    def __init__(self, nb_dices, nb_faces, nb_turns):
        self.game_env = GameEnvironment(nb_dices, nb_faces, nb_turns)

    def play_game_with_random_agent(self):
        """Simulates a game with a random agent."""
        total_score = 0
        for turn in range(self.game_env.turns):
            # Initialize TurnEnvironment for each turn
            MyTurn = TurnEnvironment(self.game_env.dices, self.game_env.faces)
            current_state = MyTurn.get_state_from_action(np.zeros((self.game_env.faces), dtype='int'))
            
            for roll in range(3):  # Up to 3 rolls per turn
                action, reward = self.game_env.choose_random_action(current_state)
                if not action:  # If no valid action is possible
                    break
                current_state = MyTurn.get_state_from_action(action)  # Update state after action
                total_score += reward  # Add the reward for the action
        return total_score


def simulate_random_agent(nb_dices=4, nb_faces=5, nb_turns=10, num_simulations=1000):
    """Runs multiple simulations with a random agent and displays the results."""
    agent = RandomAgent(nb_dices, nb_faces, nb_turns)
    total_scores = []

    for _ in range(num_simulations):
        total_score = agent.play_game_with_random_agent()
        total_scores.append(total_score)

    # Calculating statistics
    max_score = max(total_scores)
    min_score = min(total_scores)
    avg_score = sum(total_scores) / len(total_scores)

    # Displaying results
    print(f"Max Score: {max_score}")
    print(f"Min Score: {min_score}")
    print(f"Average Score: {avg_score:.2f}")

    # Plotting the distribution
    plt.figure(figsize=(10, 6))
    plt.hist(total_scores, bins=30, color='blue', alpha=0.7)
    plt.axvline(max_score, color='green', linestyle='dashed', linewidth=1, label=f"Max: {max_score}")
    plt.axvline(min_score, color='red', linestyle='dashed', linewidth=1, label=f"Min: {min_score}")
    plt.axvline(avg_score, color='orange', linestyle='dashed', linewidth=1, label=f"Average: {avg_score:.2f}")
    plt.title(f"Distribution of Scores over {num_simulations} Simulations")
    plt.xlabel("Total Score")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()
