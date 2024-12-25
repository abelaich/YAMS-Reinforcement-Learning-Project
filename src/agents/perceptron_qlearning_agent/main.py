# Run the simulation and plot the results
if __name__ == "__main__":
    agent = PerceptronQLearningAgent(
        name="Perceptron Q-Learning Agent",
        alpha=0.01,  # Reduced learning rate
        gamma=0.9,
        epsilon=0.2,
        lambda_=0.9,
        nb_dices=5,
        nb_faces=6,
        max_rounds=7,
        action_strategy="Perceptron Q-learning with eligibility traces"
    )
    
    scores = simulate_game(agent, num_games=10000)
    
    # Plot moving average of scores
    window_size = 500  # Sliding window size
    if len(scores) >= window_size:
        average_scores = [np.mean(scores[i:i+window_size]) for i in range(len(scores)-window_size)]
    else:
        average_scores = scores  # If fewer scores than window size
    
    # Plot score evolution
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(average_scores)), average_scores, label="Average score")
    plt.xlabel('Episodes')
    plt.ylabel('Average score')
    plt.title("Q-learning Agent Performance During Training")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Display the agent parameters for the report
    print(f"Q-learning Agent Parameters:")
    print(f"  - Number of dice: {agent.nb_dices}")
    print(f"  - Number of faces per die: {agent.nb_faces}")
    print(f"  - Epsilon (exploration): {agent.epsilon}")
    print(f"  - Alpha (learning rate): {agent.alpha}")
    print(f"  - Gamma (discount factor): {agent.gamma}")
    print(f"  - Maximum number of rounds per game: {agent.max_rounds}")
    print(f"  - Action strategy: {agent.action_strategy}")
