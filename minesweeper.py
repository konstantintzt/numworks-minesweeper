import random
import ion
import kandinsky
import time

alive = True

offsets = [
    [0, 1],
    [0, -1],
    [1, 1],
    [1, 0],
    [1, -1],
    [-1, 1],
    [-1, 0],
    [-1, -1]
]

colors = {
    "unknown": (255,255,255),
    "mine_number": (102,102,102),
    "known_mine": (255,0,0),
    "selected": (179,179,179)
}

def draw(current_x, current_y, game_map, mine_map, neighbor_map):
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            current_cell = game_map[y][x]

            y_coord = y*20 + 1
            x_coord = x*20

            col = (255,255,255)

            if y == current_y and x == current_x:
                col = colors["selected"]
            elif current_cell == 9:
                col = colors["unknown"]
            elif 0 <= current_cell <= 8:
                col = colors["mine_number"]
            else:
                col = colors["known_mine"]
            
            kandinsky.fill_rect(x_coord, y_coord, 20, 20, col)

            if 0 <= current_cell <= 8:
                kandinsky.draw_string(str(current_cell), x_coord+5, y_coord+1, (0,0,0), col)

def mark_mine(x,y,game_map):

    if game_map[y][x] > 8:
        game_map[y][x] = 10

def main():

    # Game settings
    x_size = 16
    y_size = 11
    n_mines = 24 # Modify this to change difficulty!

    # Current player position
    curr_x = 0
    curr_y = 0
    
    mine_map, neighbor_map, game_map = generate_map(x_size, y_size, n_mines)

    draw(curr_x, curr_y, game_map, mine_map, neighbor_map)

    visited = [[0]*x_size for y in range(y_size)]

    while alive:

        clicked = False

        if ion.keydown(ion.KEY_OK):
            click_cell(curr_x, curr_y, mine_map, neighbor_map, game_map, visited)
            clicked = True
        elif ion.keydown(ion.KEY_BACKSPACE):
            mark_mine(curr_x, curr_y, game_map)
            clicked = True
        elif ion.keydown(ion.KEY_DOWN):
            if curr_y < y_size-1:
                curr_y += 1
                clicked = True
        elif ion.keydown(ion.KEY_UP):
            if curr_y > 0:
                curr_y -= 1
                clicked = True
        elif ion.keydown(ion.KEY_RIGHT):
            if curr_x < x_size - 1:
                curr_x += 1
                clicked = True
        elif ion.keydown(ion.KEY_LEFT):
            if curr_x > 0:
                curr_x -= 1
                clicked = True

        if clicked:
            draw(curr_x, curr_y, game_map, mine_map, neighbor_map)
            visited = [[0]*x_size for y in range(y_size)]
        time.sleep(0.025)
    

def generate_map(x_size, y_size, n_mines):
    mine_map = []
    neighbor_map = []
    game_map = []

    mine_map = [[0]*x_size for y in range(y_size)]
    game_map = [[9]*x_size for y in range(y_size)]

    for i in range(n_mines):
        x_coord = random.randint(0, x_size-1)
        y_coord = random.randint(0, y_size-1)
        mine_map[y_coord][x_coord] = 1

    for y in range(y_size):
        neighbor_map.append([])
        for x in range(x_size):
            neighbor_map[y].append(get_mines(x, y, mine_map))

    return mine_map, neighbor_map, game_map

def display(table):
    for l in table:
        print(*l)

def is_inside_field(x, y, width, length):
    if x < 0 or y < 0 or x >= width or y >= length:
        return False
    else:
        return True

def get_mines(x, y, mine_map):

    count = 0

    for [x_offset, y_offset] in offsets:
        if is_inside_field(x+x_offset, y+y_offset, len(mine_map[0]), len(mine_map)):
            count += mine_map[y+y_offset][x+x_offset]

    return count

def gameover():
    alive = False
    kandinsky.fill_rect(0, 0, 320, 222, (255,0,0))
    kandinsky.draw_string("You hit a mine! Game over!", 0, 110, (0,0,0), (255,0,0))
    exit()

def wongame():
    alive = False
    kandinsky.fill_rect(0, 0, 320, 222, (0,255,0))
    kandinsky.draw_string("You won! GG!", 0, 110, (0,0,0), (0,255,0))
    exit()

def click_cell(x, y, mine_map, neighbor_map, game_map, visited):

    if mine_map[y][x] == 1:
        gameover()
    elif neighbor_map[y][x] == 0:
        game_map[y][x] = 0
        clear_blank_patch(y, x, mine_map, neighbor_map, game_map, visited)
    else:
        game_map[y][x] = neighbor_map[y][x]

    for y_coord in range(len(mine_map)):
        for x_coord in range(len(mine_map[0])):
            if mine_map[y_coord][x_coord] == 0 and (game_map[y_coord][x_coord] == 9 or game_map[y_coord][x_coord] == 8):
                return

    wongame()

def clear_blank_patch(y, x, mine_map, neighbor_map, game_map,visited):

    stack = []
    stack.append([y,x])

    while len(stack):
        [y_coord, x_coord,] = stack[-1]
        stack.pop()

        if visited[y_coord][x_coord] == 1 or mine_map[y_coord][x_coord] == 1:
            continue

        visited[y_coord][x_coord] = 1
        game_map[y_coord][x_coord] = neighbor_map[y_coord][x_coord]

        if neighbor_map[y_coord][x_coord] != 0:
            continue

        for [x_offset, y_offset] in offsets:
            if is_inside_field(x_coord+x_offset, y_coord+y_offset, len(mine_map[0]), len(mine_map)) and not visited[y_coord+y_offset][x_coord+x_offset]:
                stack.append([y_coord+y_offset, x_coord+x_offset])

main()