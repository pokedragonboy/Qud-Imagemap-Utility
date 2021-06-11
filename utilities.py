import config as cfg
import math

numbers_to_letters = {
    0: "",
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
    9: "I",
    10: "J",
    11: "K",
    12: "L",
    13: "M",
    14: "N",
    15: "O",
    16: "P",
    17: "Q",
    18: "R",
    19: "S",
    20: "T",
    21: "U",
    22: "V",
    23: "W",
    24: "X",
    25: "Y",
    26: "Z"
}


def convert_and_append():
    convert_to_true_coords()
    append_coords_to_list()


def clockwise():  # Not sure if there is a better way than this pseudo-dictionary "code wheel" setup I have going
    direction_list = ["R", "UR", "U", "UL", "L", "DL", "D", "DR"]
    angle_list = [0, 45, 90, 135, 180, -135, -90, -45]

    shift_amount = direction_list.index(cfg.move_1)

    a = shift_amount % len(angle_list)
    angle_list = angle_list[-a:] + angle_list[:-a]  # "Rotating" the angle_list so 0 has the same index as move_1

    if angle_list[direction_list.index(cfg.move_2)] < 0:
        clockwiseness_bool = True

    elif angle_list[direction_list.index(cfg.move_2)] > 0:
        clockwiseness_bool = False

    return clockwiseness_bool


def populate_rowletters_to_numbers():
    i = 0
    while i <= cfg.grid_height:
        letter = numbers_to_letters[math.floor(i / 26)] + numbers_to_letters[(i % 26) + 1]
        cfg.rowletters_to_numbers[letter] = i
        i += 1


def nice_string(uglylist):
    prettylist = str(uglylist).replace("',", ",").replace(" '", "").lstrip("['").rstrip("']")
    return prettylist


def find_move_direction(starting_index):
    x = 0
    y = 1

    if cfg.input_mem[starting_index][x] > cfg.input_mem[starting_index + 1][x]:
        move_direction = "L"  # L stands for Left
        if cfg.rowletters_to_numbers[cfg.input_mem[starting_index][y]] > \
                cfg.rowletters_to_numbers[cfg.input_mem[starting_index + 1][y]]:
            move_direction = "UL"
        elif cfg.rowletters_to_numbers[cfg.input_mem[starting_index][y]] < \
                cfg.rowletters_to_numbers[cfg.input_mem[starting_index + 1][y]]:
            move_direction = "DL"
    elif cfg.input_mem[starting_index][x] < cfg.input_mem[starting_index + 1][x]:
        move_direction = "R"  # R stands for Right
        if cfg.rowletters_to_numbers[cfg.input_mem[starting_index][y]] > \
                cfg.rowletters_to_numbers[cfg.input_mem[starting_index + 1][y]]:
            move_direction = "UR"
        elif cfg.rowletters_to_numbers[cfg.input_mem[starting_index][y]] < \
                cfg.rowletters_to_numbers[cfg.input_mem[starting_index + 1][y]]:
            move_direction = "DR"
    elif cfg.rowletters_to_numbers[cfg.input_mem[starting_index][y]] > \
            cfg.rowletters_to_numbers[cfg.input_mem[starting_index + 1][y]]:
        move_direction = "U"  # U stands for Up
    elif cfg.rowletters_to_numbers[cfg.input_mem[starting_index][y]] < \
            cfg.rowletters_to_numbers[cfg.input_mem[starting_index + 1][y]]:
        move_direction = "D"  # D stands for Down

    return move_direction


def convert_to_true_coords():
    if cfg.corner[1] == "L":
        cfg.x_coord = int(cfg.input_mem[1][0]) * cfg.tile_width
    elif cfg.corner[1] == "R":
        cfg.x_coord = (int(cfg.input_mem[1][0]) * cfg.tile_width) + (cfg.tile_width - 1)
    if cfg.corner[0] == "T":
        cfg.y_coord = int(cfg.rowletters_to_numbers[cfg.input_mem[1][1]]) * cfg.tile_height
    elif cfg.corner[0] == "B":
        cfg.y_coord = (int(cfg.rowletters_to_numbers[cfg.input_mem[1][1]]) * cfg.tile_height) + (cfg.tile_height - 1)


