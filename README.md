<h1>YAMS: Reinforcement Learning Project</h1>

<h2>Objective</h2>
<p>The goal of the YAMS Reinforcement Learning (RL) project is to develop an agent capable of playing the Yahtzee game optimally using RL algorithms. The agent will aim to maximize its total score after playing 10 games, learning how to make the best decisions about which dice to keep and which to re-roll. The RL model will be evaluated on its ability to choose optimal actions based on the game’s state and its learning progress.</p>

<p>Each game of Yahtzee is divided into thirteen rounds. During each round, a player rolls five dice. The player can re-roll the dice up to two more times and may choose which specific dice to re-roll. After completing the rolls, the player must assign the final roll to one of the thirteen categories on their score-sheet. The score for each round is determined by how well the dice match the chosen category. Once a category is selected, it cannot be used again for the remainder of the game. The game ends when all categories are filled, and the player with the highest total score wins.</p>

<h3>Example of a Round</h3>
<p>For example, imagine a player rolls a 1, 2, 2, 3, and 5 on their first roll. The player decides to re-roll the 3 and 5, obtaining a 2 and 4. The player re-rolls the 4 again and gets another 2, resulting in a final roll of 1, 2, 2, 2, 2. The player then assigns this roll to the "Twos" category, where the score is the sum of all dice that show a 2. In this case, the score would be 2 + 2 + 2 + 2 = 8 points for that round.</p>
<div style="text-align: center;">
    <img alt="image" src="https://th.bing.com/th/id/R.50770cd1a8da1fa8bb6cf1661c0c1e1b?rik=QFV9KTnRCf%2buPA&riu=http%3a%2f%2fwww.neopoker.fr%2fwp-content%2fuploads%2f2013%2f02%2fGrille-de-Yams.jpg&ehk=ty1O63p0oIB92rX0KArFVCgsGVUYgyAq1WCReuNW2o4%3d&risl=&pid=ImgRaw&r=0" />
</div>



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


<h1>Results</h1>
<h2>1. Random Agent</h2>
<ul>
    <li><strong>Score max:</strong> 186</li>
    <li><strong>Score min:</strong> 82</li>
    <li><strong>Score moyen:</strong> 119.01</li>
</ul>
<img width="800" alt="image" src="https://github.com/user-attachments/assets/4e527744-0f5d-450f-a5ca-62ebcdd08616" />

<h2>2. Greedy Agents</h2>
<ul>
  <li><strong>Greedy Agent Level 1</strong>: It never re-rolls the dice after the first roll and chooses the action that immediately maximizes its score.</li>
  <li><strong>Greedy Agent Level 2</strong>: It can re-roll once and chooses the action that maximizes the expected score after one re-roll.</li>
  <li><strong>Greedy Agent Level 3</strong>: It can re-roll twice and chooses the action that maximizes the expected score after two re-rolls.</li>
</ul>
<div style="display: flex; justify-content: space-around;">
    <img alt="image" src="https://github.com/user-attachments/assets/4bf79806-199a-482b-9e8c-b1fa25f54ed4" style="width: 30%; height: 200px;" />
<img alt="image" src="https://github.com/user-attachments/assets/047a7fe4-5e04-4357-81fe-847755e2f8cc" style="width: 30%; height: 200px;" />
<img alt="image" src="https://github.com/user-attachments/assets/c1aed571-7312-4365-9b41-625faa5bf1be" style="width: 30%; height: 200px;" />
</div>

<h2>3. Q-learning and SARSA Agent</h2>
<ul>
    <li><strong>SARSA Update</strong>:<br>
        <code>Q(s, a) ← Q(s, a) + α [ r + γ Q(s', a') - Q(s, a) ]</code><br>
        where <em>a'</em> is the next action chosen by the policy in the next state <em>s'</em>.
        <img width="800" alt="image" src="https://github.com/user-attachments/assets/d73d0950-45b6-44fb-a36f-cf0faec7b748" />
    </li>
    <li><strong>Q-Learning Update</strong>:<br>
        <code>Q(s, a) ← Q(s, a) + α [ r + γ max<sub>a'</sub> Q(s', a') - Q(s, a) ]</code><br>
        Q-Learning uses the best possible Q value without considering the agent's current policy.
        <img width="800" alt="image" src="https://github.com/user-attachments/assets/5e202d38-31d4-4ca7-99a7-def6f3cdaf04" />
    </li>
</ul>



<h2>4. Perceptron Q-learning Agent</h2>
<p>Ref : https://web.stanford.edu/class/aa228/reports/2018/final75.pdf (Paper Reinforcement Learning for Solving Yahtzee)</p>
<img width="800" alt="image" src="https://github.com/user-attachments/assets/91e2d15d-bca7-44f2-97a9-3c348a476f0d" />

<h1>Conclusion</h2>
<ul>
  <li>Number of dice: 5</li>
  <li>Number of faces per die: 6</li>
  <li>Epsilon (exploration): 0.2</li>
  <li>Alpha (learning rate): 0.01</li>
  <li>Gamma (discount factor): 0.9</li>
  <li>Maximum number of turns per game: 7</li>
</ul>
<img width="800" alt="image" src="https://github.com/user-attachments/assets/16886e9e-5522-4b6f-9a0d-ff4236e9fdd1" />






