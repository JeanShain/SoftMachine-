#     self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#     pygame.display.set_caption("SoftMashine")
#
#     self.clock = pygame.time.Clock()
#     self.running = True
#
#     # карта та середовище
#     self.grid = Grid(ROWS, COLS)
#     self.environment = Environment(self.grid)
#
#     # основні точки
#     self.start_node = None
#     self.end_node = None
#     self.uav_node = None
#
#     # маршрут і рух
#     self.path = []
#     self.move_index = 0
#     self.is_moving = False
#
#     # хвіст і поворот основного дрона
#     self.trail = []
#     self.uav_angle = 0
#
#     # перешкоди, які користувач поставив до старту
#     self.initial_obstacles = set()
#
#     # усі динамічні дрони
#     self.dynamic_obstacles = []
#
#     # interceptor: виходять із міської зони і летять на випередження
#     self.max_interceptors = 4
#     self.interceptor_spawn_delay = 1800
#     self.last_interceptor_spawn_time = 0
#     self.interceptor_move_delay = 300
#     self.last_interceptor_move_time = 0
#
#     # hunter: з’являються випадково і переслідують основний дрон
#     self.max_hunters = 4
#     self.hunter_spawn_delay = 2600
#     self.last_hunter_spawn_time = 0
#     self.hunter_move_delay = 360
#     self.last_hunter_move_time = 0
#
#     # рух основного дрона
#     self.move_delay = 150
#     self.last_move_time = 0
#
#     # статичні перешкоди, які з’являються на маршруті
#     self.environment_change_delay = 1200
#     self.last_environment_change_time = 0
#
#     # перебудова маршруту
#     self.rebuild_delay = 500
#     self.last_rebuild_time = 0
#
#     # zoom
#     self.zoom = 1.0
#     self.camera_x = 0
#     self.camera_y = 0
#
#     # завантаження іконок і карти
#     self.assets = self.load_assets()
#     pygame.mouse.set_visible(False)
#
#     # --------------------------------------------------
#     # завантаження зображень
#     # --------------------------------------------------
#
#     def load_image(self, filename, size=None):
#         path = os.path.join(ASSETS_PATH, filename)
#         image = pygame.image.load(path).convert_alpha()
#
#         if size:
#             image = pygame.transform.smoothscale(image, size)
#
#         return image
#
#     def load_assets(self):
#         icon_size = (ICON_SIZE, ICON_SIZE)
#         uav_size = (UAV_SIZE, UAV_SIZE)
#
#         return {
#             "map": self.load_image(MAP_IMAGE),
#             "cursor": self.load_image(CURSOR_IMAGE, (CURSOR_SIZE, CURSOR_SIZE)),
#             "start": self.load_image(UAV_HOME_IMAGE, icon_size),
#             "uav": self.load_image(UAV_IMAGE, uav_size),
#             "finish": self.load_image(FINISH_IMAGE, icon_size),
#             "static": self.load_image(STATIC_OBSTACLE_IMAGE, icon_size),
#             "interceptor": self.load_image(INTERCEPTOR_IMAGE, icon_size),
#             "hunter": self.load_image(HUNTER_IMAGE, icon_size),
#     }
#
#     # --------------------------------------------------
#     # камера / zoom
#     # --------------------------------------------------
#
#     def world_to_screen(self, x, y):
#         screen_x = (x - self.camera_x) * self.zoom
#         screen_y = (y - self.camera_y) * self.zoom
#         return int(screen_x), int(screen_y)
#
#     def screen_to_world(self, x, y):
#         world_x = x / self.zoom + self.camera_x
#         world_y = y / self.zoom + self.camera_y
#         return world_x, world_y
#
#     def get_clicked_position(self, mouse_pos):
#         x, y = mouse_pos
#         world_x, world_y = self.screen_to_world(x, y)
#
#         row = int(world_y // CELL_SIZE)
#         col = int(world_x // CELL_SIZE)
#
#         return row, col
#
# def handle_zoom(self, event):
#     mouse_x, mouse_y = pygame.mouse.get_pos()
#     before_x, before_y = self.screen_to_world(mouse_x, mouse_y)
#
#     if event.y > 0:
#         self.zoom = min(ZOOM_MAX, self.zoom + ZOOM_STEP)
#     elif event.y < 0:
#         self.zoom = max(ZOOM_MIN, self.zoom - ZOOM_STEP)
#
#     after_x, after_y = self.screen_to_world(mouse_x, mouse_y)
#
#     self.camera_x += before_x - after_x
#     self.camera_y += before_y - after_y
#
#     if self.zoom == 1.0:
#         self.camera_x = 0
#         self.camera_y = 0
#
#     # --------------------------------------------------
#     # координати та згладжування
#     # --------------------------------------------------
#
#     def node_to_center_point(self, node):
#         return (
#             node.col * CELL_SIZE + CELL_SIZE // 2,
#             node.row * CELL_SIZE + CELL_SIZE // 2
#         )
#
#     def create_smooth_path(self, path):
#         """
#         маршрут A* у плавнішу траєкторію.
#         """
#         if len(path) < 2:
#             return []
#
#         points = [self.node_to_center_point(node) for node in path]
#         smooth_points = []
#
#         for i in range(len(points) - 1):
#             x1, y1 = points[i]
#             x2, y2 = points[i + 1]
#
#             steps = 12
#
#             for step in range(steps):
#                 t = step / steps
#
#                 # інтерполяція між двома точками
#                 x = x1 + (x2 - x1) * t
#                 y = y1 + (y2 - y1) * t
#
#                 smooth_points.append((x, y))
#
#         smooth_points.append(points[-1])
#         return smooth_points
#
# # --------------------------------------------------
# # малювання
# # --------------------------------------------------
#
# def draw_fixed_icon(self, image, world_x, world_y):
#     """
#     іконки не масштабуються при zoom, тільки карта
#     """
#
#     screen_x, screen_y = self.world_to_screen(world_x, world_y)
#
#     rect = image.get_rect(
#         center=(
#             screen_x + CELL_SIZE * self.zoom / 2,
#             screen_y + CELL_SIZE * self.zoom / 2
#         )
#     )
#
#     self.window.blit(image, rect)
#
# def calculate_angle(self, current_node, next_node):
#     dx = next_node.col - current_node.col
#     dy = next_node.row - current_node.row
#
#     angle = math.degrees(math.atan2(dy, dx))
#
#     return angle
#
# def draw_background_map(self):
#     scaled_width = int(WINDOW_WIDTH * self.zoom)
#     scaled_height = int(WINDOW_HEIGHT * self.zoom)
#
#     map_image = pygame.transform.smoothscale(
#         self.assets["map"],
#         (scaled_width, scaled_height)
#     )
#
#     screen_x, screen_y = self.world_to_screen(0, 0)
#     self.window.blit(map_image, (screen_x, screen_y))
#
#     overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
#     overlay.fill((0, 0, 0, 90))
#     self.window.blit(overlay, (0, 0))
#
# def draw_grid_lines(self):
#     for row in range(ROWS + 1):
#         y = row * CELL_SIZE
#         start = self.world_to_screen(0, y)
#         end = self.world_to_screen(WINDOW_WIDTH, y)
#
#     for col in range(COLS + 1):
#         x = col * CELL_SIZE
#         start = self.world_to_screen(x, 0)
#         end = self.world_to_screen(x, WINDOW_HEIGHT)
#
# def draw_route(self):
#     """
#     жовтий маршрут
#     беремо точки зі згладженого маршруту
#     """
#     if len(self.smooth_path_points) < 2:
#         return
#
#     points = [
#         self.world_to_screen(x, y)
#         for x, y in self.smooth_path_points[self.current_smooth_index:]
#     ]
#
#     if len(points) > 1:
#         pygame.draw.aalines(self.window, ROUTE_COLOR, False, points)
#         pygame.draw.lines(self.window, ROUTE_COLOR, False, points, max(2, int(4 * self.zoom)))
#
# def draw_trail(self):
#     if len(self.trail) < 2:
#         return
#
#     points = []
#
#     for node in self.trail:
#         x = node.col * CELL_SIZE + CELL_SIZE // 2
#         y = node.row * CELL_SIZE + CELL_SIZE // 2
#         points.append(self.world_to_screen(x, y))
#
#     pygame.draw.lines(self.window, TRAIL_COLOR, False, points, max(2, int(5 * self.zoom)))
# def draw_nodes(self):
#     for row in self.grid.nodes:
#         for node in row:
#             x = node.col * CELL_SIZE
#             y = node.row * CELL_SIZE
#
#             if node.is_obstacle:
#                 self.draw_fixed_icon(self.assets["static"], x, y)
#
#             elif node.is_start:
#                 self.draw_fixed_icon(self.assets["start"], x, y)
#
#             elif node.is_end:
#                 self.draw_fixed_icon(self.assets["finish"], x, y)
#
# def draw_rotated_uav(self):
#     """
#     Малює основний БПЛА у піксельній позиції, а не в центрі клітинки.
#     Завдяки цьому рух виглядає плавніше.
#     """
#     if not self.uav_node:
#         return
#
#     image = self.assets["uav"]
#     rotated = pygame.transform.rotate(image, -self.uav_angle)
#
#     screen_center = self.world_to_screen(self.uav_x, self.uav_y)
#     rect = rotated.get_rect(center=screen_center)
#
#     self.window.blit(rotated, rect)
#
# def draw_dynamic_obstacles(self):
#     """
#     Малює два типи дронів:
#     interceptor — розумний;
#     hunter — переслідувач.
#     """
#
#     for obstacle in self.dynamic_obstacles:
#         center_x = obstacle.col * CELL_SIZE + CELL_SIZE // 2
#         center_y = obstacle.row * CELL_SIZE + CELL_SIZE // 2
#
#         screen_center = self.world_to_screen(center_x, center_y)
#
#         # Вибираємо картинку залежно від типу дрона
#         if obstacle.type == "interceptor":
#             image = self.assets["interceptor"]
#         else:
#             image = self.assets["hunter"]
#
#         rotated = pygame.transform.rotate(
#             image,
#             -obstacle.angle
#         )
#
#         rect = rotated.get_rect(center=screen_center)
#
#         self.window.blit(rotated, rect)
# def draw_cursor(self):
#     x, y = pygame.mouse.get_pos()
#     self.window.blit(self.assets["cursor"], (x, y))
#
# def draw(self):
#     self.window.fill((0, 0, 0))
#
#     self.draw_background_map()
#     self.draw_trail()
#     self.draw_route()
#     self.draw_nodes()
#     self.draw_dynamic_obstacles()
#     self.draw_rotated_uav()
#     self.draw_grid_lines()
#     self.draw_cursor()
#
#     pygame.display.update()
#
# # --------------------------------------------------
# # побудова маршруту
# # --------------------------------------------------
#
# def clear_path_visuals(self):
#     self.grid.clear_path_states()
#
#     if self.start_node:
#         self.start_node.is_start = True
#
#     if self.end_node:
#         self.end_node.is_end = True
#
# def create_temporary_danger_blocks(self, radius=0):
#     blocked_nodes = []
#
#     for obstacle in self.dynamic_obstacles:
#         for dr in range(-radius, radius + 1):
#             for dc in range(-radius, radius + 1):
#                 node = self.grid.get_node(obstacle.row + dr, obstacle.col + dc)
#
#                 if (
#                         node
#                         and node != self.start_node
#                         and node != self.end_node
#                         and node != self.uav_node
#                         and not node.is_obstacle
#                 ):
#                     node.is_obstacle = True
#                     blocked_nodes.append(node)
#
#     return blocked_nodes
#
# def restore_temporary_blocks(self, blocked_nodes):
#     for node in blocked_nodes:
#         node.is_obstacle = False
#
# def build_path(self, from_node, danger_radius=0):
#     if not from_node or not self.end_node:
#         return False
#
#     self.clear_path_visuals()
#
#     temporary_blocks = self.create_temporary_danger_blocks(radius=danger_radius)
#     new_path = astar_search(self.grid, from_node, self.end_node, safety_radius=2)
#     self.restore_temporary_blocks(temporary_blocks)
#
#     if not new_path:
#         self.path = []
#         return False
#
#     self.path = new_path
#     self.move_index = 1 if len(self.path) > 1 else 0
#
#     self.smooth_path_points = self.create_smooth_path(self.path)
#     self.current_smooth_index = 0
#
#     if self.uav_node:
#         self.uav_x, self.uav_y = self.node_to_center_point(self.uav_node)
#
#     for node in self.path:
#         if node != self.start_node and node != self.end_node and node != self.uav_node:
#             node.is_path = True
#
#     return True
#
# def rebuild_path(self, danger_radius=4, force=False):
#     current_time = pygame.time.get_ticks()
#
#     if not force and current_time - self.last_rebuild_time < self.rebuild_delay:
#         return False
#
#     self.last_rebuild_time = current_time
#
#     path_found = self.build_path(self.uav_node, danger_radius=danger_radius)
#
#     if path_found:
#         self.is_moving = True
#         return True
#
#     path_found = self.build_path(self.uav_node, danger_radius=0)
#     self.is_moving = path_found
#     return path_found
#
# # --------------------------------------------------
# # start
# # --------------------------------------------------
#
# def run_algorithm(self):
#     if self.start_node and self.end_node:
#         self.uav_node = self.start_node
#         self.is_moving = False
#         self.trail = [self.start_node]
#         self.build_path(self.uav_node, danger_radius=0)
#
# def start_uav_movement(self):
#     if not self.start_node or not self.end_node:
#         return
#
#     self.uav_node = self.start_node
#     self.uav_x, self.uav_y = self.node_to_center_point(self.start_node)
#     self.dynamic_obstacles = []
#     self.trail = [self.start_node]
#
#     path_found = self.build_path(self.uav_node, danger_radius=0)
#
#     if path_found:
#         self.is_moving = True
#         self.move_index = 1
#
# # --------------------------------------------------
# # рух основного дрона
# # --------------------------------------------------
#
# def move_uav(self):
#     if not self.is_moving:
#         return
#
#     if self.uav_node == self.end_node:
#         self.is_moving = False
#         return
#
#     if not self.path or self.move_index >= len(self.path):
#         self.rebuild_path(danger_radius=2)
#         return
#
#     current_time = pygame.time.get_ticks()
#
#     if current_time - self.last_move_time < self.move_delay:
#         return
#
#     self.last_move_time = current_time
#
#     next_node = self.path[self.move_index]
#
#     if next_node.is_obstacle:
#         self.rebuild_path(danger_radius=2)
#         return
#
#     for obstacle in self.dynamic_obstacles:
#         if obstacle.row == next_node.row and obstacle.col == next_node.col:
#             self.rebuild_path(danger_radius=2)
#             return
#
#     self.uav_angle = self.calculate_angle(self.uav_node, next_node)
#
#     self.uav_node = next_node
#     self.trail.append(self.uav_node)
#
#     self.move_index += 1
#
#     if self.uav_node == self.end_node:
#         self.is_moving = False
#
# # --------------------------------------------------
# # зміна середовища
# # --------------------------------------------------
#
# def change_environment_during_movement(self):
#     if not self.is_moving:
#         return
#
#     current_time = pygame.time.get_ticks()
#
#     if current_time - self.last_environment_change_time < self.environment_change_delay:
#         return
#
#     self.last_environment_change_time = current_time
#
#     created_obstacles = self.environment.add_obstacle_cluster_on_path(
#         self.path,
#         self.move_index,
#         self.start_node,
#         self.end_node,
#         self.uav_node
#     )
#
#     if created_obstacles:
#         self.rebuild_path(danger_radius=1)
#
# # --------------------------------------------------
# # динамічні дрони
# # --------------------------------------------------
#
# def spawn_interceptor_from_city(self):
#     """
#     створює interceptor з міської зони, летять на випередження
#     """
#     if not self.is_moving:
#         return
#
#     interceptor_count = sum(1 for obstacle in self.dynamic_obstacles if obstacle.type == "interceptor")
#
#     if interceptor_count >= self.max_interceptors:
#         return
#
#     current_time = pygame.time.get_ticks()
#
#     if current_time - self.last_interceptor_spawn_time < self.interceptor_spawn_delay:
#         return
#
#     self.last_interceptor_spawn_time = current_time
#
#     min_col = 460 // CELL_SIZE
#     max_col = 690 // CELL_SIZE
#     min_row = 470 // CELL_SIZE
#     max_row = 650 // CELL_SIZE
#
#     row = random.randint(min_row, max_row)
#     col = random.randint(min_col, max_col)
#
#     node = self.grid.get_node(row, col)
#
#     if node and not node.is_start and not node.is_end and node != self.uav_node:
#         self.dynamic_obstacles.append(
#             DynamicObstacle(row, col, obstacle_type="interceptor")
#         )
#
# def spawn_random_hunter(self):
#     """
#     створює hunterи у випадкових місцях карти.
#     Вони просто переслідують основний БПЛА.
#     """
#     if not self.is_moving:
#         return
#
#     hunter_count = sum(1 for obstacle in self.dynamic_obstacles if obstacle.type == "hunter")
#
#     if hunter_count >= self.max_hunters:
#         return
#
#     current_time = pygame.time.get_ticks()
#
#     if current_time - self.last_hunter_spawn_time < self.hunter_spawn_delay:
#         return
#
#     self.last_hunter_spawn_time = current_time
#
#     for _ in range(50):
#         row = random.randint(0, ROWS - 1)
#         col = random.randint(0, COLS - 1)
#
#         node = self.grid.get_node(row, col)
#
#         if (
#                 node
#                 and not node.is_start
#                 and not node.is_end
#                 and not node.is_obstacle
#                 and node != self.uav_node
#         ):
#             self.dynamic_obstacles.append(
#                 DynamicObstacle(row, col, obstacle_type="hunter")
#             )
#             return
#
# def move_dynamic_obstacles(self):
#     """
#     Рух двох типів динамічних дронів:
#     - interceptor рухається швидше і летить на випередження;
#     - hunter рухається повільніше і переслідує БПЛА.
#     """
#     if not self.is_moving:
#         return
#
#     current_time = pygame.time.get_ticks()
#
#     if current_time - self.last_interceptor_move_time >= self.interceptor_move_delay:
#         self.last_interceptor_move_time = current_time
#
#         for obstacle in self.dynamic_obstacles:
#             if obstacle.type == "interceptor":
#                 obstacle.move_interceptor(
#                     self.grid,
#                     self.path,
#                     self.move_index,
#                     self.uav_node
#                 )
#
#     if current_time - self.last_hunter_move_time >= self.hunter_move_delay:
#         self.last_hunter_move_time = current_time
#
#         for obstacle in self.dynamic_obstacles:
#             if obstacle.type == "hunter":
#                 obstacle.move_hunter(self.grid, self.uav_node)
#
# def is_dynamic_obstacle_on_future_path(self):
#     future_path = self.path[self.move_index:]
#
#     for obstacle in self.dynamic_obstacles:
#         for node in future_path:
#             if obstacle.row == node.row and obstacle.col == node.col:
#                 return True
#
#     return False
#
# def is_uav_in_danger(self):
#     if not self.uav_node:
#         return False
#
#     for obstacle in self.dynamic_obstacles:
#         distance = abs(obstacle.row - self.uav_node.row) + abs(obstacle.col - self.uav_node.col)
#
#         if distance <= 1:
#             return True
#
#     return False
#
# def handle_dynamic_obstacles(self):
#     """
#     Загальна логіка динамічних дронів.
#     """
#     self.spawn_interceptor_from_city()
#     self.spawn_random_hunter()
#     self.move_dynamic_obstacles()
#
#     if self.is_uav_in_danger():
#         self.full_restart_level()
#         return
#
#     if self.is_dynamic_obstacle_on_future_path():
#         self.rebuild_path(danger_radius=1)
#
# # --------------------------------------------------
# # Full restart
# # --------------------------------------------------
#
# def full_restart_level(self):
#     if not self.start_node or not self.end_node:
#         return
#
#     start_position = self.start_node.position()
#     end_position = self.end_node.position()
#     saved_obstacles = set(self.initial_obstacles)
#
#     self.grid = Grid(ROWS, COLS)
#     self.environment = Environment(self.grid)
#
#     self.start_node = self.grid.get_node(*start_position)
#     self.end_node = self.grid.get_node(*end_position)
#
#     self.start_node.is_start = True
#     self.end_node.is_end = True
#
#     for row, col in saved_obstacles:
#         node = self.grid.get_node(row, col)
#
#         if node and node != self.start_node and node != self.end_node:
#             node.is_obstacle = True
#
#     self.initial_obstacles = saved_obstacles
#
#     self.uav_node = self.start_node
#     self.path = []
#     self.move_index = 0
#     self.dynamic_obstacles = []
#     self.trail = [self.start_node]
#
#     path_found = self.build_path(self.uav_node, danger_radius=4)
#
#     if path_found:
#         self.is_moving = True
#         self.move_index = 1
#     else:
#         self.is_moving = False
#
# # --------------------------------------------------
# # Mouse controls
# # --------------------------------------------------
#
# def handle_left_click(self, row, col):
#     if self.is_moving:
#         return
#
#     node = self.grid.get_node(row, col)
#
#     if not node:
#         return
#
#     if self.start_node is None and node != self.end_node:
#         self.start_node = node
#         node.is_start = True
#         self.uav_node = node
#         self.trail = [node]
#
#     elif self.end_node is None and node != self.start_node:
#         self.end_node = node
#         node.is_end = True
#
#     elif node != self.start_node and node != self.end_node:
#         node.is_obstacle = True
#         self.initial_obstacles.add((node.row, node.col))
#
# def handle_right_click(self, row, col):
#     if self.is_moving:
#         return
#
#     node = self.grid.get_node(row, col)
#
#     if not node:
#         return
#
#     if node == self.start_node:
#         self.start_node = None
#         self.uav_node = None
#         self.trail = []
#
#     if node == self.end_node:
#         self.end_node = None
#
#     self.initial_obstacles.discard((node.row, node.col))
#     node.reset()
#
# def reset_grid(self):
#     self.grid = Grid(ROWS, COLS)
#     self.environment = Environment(self.grid)
#
#     self.start_node = None
#     self.end_node = None
#     self.uav_node = None
#
#     self.path = []
#     self.move_index = 0
#     self.is_moving = False
#
#     self.trail = []
#     self.initial_obstacles = set()
#     self.dynamic_obstacles = []
#
#     self.zoom = 1.0
#     self.camera_x = 0
#     self.camera_y = 0
#
# # --------------------------------------------------
# # Main loop
# # --------------------------------------------------
#
# def run(self):
#     while self.running:
#         self.clock.tick(FPS)
#
#         self.move_uav()
#         self.change_environment_during_movement()
#         self.handle_dynamic_obstacles()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.running = False
#
#             elif event.type == pygame.MOUSEWHEEL:
#                 self.handle_zoom(event)
#
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     self.run_algorithm()
#
#                 elif event.key == pygame.K_m:
#                     self.start_uav_movement()
#
#                 elif event.key == pygame.K_c:
#                     self.reset_grid()
#
#                 elif event.key == pygame.K_r:
#                     self.zoom = 1.0
#                     self.camera_x = 0
#                     self.camera_y = 0
#
#         if pygame.mouse.get_pressed()[0]:
#             row, col = self.get_clicked_position(pygame.mouse.get_pos())
#             self.handle_left_click(row, col)
#
#         elif pygame.mouse.get_pressed()[2]:
#             row, col = self.get_clicked_position(pygame.mouse.get_pos())
#             self.handle_right_click(row, col)
#
#         self.draw()
#
#     pygame.quit()