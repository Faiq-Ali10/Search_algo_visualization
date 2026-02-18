import pygame
import random
import collections
import heapq
import time

# --- Configuration ---
WIDTH, HEIGHT = 600, 750
GRID_SIZE = 40          # BIGGER CELLS -> SMALLER GRID (approx 15x15)
LEGEND_HEIGHT = 150
ROWS = (HEIGHT - LEGEND_HEIGHT) // GRID_SIZE
COLS = WIDTH // GRID_SIZE
DELAY = 0.05            # Animation speed

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)        # Wall
GREEN = (0, 255, 0)      # Start
RED = (255, 0, 0)        # Target
BLUE = (0, 0, 255)       # Path
CYAN = (0, 255, 255)     # Frontier (Start side)
ORANGE = (255, 165, 0)   # Frontier (Target side / Bi-directional)
YELLOW = (255, 255, 0)   # Explored
GREY = (200, 200, 200)   # Grid Lines

class Node:
    def __init__(self, r, c):
        self.r, self.c = r, c
        self.is_wall = False
        self.parent = None
        self.cost = float('inf')
        self.state = 'neutral' 

    def reset(self):
        self.parent = None
        self.cost = float('inf')
        self.state = 'neutral'
        self.is_wall = False

    def __lt__(self, other):
        return self.cost < other.cost

def get_neighbors(node, grid):
    neighbors = []
    # Clockwise: Up, Right, Down, Down-Right, Left, Up-Left, Up-Right, Down-Left
    directions = [
        (-1, 0), (0, 1), (1, 0), (1, 1), 
        (0, -1), (-1, -1), (-1, 1), (1, -1)
    ]
    for dr, dc in directions:
        r, c = node.r + dr, node.c + dc
        if 0 <= r < ROWS and 0 <= c < COLS:
            if not grid[r][c].is_wall:
                cost = 1.4 if dr != 0 and dc != 0 else 1.0 
                neighbors.append((grid[r][c], cost))
    return neighbors

# --- 1. BFS ---
def bfs(draw, grid, start, target):
    queue = collections.deque([start])
    start.state = 'frontier'
    
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return

        curr = queue.popleft()
        if curr == target: return reconstruct_path(target, draw)

        curr.state = 'visited'

        for neighbor, cost in get_neighbors(curr, grid):
            if neighbor.state == 'neutral':
                neighbor.state = 'frontier'
                neighbor.parent = curr
                queue.append(neighbor)
        
        draw()
        time.sleep(DELAY)

# --- 2. DFS ---
def dfs(draw, grid, start, target):
    stack = [start]
    start.state = 'frontier'

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return

        curr = stack.pop()
        if curr == target: return reconstruct_path(target, draw)
        
        curr.state = 'visited'

        for neighbor, cost in get_neighbors(curr, grid):
            if neighbor.state == 'neutral':
                neighbor.state = 'frontier'
                neighbor.parent = curr
                stack.append(neighbor)
        
        draw()
        time.sleep(DELAY)

# --- 3. UCS ---
def ucs(draw, grid, start, target):
    count = 0
    pq = [] 
    heapq.heappush(pq, (0, count, start))
    start.cost = 0
    start.state = 'frontier'
    visited = set()

    while pq:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return

        cost, _, curr = heapq.heappop(pq)
        
        if curr in visited: continue
        visited.add(curr)
        curr.state = 'visited'

        if curr == target: return reconstruct_path(target, draw)

        for neighbor, move_cost in get_neighbors(curr, grid):
            new_cost = cost + move_cost
            if new_cost < neighbor.cost:
                neighbor.cost = new_cost
                neighbor.parent = curr
                neighbor.state = 'frontier'
                count += 1
                heapq.heappush(pq, (new_cost, count, neighbor))
        
        draw()
        time.sleep(DELAY)

# --- 4. DLS ---
def dls_search(draw, grid, curr, target, limit, depth):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); return True

    if curr == target: 
        reconstruct_path(target, draw)
        return True
    
    if depth >= limit: return False

    curr.state = 'visited'
    
    draw()
    time.sleep(DELAY)

    for neighbor, cost in get_neighbors(curr, grid):
        if neighbor.state == 'neutral':
            neighbor.parent = curr
            if dls_search(draw, grid, neighbor, target, limit, depth + 1):
                return True
            
    return False

def dls(draw, grid, start, target):
    limit = 30
    dls_search(draw, grid, start, target, limit, 0)

# --- 5. IDDFS ---
def iddfs(draw, grid, start, target):
    max_depth = 50
    
    for limit in range(1, max_depth + 1):
        # Reset grid state for new depth
        for r in range(ROWS):
            for c in range(COLS):
                if not grid[r][c].is_wall:
                    grid[r][c].state = 'neutral'
                    grid[r][c].parent = None
        
        if dls_search(draw, grid, start, target, limit, 0):
            return

