coordinate_list = []  # The full list of coordinate pairs which the program generates.
input_mem = []  # A list of the 3 most recently-input tiles.
deleted_input_mem = []  # A list of the tiles which got removed from input_mem todo Update this
input_mem_coords = {}  # A dictionary containing pairings ofa given input and the coordinate pairs it generated.

last_loop_coords = []

move_1 = ""
move_2 = ""

input_coords = []
error_found = False

column = 0
row = ""
corner = ""

x_coord = ""
y_coord = ""

rowletters_to_numbers = {}

user_input = ""
message_box_contents = ""

waiting = False  # Very very jank. A boolean that says if the program is currently waiting for input


# These are the values one needs to change if adapting the program to a different game.
# tile_width is how many pixels wide a tile is, tile_height is how many pixels tall a tile is.
# grid_width is how many tiles wide the grid is, grid_height is how many tiles tall the grid is.

tile_width = 16
tile_height = 24

grid_width = 80
grid_height = 25
