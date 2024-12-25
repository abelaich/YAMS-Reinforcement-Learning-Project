# the scoring categories
SCORING_CATEGORIES = [
    "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "Three of a Kind"
]

# Function to roll 5 dice
def roll_dice():
    return [random.randint(1, 6) for _ in range(5)]

# Function to calculate the score for a category
def calculate_score(category, roll):
    count = {i: roll.count(i) for i in range(1, 7)}
    
    if category == "Ones":
        return count[1] * 1
    elif category == "Twos":
        return count[2] * 2
    elif category == "Threes":
        return count[3] * 3
    elif category == "Fours":
        return count[4] * 4
    elif category == "Fives":
        return count[5] * 5
    elif category == "Sixes":
        return count[6] * 6
    elif category == "Three of a Kind":
        for num in range(1, 7):
            if count[num] >= 3:
                return sum(roll)
        return 0  # Return 0 if "Three of a Kind" condition isn't met
    return 0  # Return 0 by default if an invalid category is provided

# Feature extraction with normalization and combination features
def extract_features(state):
    roll, categories_used = state
    features = []
    # Atomic Features
    features.append(sum(roll) / 30.0)  # Normalized sum of dice (max possible is 30)
    features.append(len(categories_used) / len(SCORING_CATEGORIES))  # Normalized count of used categories
    features.append(1 if any(roll.count(i) >= 3 for i in range(1, 7)) else 0)  # Binary: can fill "Three of a Kind"
    features.append(roll.count(6) / 5.0)  # Proportion of 6's
    features.append(roll.count(5) / 5.0)  # Proportion of 5's
    
    # Combination Features
    features.append((sum(roll) / 30.0) * (len(categories_used) / len(SCORING_CATEGORIES)))  # Sum * categories used
    features.append((roll.count(6) / 5.0) * (roll.count(5) / 5.0))  # Proportion of 6's * 5's
    
    return np.array(features)

# Perceptron Q-learning agent with eligibility traces
class PerceptronQLearningAgent:
    def __init__(self, name, alpha=0.01, gamma=0.9, epsilon=0.2, lambda_=0.9, nb_dices=5, nb_faces=6, max_rounds=7, action_strategy="Perceptron Q-learning with eligibility traces"):
        self.name = name
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.lambda_ = lambda_  # Eligibility trace decay
        self.weights = {a: np.zeros(7) for a in SCORING_CATEGORIES}  # Weights for each action (feature size=7)
        self.local_traces = {a: np.zeros(7) for a in SCORING_CATEGORIES}  # Local eligibility traces
        self.categories_used = []
        self.score = 0
        # Parameters for display
        self.nb_dices = nb_dices
        self.nb_faces = nb_faces
        self.max_rounds = max_rounds
        self.action_strategy = action_strategy

    def choose_category(self, state):
        if random.random() < self.epsilon:
            # Exploration: Random category
            available_categories = [cat for cat in SCORING_CATEGORIES if cat not in self.categories_used]
            action = random.choice(available_categories)
        else:
            # Exploitation: Choose best category based on weights
            features = extract_features(state)
            q_values = {a: np.dot(self.weights[a], features) for a in SCORING_CATEGORIES if a not in self.categories_used}
            action = max(q_values, key=q_values.get)
        return action

    def update(self, state, action, reward, next_state):
        # Extract features for current and next state
        current_features = extract_features(state)
        next_features = extract_features(next_state)
        
        # Calculate Q-values
        q_current = np.dot(self.weights[action], current_features)
        available_next_categories = [a for a in SCORING_CATEGORIES if a not in self.categories_used]
        if available_next_categories:
            q_next = max([np.dot(self.weights[a], next_features) for a in available_next_categories])
        else:
            q_next = 0.0  # No next state
        
        # Calculate TD error
        td_error = reward + self.gamma * q_next - q_current
        
        # Prevent extremely large or small td_error
        if np.abs(td_error) > 1e6:
            print(f"TD error too large: {td_error}")
            td_error = 0.0  # Ignore this update
        
        # Update eligibility trace for the current action
        self.local_traces[action] += current_features
        
        # Update weights for all actions based on eligibility traces
        for a in SCORING_CATEGORIES:
            self.weights[a] += self.alpha * td_error * self.local_traces[a]
            # Clip weights to prevent overflow
            self.weights[a] = np.clip(self.weights[a], -1e5, 1e5)
        
        # Decay eligibility traces
        for a in SCORING_CATEGORIES:
            self.local_traces[a] *= self.gamma * self.lambda_
        
        # Debug output (optional, comment out in production)
        # print(f"Action: {action}, Reward: {reward}, TD error: {td_error}")

    def reset(self):
        self.categories_used = []
        self.score = 0
        self.local_traces = {a: np.zeros(7) for a in SCORING_CATEGORIES}

# Simulate the game
def simulate_game(agent, num_games=10000):
    scores = []
    for game in range(num_games):
        agent.reset()
        total_score = 0
        state = (roll_dice(), [])
        while len(agent.categories_used) < len(SCORING_CATEGORIES):
            action = agent.choose_category(state)
            score = calculate_score(action, state[0])
            agent.categories_used.append(action)
            reward = score
            total_score += reward
            next_roll = roll_dice()
            next_state = (next_roll, agent.categories_used)
            agent.update(state, action, reward, next_state)
            state = next_state
        scores.append(total_score)
        
        # Optionally print progress
        if (game + 1) % 1000 == 0:
            print(f"Completed {game + 1} games")
    
    return scores