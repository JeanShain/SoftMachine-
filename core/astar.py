import heapq
import math


def heuristic(a, b):
    return math.sqrt((a.row - b.row) ** 2 + (a.col - b.col) ** 2)


def reconstruct_path(came_from, current):
    path = [current]

    while current in came_from:
        current = came_from[current]
        path.append(current)

    path.reverse()
    return path


def get_safety_penalty(grid, node, safety_radius=4):
    """
    Додає штраф, якщо клітинка знаходиться близько до перешкоди.
    Чим ближче до перешкоди — тим більший штраф.
    """
    penalty = 0

    for dr in range(-safety_radius, safety_radius + 1):
        for dc in range(-safety_radius, safety_radius + 1):
            nearby = grid.get_node(node.row + dr, node.col + dc)

            if nearby and nearby.is_obstacle:
                distance = math.sqrt(dr ** 2 + dc ** 2)

                if distance == 0:
                    penalty += 100
                elif distance <= safety_radius:
                    penalty += (safety_radius - distance + 1) * 3

    return penalty


def astar_search(grid, start, end, safety_radius=4):
    counter = 0
    open_set = []
    heapq.heappush(open_set, (0, counter, start))

    came_from = {}
    g_score = {start: 0}
    open_set_hash = {start}

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            return reconstruct_path(came_from, end)

        current.is_closed = True

        for neighbor in grid.get_neighbors(current):
            move_cost = heuristic(current, neighbor)
            safety_penalty = get_safety_penalty(grid, neighbor, safety_radius)

            temp_g_score = g_score[current] + move_cost + safety_penalty

            if temp_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score

                f_score = temp_g_score + heuristic(neighbor, end)

                if neighbor not in open_set_hash:
                    counter += 1
                    heapq.heappush(open_set, (f_score, counter, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.is_open = True

    return []