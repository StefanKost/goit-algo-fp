# goit-algo-fp
Algorithms and Data Structures Final Project

## Task 1 (Singly Linked List)
```bash
python task1_linked_list.py  
```

## Task 2 (Pythagoras Tree)
```bash
python task2_pythagoras_tree.py
```
### Result

![pythagoras_tree](./assets/pythagoras_tree.png)


## Task 3 (Dijkstra algorithm)
Create virtual env and install packages:
```bash
# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
pip install -r requirements.txt
```
Run command and choose path:
```
python task3_dijkstra_algorithm.py
```

### Result
![dijkstra_algorithm](./assets/dijkstra_algorithm.png)

## Task 4 (Visualise heap tree)
```bash
python task4_heap_visualisation.py
```

### Result
![heap_tree](./assets/heap_tree.png)

## Task 5 (Visualise tree traversal)
```bash
python task5_tree_traversal.py
```

### Result
![dfs_travelsal](./assets/dfs_traversal.png)
![bfs_travelsal](./assets/bfs_travelsal.png)

## Task 6 (Food selection)

| Algorithm           | Items                            | Calories | Cost |
|---------------------|----------------------------------|----------|------|
| Greedy              | cola, potato, pepsi, hot-dog     | 870      | 80   |
| Dynamic Programming | potato, cola, hot-dog, hamburger | 1020     | 110  |

**Comparison:**

| Aspect           | Greedy          | Dynamic Programming | 
|------------------|-----------------|---------------------|
| Time Complexity  | O(n log n)      | O(n × W)            |
| Space Complexity | O(n)            | O(n × W)            |
| Accuracy         | ~90% of optimal | 100%                |
| Result Quality   | Near-optimal    | Always optimal      |


**Recommended use:**
- **Greedy:** Suitable for large datasets, real-time applications, or when an approximate solution is sufficient.
- **Dynamic Programming:** Best for smaller datasets where the exact optimal solution is required.