def append_coords_to_list():
    add_line_to_message_box(f"{int(cfg.x_coord)},{int(cfg.y_coord)}")
    cfg.coordinate_list.append(f"{int(cfg.x_coord)},{int(cfg.y_coord)}")
    cfg.last_loop_coords.append([cfg.x_coord, cfg.y_coord])


# def switchback_corner_replacer(tb_lr_list):
#     for i in tb_lr_list:
#         cfg.corner = cfg.moves_to_corners[tb_lr_list[0]] + "*"
#         cfg.corner = cfg.corner.replace("*", i)
#         convert_to_true_coords(cfg.corner)
#         append_coords_to_list()

def moves_to_corners(move, special_operation = ""):
    moves_to_corners_reg = {
        "U": "T",
        "D": "B",
        "L": "L",
        "R": "R",
        "UL": "TL",
        "UR": "TR",
        "DL": "BL",
        "DR": "BR"
    }

    moves_to_corners_inv = {
        "U": "B",
        "D": "U",
        "L": "R",
        "R": "L",
        "UL": "BR",
        "UR": "BL",
        "DL": "TR",
        "DR": "TL"
    }

    if special_operation == "":
        return moves_to_corners_reg[move]

    if special_operation == "invert":
        return moves_to_corners_inv[move]


def print_coord_list():
    add_line_to_message_box("Coordinate List:")
    add_line_to_message_box(nice_string(cfg.coordinate_list))


def validate_input():
    # Tests if the user input has something wrong with it, and rejects the input if it does.
    cfg.error_found = False

    # Checks for correct length. Comes first because inputs that are too long or short mess up the other testing.
    if len(cfg.input_coords) < 2:
        add_line_to_message_box("That input has too few spaces.")
        add_line_to_message_box("Your input has not been used.")
        cfg.error_found = True  # Set that there is an error if the input is too short

    elif len(cfg.input_coords) > 2:
        add_line_to_message_box("That input has too many spaces.")
        add_line_to_message_box("Your input has not been used.")
        cfg.error_found = True  # Set that there is an error if the input is too long

    # Further checking, after it knows that the string is the right length.
    elif len(cfg.input_coords) == 2:

        # Sets the relevant sections of input_coords to individual variables to make the code easier to read.
        cfg.input_coords.append("")  # Appending a blank string so that input_coords has 3 entries so corner works

        cfg.column = cfg.input_coords[0]  # X coordinate, from 00-79 for Caves of Qud
        cfg.row = cfg.input_coords[1].upper()  # Y coordinate, from  A-Y for Caves of Qud
        cfg.corner = cfg.input_coords[2]  # BR, BL, TR, TL

        # Check that inputs are of the correct type and are within the accepted values.
        # Column checking
        try:
            int(cfg.column)
            cfg.column = int(cfg.column)
        except ValueError:
            add_line_to_message_box("The X coordinate can only be a whole number.")
            cfg.error_found = True
        if type(cfg.column) == int:
            if int(cfg.column) > (cfg.grid_width - 1):
                add_line_to_message_box("The X coordinate cannot be greater than 79.")
                cfg.error_found = True
            elif int(cfg.column) < 0:
                add_line_to_message_box("The X coordinate cannot be less than 0.")
                cfg.error_found = True

        # Row checking
        if cfg.row not in list(cfg.rowletters_to_numbers)[:cfg.grid_height]:
            add_line_to_message_box(f"The Y coordinate must be a letter from {list(cfg.rowletters_to_numbers)[0]} "
                  f"to {list(cfg.rowletters_to_numbers)[cfg.grid_height]}.")
            cfg.error_found = True


def submit_entry(entry_box_contents):
    cfg.user_input = entry_box_contents
    add_line_to_message_box(" > " + cfg.user_input)
    cfg.waiting = False


def add_line_to_message_box(message):
    formatted_contents = cfg.message_box_contents.get() + "\n " + message
    cfg.message_box_contents.set(formatted_contents)