# --- 6. Bidirectional ---
def bidirectional(draw, grid, start, target):
    start_q = collections.deque([start])
    end_q = collections.deque([target])
    
    start_visited = {start: None}
    end_visited = {target: None}
    
    start.state = 'frontier'
    target.state = 'frontier_bwd'

    while start_q and end_q:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return

        # Start Side
        curr_s = start_q.popleft()
        if curr_s in end_visited: return reconstruct_bi(curr_s, start_visited, end_visited, draw)
        curr_s.state = 'visited'
        for neighbor, cost in get_neighbors(curr_s, grid):
            if neighbor not in start_visited:
                start_visited[neighbor] = curr_s
                neighbor.state = 'frontier'
                start_q.append(neighbor)
                if neighbor in end_visited: return reconstruct_bi(neighbor, start_visited, end_visited, draw)

        # End Side
        curr_e = end_q.popleft()
        if curr_e in start_visited: return reconstruct_bi(curr_e, start_visited, end_visited, draw)
        curr_e.state = 'visited'
        for neighbor, cost in get_neighbors(curr_e, grid):
            if neighbor not in end_visited:
                end_visited[neighbor] = curr_e
                neighbor.state = 'frontier_bwd'
                end_q.append(neighbor)
                if neighbor in start_visited: return reconstruct_bi(neighbor, start_visited, end_visited, draw)
        
        draw()
        time.sleep(DELAY)

def reconstruct_path(curr, draw):
    while curr:
        curr.state = 'path'
        curr = curr.parent
        draw()

def reconstruct_bi(meet, start_v, end_v, draw):
    curr = meet
    while curr:
        curr.state = 'path'
        curr = start_v[curr]
        draw()
    curr = meet
    while curr:
        curr.state = 'path'
        curr = end_v[curr]
        draw()

# --- GUI ---
def draw_legend(win, font, algo_name):
    pygame.draw.rect(win, WHITE, (0, 0, WIDTH, LEGEND_HEIGHT))
    title = font.render(f"Algo: {algo_name}", True, BLACK)
    subtitle = font.render("Press SPACE to Start Next", True, BLACK)
    win.blit(title, (20, 10))
    win.blit(subtitle, (20, 35))

    keys = [
        (GREEN, "Start", 20, 60), (RED, "Target", 100, 60), (BLUE, "Path", 180, 60),
        (CYAN, "Frontier (S)", 260, 60), (ORANGE, "Frontier (T)", 400, 60),
        (YELLOW, "Visited", 20, 90), (BLACK, "Wall", 120, 90)
    ]
    for color, text, x, y in keys:
        pygame.draw.rect(win, color, (x, y+5, 15, 15))
        label = font.render(text, True, BLACK)
        win.blit(label, (x + 20, y+5))
    
    pygame.draw.line(win, BLACK, (0, LEGEND_HEIGHT), (WIDTH, LEGEND_HEIGHT), 2)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("GOOD PERFORMANCE TIME APP")
    font = pygame.font.SysFont('Arial', 18)
    
    grid = [[Node(r, c) for c in range(COLS)] for r in range(ROWS)]
    
    start = grid[2][2]
    target = grid[ROWS-3][COLS-3]

    algos = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("UCS", ucs),
        ("DLS (L=30)", dls),
        ("IDDFS", iddfs),
        ("Bidirectional", bidirectional)
    ]
    idx = 0

    def draw():
        draw_legend(win, font, algos[idx][0])
        for r in range(ROWS):
            for c in range(COLS):
                node = grid[r][c]
                rect = (c*GRID_SIZE, r*GRID_SIZE + LEGEND_HEIGHT, GRID_SIZE-1, GRID_SIZE-1)
                
                color = WHITE
                if node.is_wall: color = BLACK
                elif node == start: color = GREEN
                elif node == target: color = RED
                elif node.state == 'path': color = BLUE
                elif node.state == 'frontier': color = CYAN
                elif node.state == 'frontier_bwd': color = ORANGE
                elif node.state == 'visited': color = YELLOW
                
                pygame.draw.rect(win, color, rect)
                pygame.draw.rect(win, GREY, rect, 1)
        pygame.display.update()

    run = True
    while run:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start.reset(); target.reset()
                    for r in range(ROWS):
                        for c in range(COLS):
                            grid[r][c].reset()
                            
                    algos[idx][1](draw, grid, start, target)
                    idx = (idx + 1) % len(algos)
                    time.sleep(1)

    pygame.quit()

if __name__ == "__main__":
    main()