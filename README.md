# 🤖 AI Pathfinder: Uninformed Search Visualization

A Python-based graphical simulation that visualizes fundamental AI search algorithms. This project demonstrates how different "blind" search strategies explore a grid environment to find a path from a **Start Point (S)** to a **Target Point (T)** while avoiding static walls and dynamic obstacles.

The application features a real-time GUI built with **Pygame**, showing the "thought process" of each algorithm as it expands its frontier and explores nodes.

## 🚀 Features

* **6 Search Algorithms:** Implements BFS, DFS, UCS, DLS, IDDFS, and Bidirectional Search.
* **Dynamic Environment:** Random obstacles spawn *during* the search to simulate a changing world.
* **Real-time Visualization:** Color-coded animations showing Open Set (Frontier), Closed Set (Visited), and the Final Path.
* **Clockwise Movement:** Strict node expansion order (Up, Right, Down, Diagonals, etc.).
* **Interactive Controls:** Simple keyboard controls to cycle through algorithms.

## 🛠️ Prerequisites

* **Python 3.10** or higher (Recommended: Python 3.11 or 3.12).
* **pip** (Python Package Installer).

## 📦 Installation

1.  **Clone the Repository** (or download the source code):
    ```bash
    git clone [https://github.com/YourUsername/AI-Pathfinder-Assignment.git](https://github.com/Faiq-Ali10/Search_algo_visualization.git)
    cd AI-Pathfinder-Assignment
    ```

2.  **Install Dependencies:**
    Install the required libraries using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

## 🎮 How to Run

1.  Open your terminal/command prompt in the project folder.
2.  Run the main script:
    ```bash
    python main.py
    ```

## 🕹️ Controls & Usage

* **Launch:** When the app opens, you will see the grid with a Start (Green) and Target (Red).
* **Start Search:** Press **SPACE BAR** to run the currently selected algorithm.
* **Next Algorithm:** Once a search finishes (or if you want to skip), press **SPACE BAR** again to clear the grid and switch to the next algorithm in the list.

### 🎨 Color Legend

* **🟩 Green:** Start Point
* **🟥 Red:** Target Point
* **🟦 Blue:** Final Path (The solution)
* **🟦 Cyan:** Frontier Nodes (Currently in Queue/Stack)
* **🟨 Yellow:** Explored/Visited Nodes
* **🟪 Purple:** Dynamic Obstacles (Spawned randomly)
* **⬛ Black:** Static Walls
* **🟧 Orange:** Backward Frontier (Bidirectional Search only)

## 🧠 Algorithms Implemented

1.  **Breadth-First Search (BFS):** Explores equally in all directions. Guarantees the shortest path in unweighted graphs.
2.  **Depth-First Search (DFS):** Explores as deep as possible along each branch before backtracking. Not optimal, often gets lost.
3.  **Uniform-Cost Search (UCS):** Explores paths with the lowest cost first. Handles diagonal movement costs ($\sqrt{2} \approx 1.4$) vs straight movement ($1$).
4.  **Depth-Limited Search (DLS):** A version of DFS that stops searching after a specific depth limit (e.g., 30 steps) to prevent infinite loops.
5.  **Iterative Deepening DFS (IDDFS):** Repeatedly runs DLS with increasing depth limits (1, 2, 3...). Combines BFS optimality with DFS memory efficiency.
6.  **Bidirectional Search:** Runs two simultaneous searches (one from Start, one from Target) and stops when they meet in the middle. extremely fast.

## 📂 Project Structure

```text
├── main.py            # Main source code containing all logic
├── README.md          # Project documentation
└── requirements.txt   # List of dependencies