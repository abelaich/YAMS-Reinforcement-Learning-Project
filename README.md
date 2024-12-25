<h1>YAMS: Reinforcement Learning Project</h1>

<h2>Objective</h2>
<p>The goal of the YAMS Reinforcement Learning (RL) project is to develop an agent capable of playing the Yahtzee game optimally using RL algorithms. The agent will aim to maximize its total score after playing 10 games, learning how to make the best decisions about which dice to keep and which to re-roll. The RL model will be evaluated on its ability to choose optimal actions based on the game’s state and its learning progress.</p>

<p>Each game of Yahtzee is divided into thirteen rounds. During each round, a player rolls five dice. The player can re-roll the dice up to two more times and may choose which specific dice to re-roll. After completing the rolls, the player must assign the final roll to one of the thirteen categories on their score-sheet. The score for each round is determined by how well the dice match the chosen category. Once a category is selected, it cannot be used again for the remainder of the game. The game ends when all categories are filled, and the player with the highest total score wins.</p>

<h3>Example of a Round</h3>
<p>For example, imagine a player rolls a 1, 2, 2, 3, and 5 on their first roll. The player decides to re-roll the 3 and 5, obtaining a 2 and 4. The player re-rolls the 4 again and gets another 2, resulting in a final roll of 1, 2, 2, 2, 2. The player then assigns this roll to the "Twos" category, where the score is the sum of all dice that show a 2. In this case, the score would be 2 + 2 + 2 + 2 = 8 points for that round.</p>

<h2>Components</h2>

<h3>Performance Measure</h3>
<p>The agent’s objective is to maximize the total score after 10 games. The performance measures include:</p>
<ul>
    <li><strong>Total Score:</strong> The sum of dice values after 10 games.</li>
    <li><strong>Efficiency:</strong> The ability to make optimal decisions after each roll.</li>
    <li><strong>Number of Dice Kept:</strong> Indicates the strategy adopted by the agent.</li>
</ul>

<h3>Environment</h3>
<p>The environment consists of two parts: the full game environment and the turn environment.</p>

<h4>Game Environment</h4>
<p>The game environment defines the rules of the Yahtzee game, manages turns and episodes, and assigns rewards based on the actions taken.</p>
<p><strong>Main Attributes:</strong></p>
<ul>
    <li><code>self.dices, self.faces, self.turns</code>: Parameters of the game.</li>
    <li><code>self.S</code>: Describes the point categories in the game (sum of faces, three of a kind, pair, chance, etc.).</li>
</ul>
<p><strong>Key Methods:</strong></p>
<ul>
    <li><code>get_action</code>: Calculates the possible rewards for a given state.</li>
    <li><code>play_episode</code>: Simulates a full game episode, including dice rolls and selected actions.</li>
    <li><code>choose_action</code> and <code>choose_random_action</code>: Select actions either strategically (via Q-values) or randomly.</li>
</ul>

<h4>Turn Environment</h4>
<p>The turn environment models a single game round, managing the state of the dice, possible actions, and transitions between states.</p>
<p><strong>Main Attributes:</strong></p>
<ul>
    <li><code>self.dices, self.faces</code>: Number of dice and sides per die.</li>
    <li><code>self.Roll, self.Roll_P</code>: Possible dice states and their probabilities.</li>
    <li><code>self.S</code>: List of initial dice states.</li>
    <li><code>self.Aa</code>: List of all possible actions.</li>
</ul>
<p><strong>Key Methods:</strong></p>
<ul>
    <li><code>get_states</code>: Generates all possible dice states and their probabilities.</li>
    <li><code>get_actions_from_state</code>: Determines the possible actions for a given state.</li>
    <li><code>get_actions_list</code>: Generates a global list of all possible actions for all states.</li>
    <li><code>One_step_backward</code>: Updates state values and Q-values through a dynamic learning step.</li>
    <li><code>choose_best_action</code>: Selects the action with the highest Q-value for a given state.</li>
</ul>

<h3>Agents</h3>
<p>The project features several agents that employ different reinforcement learning techniques, including:</p>
<ul>
    <li><strong>Random Agent</strong>: Chooses actions randomly.</li>
    <li><strong>Greedy Agent</strong>: Selects the action with the highest immediate reward.</li>
    <li><strong>Monte Carlo Agent</strong>: Learns from complete episodes by averaging returns from different states.</li>
    <li><strong>Q-learning Agent</strong>: Uses Q-values to make decisions based on past experiences.</li>
    <li><strong>SARSA Agent</strong>: Similar to Q-learning but updates Q-values using the action taken in the next step.</li>
    <li><strong>Perceptron Q-learning Agent</strong>: Combines Q-learning with a perceptron model for function approximation.</li>
</ul>

<h2>Properties of the Environment</h2>
<table border="1" cellpadding="10">
    <tr>
        <th>Property</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><strong>Observability</strong></td>
        <td>The environment is fully observable. The agent can see the value of all dice after each roll.</td>
    </tr>
    <tr>
        <td><strong>Determinism</strong></td>
        <td>The environment is stochastic due to the random nature of dice rolls.</td>
    </tr>
    <tr>
        <td><strong>Dynamics</strong></td>
        <td>The environment is sequential, as decisions (such as which dice to keep or re-roll) affect future outcomes.</td>
    </tr>
    <tr>
        <td><strong>Time Complexity</strong></td>
        <td>The game is discrete, with each action occurring in defined steps (roll, keep, re-roll).</td>
    </tr>
    <tr>
        <td><strong>Autonomy</strong></td>
        <td>The agent is autonomous, making decisions based on its observations, without external interference.</td>
    </tr>
    <tr>
        <td><strong>Multi-agent</strong></td>
        <td>This is a single-agent environment, where only one player interacts with the environment.</td>
    </tr>
</table>
