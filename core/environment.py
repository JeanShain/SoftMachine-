import random


class Environment:
    """
    Клас Environment відповідає за зміну середовища.
    Тут ми додаємо статичні перешкоди саме на майбутній частині маршруту.
    """

    def __init__(self, grid):
        self.grid = grid

    def add_obstacle_cluster_on_path(self, path, current_index, start_node, end_node, uav_node):
        """
        Додає групу перешкод попереду БПЛА на його маршруті.
        Це імітує зміну середовища під час польоту.
        """
        if not path:
            return []

        future_path = path[current_index + 3: current_index + 10]

        available_nodes = []

        for node in future_path:
            if (
                node
                and not node.is_obstacle
                and node != start_node
                and node != end_node
                and node != uav_node
            ):
                available_nodes.append(node)

        if not available_nodes:
            return []

        main_obstacle = random.choice(available_nodes)
        main_obstacle.is_obstacle = True

        created_obstacles = [main_obstacle]

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)

        for dr, dc in directions[:2]:
            neighbor = self.grid.get_node(main_obstacle.row + dr, main_obstacle.col + dc)

            if (
                neighbor
                and not neighbor.is_obstacle
                and neighbor != start_node
                and neighbor != end_node
                and neighbor != uav_node
            ):
                neighbor.is_obstacle = True
                created_obstacles.append(neighbor)

        return created_obstacles