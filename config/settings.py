# Розмір вікна
MENU_WIDTH = 280

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 563

MAP_WIDTH = WINDOW_WIDTH - MENU_WIDTH

# Розмір сітки
ROWS = 72
COLS = 128
CELL_SIZE = MAP_WIDTH // COLS

# Частота оновлення кадрів
FPS = 160

ASSETS_PATH = "assets"

MAP_IMAGE = "map.png"
CURSOR_IMAGE = "cursor.png"
UAV_IMAGE = "uav.png"
UAV_HOME_IMAGE = "uav_home.png"
FINISH_IMAGE = "finish.png"
STATIC_OBSTACLE_IMAGE = "static.png"
INTERCEPTOR_IMAGE = "interceptor.png"
HUNTER_IMAGE = "hunter.png"
MISSION_COMPLETE_IMAGE = "mission_p.png"

ROUTE_COLOR = (255, 210, 40)      # жовтий
TRAIL_COLOR = (213, 0, 217)      # фіолетовий
# GRID_DARK = (40, 40, 40)

ZOOM_MIN = 1.0
ZOOM_MAX = 3.0
ZOOM_STEP = 0.1

ICON_SIZE = 20
UAV_SIZE = 22
CURSOR_SIZE = 20