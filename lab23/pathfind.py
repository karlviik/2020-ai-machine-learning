from queue import Queue, PriorityQueue

MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def is_within_bounds(graph, coord):
    return 0 <= coord[0] < len(graph) and 0 <= coord[1] < len(graph[0])


def get_neighbouring_coords(graph, coord):
    neighbours = []
    for move in MOVES:
        new_coord = (coord[0] + move[0], coord[1] + move[1])
        if is_within_bounds(graph, new_coord) and graph[new_coord[0]][new_coord[1]] is not '*':
            neighbours.append(new_coord)
    return neighbours


def construct_path(came_from: dict, goal: tuple):
    path = [goal]
    pos = goal
    while True:
        pos = came_from[pos]
        if pos:
            path.append(pos)
        else:
            break
    path.reverse()
    print(f"Length of path is {len(path)}")
    return path


def read_start_and_goal_from_map(lines):
    start_col = -1
    start_row = -1
    end_col = -1
    end_row = -1
    for i, line in enumerate(lines):
        if line.find("s") > -1:
            start_col = line.find("s")
            start_row = i
        if line.find("D") > -1:
            end_col = line.find("D")
            end_row = i
    return (start_row, start_col), (end_row, end_col), lines


def read_map_from_file(name):
    with open(name) as f:
        lines = [l.strip() for l in f.readlines() if len(l) > 1]
    return read_start_and_goal_from_map(lines)


def breadth_first_search(lava_map_tuple):
    # not using pre-found end coordinate here
    start = lava_map_tuple[0]
    graph = lava_map_tuple[2]

    frontier = Queue()
    frontier.put(start)

    came_from = {start: None}

    goal = ()
    iteration_counter = 0
    while not frontier.empty():
        iteration_counter += 1
        current = frontier.get()
        for next_coord in get_neighbouring_coords(graph, current):
            if next_coord not in came_from:
                frontier.put(next_coord)
                came_from[next_coord] = current
                if graph[next_coord[0]][next_coord[1]] == "D":
                    goal = next_coord
                    break
        else:
            continue
        break
    print(f"Breath first search made {iteration_counter} cycles.")
    return construct_path(came_from, goal)


def greedy_search(lava_map_tuple):

    def h(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    start = lava_map_tuple[0]
    goal = lava_map_tuple[1]
    graph = lava_map_tuple[2]

    frontier = PriorityQueue()
    frontier.put((0, start))

    came_from = {start: None}

    iteration_counter = 0
    while not frontier.empty():
        iteration_counter += 1
        _, current = frontier.get()
        for next_coord in get_neighbouring_coords(graph, current):
            if next_coord not in came_from:
                priority = h(next_coord, goal)
                frontier.put((priority, next_coord))
                came_from[next_coord] = current
                if graph[next_coord[0]][next_coord[1]] == "D":
                    goal = next_coord
                    break
        else:
            continue
        break
    print(f"Greedy search made {iteration_counter} cycles.")
    return construct_path(came_from, goal)


def a_star_search(lava_map_tuple):

    def h(cur, end):
        return abs(cur[0] - end[0]) + abs(cur[1] - end[1])

    start = lava_map_tuple[0]
    goal = lava_map_tuple[1]
    graph = lava_map_tuple[2]

    frontier = PriorityQueue()
    frontier.put((0, start))

    came_from = {start: None}

    cost_so_far = {start: 0}

    iteration_counter = 0
    while not frontier.empty():
        iteration_counter += 1
        _, current = frontier.get()
        new_cost = cost_so_far[current] + 1
        for next_coord in get_neighbouring_coords(graph, current):
            if next_coord not in cost_so_far or new_cost < cost_so_far[next_coord]:
                cost_so_far[next_coord] = new_cost
                priority = new_cost + h(next_coord, goal)
                frontier.put((priority, next_coord))
                came_from[next_coord] = current
                if graph[next_coord[0]][next_coord[1]] == "D":
                    goal = next_coord
                    break
        else:
            continue
        break
    print(f"A* search made {iteration_counter} cycles.")
    return construct_path(came_from, goal)



lava_map1 = [
    "      **               **      ",
    "     ***     D        ***      ",
    "     ***                       ",
    "                      *****    ",
    "           ****      ********  ",
    "           ***          *******",
    " **                      ******",
    "*****             ****     *** ",
    "*****              **          ",
    "***                            ",
    "              **         ******",
    "**            ***       *******",
    "***                      ***** ",
    "                               ",
    "                s              ",
]
lava_map2 = [
    "     **********************    ",
    "   *******   D    **********   ",
    "   *******                     ",
    " ****************    **********",
    "***********          ********  ",
    "            *******************",
    " ********    ******************",
    "********                   ****",
    "*****       ************       ",
    "***               *********    ",
    "*      ******      ************",
    "*****************       *******",
    "***      ****            ***** ",
    "                               ",
    "                s              ",
]
maps = [
    read_start_and_goal_from_map(lava_map1),
    read_start_and_goal_from_map(lava_map2),
    read_map_from_file("cave300x300"),
    read_map_from_file("cave600x600"),
    read_map_from_file("cave900x900")
]

for map in maps:
    print(f"\n\nMap size: {len(map[2])}x{len(map[2][0])}\n")
    breadth_first_search(map)
    print()
    greedy_search(map)
    print()
    a_star_search(map)
# cur_map = lava_map2
# [print(row) for row in cur_map]
# moves = greedy_search(maps[1])
# for move in moves:
#     cur_map[move[0]] = cur_map[move[0]][:move[1]] + 'O' + cur_map[move[0]][move[1] + 1:]
# [print(row) for row in cur_map]
