import pygame
import sys
import time
from collections import deque
import heapq

# window & grid configuration
GRID_SIZE   = 620          # square grid
PANEL_H     = 120          # panel height below the grid
WIDTH       = GRID_SIZE
HEIGHT      = GRID_SIZE + PANEL_H
ROWS, COLS  = 20, 20
CELL        = GRID_SIZE // COLS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")
font  = pygame.font.SysFont("Arial", 13)
font2 = pygame.font.SysFont("Arial", 12)

# colours 
WHITE  = (255, 255, 255)
BLACK  = (30,  30,  30)
GRAY   = (200, 200, 200)
DGRAY  = (90,  90,  100)
GREEN  = (50,  200, 100)
RED    = (220, 60,  60)
BLUE   = (60,  130, 220)
YELLOW = (250, 210, 50)
ORANGE = (240, 140, 40)
TEAL   = (60,  200, 190)
BG     = (240, 240, 245)
PANEL  = (45,  45,  55)

ALGO_NAMES = ["BFS", "DFS", "Greedy", "A*"]

# grid state 
cells     = [["empty"] * COLS for _ in range(ROWS)]
start     = None
goal      = None
metrics   = {}
algo_idx  = 0
draw_mode = 0
mouse_held = False

# helper functions
def cell_color(state):
    return {"empty": WHITE, "wall": BLACK, "visited": TEAL,
            "frontier": BLUE, "path": YELLOW,
            "start": GREEN,  "goal": RED}.get(state, WHITE)

def reset_all():
    global start, goal, cells, metrics
    cells   = [["empty"] * COLS for _ in range(ROWS)]
    start   = None
    goal    = None
    metrics = {}

def clear_path():
    global metrics
    for r in range(ROWS):
        for c in range(COLS):
            if cells[r][c] in ("visited", "frontier", "path"):
                cells[r][c] = "empty"
    if start:
        cells[start[0]][start[1]] = "start"
    if goal:
        cells[goal[0]][goal[1]] = "goal"
    metrics = {}

def get_neighbors(r, c):
    out = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and cells[nr][nc] != "wall":
            out.append((nr, nc))
    return out

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def mark_visited(node):
    r, c = node
    if cells[r][c] in ("empty", "frontier"):
        cells[r][c] = "visited"

def mark_frontier(node):
    r, c = node
    if cells[r][c] == "empty":
        cells[r][c] = "frontier"

def reconstruct(came_from, node):
    length = 0
    while node in came_from:
        node = came_from[node]
        if node != start:
            cells[node[0]][node[1]] = "path"
        length += 1
    return length

# draw 
BTN_W = 68
BTN_H = 28
GAP   = 6
by1   = GRID_SIZE + 8

