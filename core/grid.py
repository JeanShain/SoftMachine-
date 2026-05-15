from core.node import Node


class Grid:
    """
    Клас Grid відповідає за створення карти у вигляді сітки.
    Також він повертає сусідів клітинки для алгоритму A*.
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.nodes = self.create_grid()

    def create_grid(self):
        return [[Node(row, col) for col in range(self.cols)] for row in range(self.rows)]

    def is_inside(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get_node(self, row, col):
        if self.is_inside(row, col):
            return self.nodes[row][col]
        return None

    def get_neighbors(self, node):
        """
        Повертає сусідів клітинки.
        Рух дозволений у 8 напрямках:
        вгору, вниз, вліво, вправо та по діагоналі.
        """
        neighbors = []

        directions = [
            (-1, 0),  # вгору
            (1, 0),  # вниз
            (0, -1),  # вліво
            (0, 1),  # вправо
            (-1, -1),  # діагональ
            (-1, 1),
            (1, -1),
            (1, 1)
        ]

        for dr, dc in directions:
            neighbor = self.get_node(node.row + dr, node.col + dc)

            if neighbor and not neighbor.is_obstacle:
                neighbors.append(neighbor)

        return neighbors

    def clear_path_states(self):
        """
        Очищає візуальні сліди попереднього маршруту.
        """
        for row in self.nodes:
            for node in row:
                node.clear_path_state()