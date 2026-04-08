# comp6721

🚀 Intelligent Path-Finding Visualizer
Interactive AI Search Algorithm Simulator

The Intelligent Path-Finding Visualizer is an interactive desktop application that demonstrates how different AI search algorithms navigate grid-based environments.

It allows users to visually explore algorithm behavior in real time, showing:

Exploration patterns
Decision-making process
Performance differences between algorithms
🧠 Algorithms Implemented
Breadth-First Search (BFS)
Guarantees the shortest path but explores many nodes
Depth-First Search (DFS)
Faster in some cases but may produce very long, non-optimal paths
Greedy Best-First Search
Uses heuristics for speed but does not guarantee optimal results
A* Search
Combines optimality and efficiency — the best overall performer
🎯 Features
Interactive grid editor for custom maze creation
Real-time step-by-step visualization
Performance comparison between algorithms
Simple and intuitive controls

Users can:

Set Start (S) and Goal (G) positions
Draw walls using W
Erase cells using E
Run algorithms and instantly see results
🎨 Visualization Legend
Element	Color
Start Node	Green 🟩
Goal Node	Red 🟥
Wall	Black ⬛
Frontier	Blue 🔵
Visited Nodes	Teal 🟦
Final Path	Yellow 🟨
📊 Performance Metrics

After each run, the system displays:

Nodes Expanded
Path Length
Execution Time

This makes it easy to compare algorithm efficiency and behavior.

🛠️ Tech Stack
Python 3.12
Pygame

The entire project is implemented in a single file:
main.py

⚙️ Installation & Setup
# Clone the repository
git clone https://github.com/gmsv07/pathfinding-visualizer.git

🔗 GitHub Repository: https://github.com/gmsv07/pathfinding-visualizer

# Navigate to project folder
cd pathfinding-visualizer

# Install dependencies
pip install pygame

# Run the project
python main.py

⚠️ Important: Use Python 3.12
(Pygame is not compatible with Python 3.14)

🎮 Controls
Key	Action
S	Set Start
G	Set Goal
W	Draw Walls
E	Erase
R	Run Algorithm
C	Clear Path
X	Reset Grid
📈 Results Summary
Algorithm	Optimal	Speed	Nodes Expanded
BFS	Yes	Slow	Very High
DFS	No	Medium	Moderate
Greedy	No	Very Fast	Very Low
A*	Yes	Fast	Low

👉 A* provides the best balance between speed and accuracy.

🏁 Conclusion

This project highlights the strengths and weaknesses of classic search algorithms:

BFS → reliable but expensive
DFS → unpredictable and inefficient
Greedy → fast but not always correct
A* → optimal and efficient

The visualization makes these differences intuitive and easy to understand.

📚 References
https://www.pygame.org/docs/
https://docs.python.org/3.12/
👨‍💻 Authors
Siva Sankar Reddy Veluri
Gundavarapu Mounika Satya Vani