def draw():
    screen.fill(BG)

    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*CELL, r*CELL, CELL, CELL)
            pygame.draw.rect(screen, cell_color(cells[r][c]), rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

    pygame.draw.rect(screen, PANEL, (0, GRID_SIZE, WIDTH, PANEL_H))

    # row 1 - algo + action buttons
    for i, name in enumerate(ALGO_NAMES):
        bx = 6 + i*(BTN_W+GAP)
        col = ORANGE if i == algo_idx else DGRAY
        pygame.draw.rect(screen, col, (bx, by1, BTN_W, BTN_H), border_radius=5)
        lbl = font.render(name, True, WHITE)
        screen.blit(lbl, (bx + BTN_W//2 - lbl.get_width()//2, by1 + 7))

    for i, name in enumerate(["Run", "Clear", "Reset"]):
        bx = 6 + (4+i)*(BTN_W+GAP)
        pygame.draw.rect(screen, DGRAY, (bx, by1, BTN_W, BTN_H), border_radius=5)
        lbl = font.render(name, True, WHITE)
        screen.blit(lbl, (bx + BTN_W//2 - lbl.get_width()//2, by1 + 7))

    # row 2 - mode indicators or instructions
    MODE_W = 140
    by2    = GRID_SIZE + 44
    modes  = ["S: Set Start", "G: Set Goal", "W: Draw Wall", "E: Erase"]
    for i, m in enumerate(modes):
        bx     = 6 + i*(MODE_W+6)
        border = ORANGE if i == draw_mode else DGRAY
        pygame.draw.rect(screen, border, (bx, by2, MODE_W, 22), 2, border_radius=4)
        lbl = font2.render(m, True, WHITE)
        screen.blit(lbl, (bx+6, by2+4))

    # row 3: metrics
    if metrics:
        by3   = GRID_SIZE + 74
        texts = [
            f"Algo: {ALGO_NAMES[algo_idx]}",
            f"Expanded: {metrics['expanded']}",
            f"Path len: {metrics['path_len']}",
            f"Time: {metrics['time']:.4f}s",
        ]
        for i, t in enumerate(texts):
            lbl = font2.render(t, True, WHITE)
            screen.blit(lbl, (6 + i*152, by3))

    pygame.display.flip()

def step():
    draw()
    pygame.time.delay(20)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); sys.exit()

# algorithms
def run_bfs():
    clear_path()
    if not start or not goal: return
    queue = deque([start])
    visited = {start}
    came_from = {}
    expanded  = 0
    t0 = time.time()
    found = False
    while queue:
        node = queue.popleft()
        expanded += 1
        if node == goal: found = True; break
        for nb in get_neighbors(*node):
            if nb not in visited:
                visited.add(nb); came_from[nb] = node; mark_frontier(nb); queue.append(nb)
        mark_visited(node); step()
    path_len = reconstruct(came_from, goal) if found else 0
    metrics.update(expanded=expanded, path_len=path_len, time=time.time()-t0)
    draw()

def run_dfs():
    clear_path()
    if not start or not goal: return
    stack = [start]
    visited = set()
    came_from = {}
    expanded = 0
    t0 = time.time()
    found = False
    while stack:
        node = stack.pop()
        if node in visited: continue
        visited.add(node); expanded += 1
        if node == goal: found = True; break
        mark_visited(node)
        for nb in get_neighbors(*node):
            if nb not in visited:
                came_from[nb] = node; mark_frontier(nb); stack.append(nb)
        step()
    path_len = reconstruct(came_from, goal) if found else 0
    metrics.update(expanded=expanded, path_len=path_len, time=time.time()-t0)
    draw()

def run_greedy():
    clear_path()
    if not start or not goal: return
    heap = [(heuristic(start, goal), start)]
    visited = set()
    came_from = {}
    expanded  = 0
    t0 = time.time()
    found = False
    while heap:
        _, node = heapq.heappop(heap)
        if node in visited: continue
        visited.add(node); expanded += 1
        if node == goal: found = True; break
        for nb in get_neighbors(*node):
            if nb not in visited:
                came_from[nb] = node; mark_frontier(nb)
                heapq.heappush(heap, (heuristic(nb, goal), nb))
        mark_visited(node); step()
    path_len = reconstruct(came_from, goal) if found else 0
    metrics.update(expanded=expanded, path_len=path_len, time=time.time()-t0)
    draw()

def run_astar():
    clear_path()
    if not start or not goal: return
    heap = [(heuristic(start, goal), 0, start)]
    visited = set()
    came_from = {}
    g_score = {start: 0}
    expanded = 0
    t0 = time.time()
    found = False
    while heap:
        f, g, node = heapq.heappop(heap)
        if node in visited: continue
        visited.add(node); expanded += 1
        if node == goal: found = True; break
        for nb in get_neighbors(*node):
            ng = g + 1
            if nb not in g_score or ng < g_score[nb]:
                g_score[nb] = ng; came_from[nb] = node; mark_frontier(nb)
                heapq.heappush(heap, (ng + heuristic(nb, goal), ng, nb))
        mark_visited(node); step()
    path_len = reconstruct(came_from, goal) if found else 0
    metrics.update(expanded=expanded, path_len=path_len, time=time.time()-t0)
    draw()

RUNNERS = [run_bfs, run_dfs, run_greedy, run_astar]

def click_panel(mx, my):
    global algo_idx
    for i in range(4):
        bx = 6 + i*(BTN_W+GAP)
        if bx <= mx <= bx+BTN_W and by1 <= my <= by1+BTN_H:
            algo_idx = i; return
    for i, action in enumerate(["run","clear","reset"]):
        bx = 6 + (4+i)*(BTN_W+GAP)
        if bx <= mx <= bx+BTN_W and by1 <= my <= by1+BTN_H:
            if action == "run":     RUNNERS[algo_idx]()
            elif action == "clear": clear_path()
            elif action == "reset": reset_all()
            return

# main loop
def main():
    global start, goal, algo_idx, draw_mode, mouse_held

    clock = pygame.time.Clock()
    while True:
        draw()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if ev.type == pygame.KEYDOWN:
                if   ev.key == pygame.K_s: draw_mode = 0
                elif ev.key == pygame.K_g: draw_mode = 1
                elif ev.key == pygame.K_w: draw_mode = 2
                elif ev.key == pygame.K_e: draw_mode = 3
                elif ev.key == pygame.K_r: RUNNERS[algo_idx]()
                elif ev.key == pygame.K_c: clear_path()
                elif ev.key == pygame.K_x: reset_all()

            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_held = True
                mx, my = ev.pos
                if my >= GRID_SIZE:
                    click_panel(mx, my)
                else:
                    r, c = my // CELL, mx // CELL
                    if draw_mode == 0:
                        if start: cells[start[0]][start[1]] = "empty"
                        start = (r,c); cells[r][c] = "start"
                    elif draw_mode == 1:
                        if goal: cells[goal[0]][goal[1]] = "empty"
                        goal = (r,c); cells[r][c] = "goal"
                    elif draw_mode == 2:
                        if (r,c) != start and (r,c) != goal:
                            cells[r][c] = "wall"
                    elif draw_mode == 3:
                        cells[r][c] = "empty"

            if ev.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

            if ev.type == pygame.MOUSEMOTION and mouse_held:
                mx, my = ev.pos
                if my < GRID_SIZE:
                    r, c = my // CELL, mx // CELL
                    if 0 <= r < ROWS and 0 <= c < COLS:
                        if draw_mode == 2 and (r,c) != start and (r,c) != goal:
                            cells[r][c] = "wall"
                        elif draw_mode == 3:
                            cells[r][c] = "empty"

if __name__ == "__main__":
    main()