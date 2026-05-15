import random
import math


class DynamicObstacle:
    """
    Рухома перешкода.
    type:
    - "interceptor" — летить на випередження по маршруту
    - "hunter" — просто переслідує БПЛА
    """

    def __init__(self, row, col, obstacle_type="hunter"):
        self.row = row
        self.col = col
        self.type = obstacle_type
        self.angle = 0

    def position(self):
        return self.row, self.col

    def update_angle(self, old_row, old_col):
        dx = self.col - old_col
        dy = self.row - old_row

        if dx != 0 or dy != 0:
            self.angle = math.degrees(math.atan2(dy, dx))

    def move_to_target(self, grid, target_node):
        if target_node is None:
            return

        moves = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        random.shuffle(moves)

        best_move = None
        best_distance = abs(self.row - target_node.row) + abs(self.col - target_node.col)

        for dr, dc in moves:
            new_row = self.row + dr
            new_col = self.col + dc

            node = grid.get_node(new_row, new_col)

            if not node:
                continue

            if node.is_start or node.is_end or node.is_obstacle:
                continue

            distance = abs(new_row - target_node.row) + abs(new_col - target_node.col)

            if distance < best_distance:
                best_distance = distance
                best_move = (new_row, new_col)

        if best_move:
            old_row = self.row
            old_col = self.col

            self.row, self.col = best_move
            self.update_angle(old_row, old_col)

    def move_hunter(self, grid, uav_node):
        """
        Просте переслідування основного БПЛА.
        """
        self.move_to_target(grid, uav_node)

    def move_interceptor(self, grid, path, move_index, uav_node):
        """
        Розумніша логіка:
        дрон не летить прямо за БПЛА,
        а вибирає точку попереду на маршруті.
        """
        if not path or not uav_node:
            self.move_hunter(grid, uav_node)
            return

        prediction_index = min(move_index + 8, len(path) - 1)
        predicted_target = path[prediction_index]

        self.move_to_target(grid, predicted_target)