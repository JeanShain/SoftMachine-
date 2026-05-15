class Node:
    """
    Клас Node описує одну клітинку карти.
    Кожна клітинка може бути стартом, фінішем, перешкодою або частиною маршруту.
    """

    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.is_start = False
        self.is_end = False
        self.is_obstacle = False
        self.is_path = False
        self.is_open = False
        self.is_closed = False

    def position(self):
        return self.row, self.col

    def reset(self):
        """
        Повністю очищає стан клітинки.
        """
        self.is_start = False
        self.is_end = False
        self.is_obstacle = False
        self.is_path = False
        self.is_open = False
        self.is_closed = False

    def clear_path_state(self):
        """
        Очищає тільки службові позначки алгоритму A*.
        Старт, фініш і перешкоди залишаються.
        """
        self.is_path = False
        self.is_open = False
        self.is_closed = False