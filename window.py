from tkinter import *
from tkinter.filedialog import askopenfilename
import config as cfg
import utilities as util
import time
import math
from PIL import ImageTk, Image

# todo: Round up the last couple of input() uses (make them into the wait loop thing)
# todo: Make the message box text selectable, rather than just invisibly copying to your clipboard
# todo: Make single-tile mode work again
# todo: Implement a nicer way to choose tile modes than text input (perhaps a pop-up window or radio buttons)
# todo: Allow one to zoom in on imagemap preview
#    - This will make turning mouse coords into tile coords more complicated
# todo: Make the preview more useful by showing the last input tile
# todo: Allow one to select whether they want commas or spaces between coordinates
#    - Commas are what maschek.hu uses, spaces are what the actual imagemap code uses

# I would like to have all of these functions in a separate module, but I cannot seem to figure out how to make it work


def update_polygon():
    global polygon
    try:  # This is in a try block to get past the first couple loops where the coordinate list is empty and it would
        # run into an error tying to make '' into an integer.
        canvas_coords = list(map(int, util.nice_string(cfg.coordinate_list).split(",")))  # This is pretty hacky
        imgmap_preview.delete("polygon")
        polygon = imgmap_preview.create_polygon(canvas_coords, fill="", outline="#EA58E8", tag="polygon")

    except ValueError:
        pass


def wait():  # Naming this function "wait" might be bad practice?
    global hoverbox  # Setting hoverbox to global so that I can create canvas rectangles within this function

    mouse_x = imgmap_preview.winfo_pointerx() - imgmap_preview.winfo_rootx() \
              + preview_xbar.get()[0] * background_image.width()  # The mouse x position, relative to the top left
                                                                  # corner of the preview background image
    mouse_y = imgmap_preview.winfo_pointery() - imgmap_preview.winfo_rooty() \
              + preview_ybar.get()[0] * background_image.height()  # The mouse y position, relative to the top left
                                                                   # corner of the preview background image
    mouse_coords = f"{math.floor(mouse_x / cfg.tile_width)} " \
                   f"{util.numbers_to_letters[math.floor(mouse_y / cfg.tile_height) % cfg.grid_height + 1]}"

    # Makes a rectangle that highlights the tile which you are currently hovering over
    # All the math is just to get the coordinates of the corners of the tile so that the rectangle will snap to it
    imgmap_preview.delete("hoverbox")
    hoverbox = imgmap_preview.create_rectangle(math.floor(mouse_x / cfg.tile_width) * cfg.tile_width,
                                               math.floor(mouse_y / cfg.tile_height) * cfg.tile_height,
                                               math.floor(mouse_x / cfg.tile_width) * cfg.tile_width + cfg.tile_width - 1,
                                               math.floor(mouse_y / cfg.tile_height) * cfg.tile_height + cfg.tile_height - 1,
                                               outline="#EA58E8", tag="hoverbox")

    mouse_position.set(mouse_coords)

    root.update()


def gui_input(prompt):
    util.add_line_to_message_box(prompt)
    entry_box.delete(0, END)
    cfg.waiting = True
    while cfg.waiting:
        wait()


# Below here are the functions that are actually the program, rather than utilities for the program that I can't put in
# the utilities module for one reason or another

def splitter():
    util.add_line_to_message_box("Select a mode (input M for multi-tile mode or S for single-tile mode):")
    entry_box.delete(0, END)
    cfg.waiting = True
    while cfg.waiting:
        wait()

    if cfg.user_input == "":
        pass

    elif cfg.user_input.upper() != "S" and cfg.user_input.upper() != "M":
        print("Sorry, that input is not recognized.")
        util.add_line_to_message_box("Sorry, that input is not recognized")

    elif cfg.user_input.upper() == "S":
        imgmap_preview.delete("polygon")
        util.add_line_to_message_box("Single-tile mode started \n")
        cfg.coordinate_list = []
        cfg.input_mem = []
        root.update()
        single_tile_mode()

    elif cfg.user_input.upper() == "M":
        imgmap_preview.delete("polygon")
        print("Multi-tile mode started")
        print()
        util.add_line_to_message_box("Multi-tile mode started \n")
        cfg.coordinate_list = []
        cfg.input_mem = []
        root.update()
        multi_tile_mode()

    root.after(1000, func=splitter)


def single_tile_mode():
    import config as cfg
    import utilities as util

    while True:
        time.sleep(0.01)
        util.add_line_to_message_box("Input your coordinates:")
        entry_box.delete(0, END)
        cfg.waiting = True
        while cfg.waiting:
            wait()

        cfg.input_coords = cfg.user_input.split(" ")
        command = cfg.input_coords[0].lower()

        if command == "pause":  # This command does nothing, it just hits a breakpoint for debugging purposes
            break

        else:
            util.validate_input()

            # Prevents code from proceeding if the inputs are off, and tells the user their input was rejected.
            if cfg.error_found:
                print("Your input has not been used.")

            elif not cfg.error_found:
                cfg.x_coord = int(cfg.column) * cfg.tile_width
                cfg.y_coord = int(cfg.rowletters_to_numbers[cfg.row]) * cfg.tile_height

                util.append_coords_to_list()

                cfg.x_coord = (int(cfg.column) * cfg.tile_width) + (cfg.tile_width - 1)
                cfg.y_coord = (int(cfg.rowletters_to_numbers[cfg.row]) * cfg.tile_height) + (cfg.tile_height - 1)

                util.append_coords_to_list()

                util.print_coord_list()
                root.clipboard_clear()
                root.clipboard_append(util.nice_string(cfg.coordinate_list).replace(",", " "))
                util.add_line_to_message_box("(This string has been copied to your clipboard) \n")
                break


def multi_tile_mode():

    # This enormous try: block should be commented out while editing/bugfixing and turned on for releases
    # It only serves to make it so that if any unexpected errors are thrown, the full coordinate list is printed so that
    # people's work is not lost. Ideally, it will never be used.

    # try:
    finishing = False

    while True:
        time.sleep(0.01)
        util.add_line_to_message_box("Input your coordinates:")
        entry_box.delete(0, END)
        cfg.waiting = True
        while cfg.waiting:
            wait()

        cfg.input_coords = cfg.user_input.split(" ")
        command = cfg.input_coords[0].lower()

        # Handling any special inputs from the user.
        # todo Rearrange these commands in order of most likely to be used for small optimization
        # todo Possible new commands:
        #   * help - prints a list of commands & their functions, as well as directing the user to manual.txt
        #   * pause - troubleshooting only, just runs into a breakpoint
        # The finish command needs to be on its own outside of the main if... elif... else... chain which handles other
        # commands so that fake the "user input" which it assigns will be processed.
        if command == "finish":
            if len(cfg.coordinate_list) >= 3:
                if cfg.input_mem[-1] == first_tile:
                    gui_input("Do you really want to finish this shape? Y/N: ")
                    if cfg.user_input.upper() == "Y":
                        cfg.input_coords = second_tile
                        finishing = True
                else:
                    util.add_line_to_message_box("You cannot finish this shape yet, as you have not ended on the first tile.")
            else:
                util.add_line_to_message_box("You cannot finish this shape yet, as it only has 2 coordinates.")

        # Do not change this from an if to an elif unless you are doing a major rewrite rather than small optimizations
        if command == "stop":
            if input("Do you really want to exit out of multi-tile mode? Y/N: ").upper() == "Y":
                if len(cfg.coordinate_list) > 0:
                    util.print_coord_list()
                break

        elif command == "pause":
            pass

        elif command == "print":
            util.print_coord_list()

        elif command == "delete":  # Right now, delete has many problems. Might want to comment it out for a release
            if len(cfg.coordinate_list) >= 1:
                util.add_line_to_message_box(f"{cfg.coordinate_list[-1]} removed.")
                cfg.coordinate_list.pop(-1)  # Actual entry has to be removed after the message says it was removed

                cfg.input_mem.pop(-1)
                if len(cfg.deleted_input_mem) == 1:  # Test this code. May be a source of error. Not sure.
                    cfg.input_mem.append(cfg.input_mem[-1])
                    cfg.input_mem[-2] = cfg.input_mem[-3]
                    cfg.input_mem[-3] = cfg.deleted_input_mem.pop(-1)
            elif len(cfg.coordinate_list) == 0:
                util.add_line_to_message_box("There are currently no tiles in your coordinate list. "
                                             "You cannot delete something which doesn't exist.")

        elif command == "clear":
            gui_input("Do you really want to clear the coordinate list? Y/N: ")

            if cfg.user_input.upper() == "Y":
                util.print_coord_list()
                cfg.coordinate_list = []
                cfg.input_mem = []
                util.add_line_to_message_box("List cleared.")

        # todo Add some logic so it wont say you are replacing the current coordinate list if there isn't a current list
        elif command == "load":
            if input("Do you really want to load an old coordinate list, "
                     "replacing the current coordinate list? Y/N: ").upper() == "Y":
                groups = input("List to load: ").split(",")
                if len(groups) % 2 == 0:
                    cfg.coordinate_list = []
                    cfg.input_mem = []
                    for n in range(0, int(len(groups) / 2)):
                        n = n * 2
                        cfg.coordinate_list.append(",".join(groups[n:n + 2]))
                elif len(groups) % 2 != 0:
                    util.add_line_to_message_box("The old coordinate list must have an even number of entries.")

        else:
            # Validating the general inputs
            util.validate_input()

            # Checking to make sure the the input is different from the last. This is outside of validate_input because
            # it is specific to multi-tile mode.
            if len(cfg.input_mem) > 0:
                if [cfg.column, cfg.row] == cfg.input_mem[-1]:
                    util.add_line_to_message_box("You cannot input the same tile twice in a row.")
                    cfg.error_found = True

            # Prevents code from proceeding if the inputs are off, and tells the user their input was rejected.
            if cfg.error_found:
                util.add_line_to_message_box("Your input has not been used.")

            # "Main" body of code. What the program does if it understands the inputs.
            elif not cfg.error_found:
                if len(cfg.input_mem) == 1:
                    first_tile = cfg.input_mem[0]
                if len(cfg.input_mem) == 2:
                    second_tile = cfg.input_mem[1]

                cfg.input_mem.append([cfg.column, cfg.row])  # Writes values into input_mem
                if len(
                        cfg.input_mem) > 3:  # The program deletes the oldest item in the memory if there are more than 3
                    cfg.deleted_input_mem.append(
                        cfg.input_mem.pop(0))  # Part of the delete function, may remove if I overhaul it
                    cfg.input_mem_coords[str(cfg.input_mem[-2])] = cfg.last_loop_coords
                    cfg.last_loop_coords = []
                    # if len(cfg.deleted_input_mem) > 10:
                    #     cfg.deleted_input_mem.pop(0)
                    #     cfg.input_mem_coords.pop(0)

                if len(cfg.input_mem) == 3:

                    cfg.move_1 = util.find_move_direction(0)
                    cfg.move_2 = util.find_move_direction(1)
                    move_list = [cfg.move_1, cfg.move_2]
                    util.add_line_to_message_box(str(move_list))  # Debug code. Delete at some point.

                    # Determining orientation type, the shape that the two move directions make, so corners can be found
                    orientation_type = ""
                    if cfg.move_1 == cfg.move_2:
                        orientation_type = "Straight Orthogonal"

                        if len(cfg.move_1) == 2:  # Using len() to distinguish diagonal from orthogonal may be an issue
                            orientation_type = "Straight Diagonal"  # todo Investigate very long straight diagonals

                    elif cfg.move_1 != cfg.move_2:
                        orientation_type = "Turn Orthogonal"

                        if len(cfg.move_1) == 2 and len(cfg.move_2) == 2:
                            orientation_type = "Turn Diagonal"

                        if len(cfg.move_1) != len(
                                cfg.move_2):  # This may cause issues if the moves get longer than 2 characters
                            orientation_type = "Turn Gradual"

                        if "U" in move_list and "D" in move_list or "L" in move_list and "R" in move_list:
                            orientation_type = "Switchback Orthogonal"

                        if "UR" in move_list and "DL" in move_list or "UL" in move_list and "DR" in move_list:
                            orientation_type = "Switchback Diagonal"

                    # Using the orientation type found to determine where the corners should be.
                    if orientation_type == "Straight Orthogonal":
                        pass

                    elif orientation_type == "Straight Diagonal":
                        cfg.corner = util.moves_to_corners(cfg.move_1, "invert")
                        util.convert_and_append()

                        if cfg.move_1 == "UL" or cfg.move_1 == "DR":
                            cfg.corner = cfg.corner.replace(cfg.corner[1], util.moves_to_corners(cfg.move_1[1]))

                        elif cfg.move_1 == "DL" or cfg.move_1 == "UR":
                            cfg.corner = cfg.corner.replace(cfg.corner[0], util.moves_to_corners(cfg.move_1[0]))

                        util.convert_and_append()

                        cfg.corner = util.moves_to_corners(cfg.move_2)
                        util.convert_and_append()

                    elif orientation_type == "Turn Orthogonal":
                        if "R" in move_list:
                            t_or_b = "T"
                        elif "L" in move_list:
                            t_or_b = "B"
                        if "U" in move_list:
                            l_or_r = "L"
                        elif "D" in move_list:
                            l_or_r = "R"
                        cfg.corner = t_or_b + l_or_r
                        util.convert_and_append()

                    elif orientation_type == "Turn Diagonal":
                        cfg.corner = util.moves_to_corners(cfg.move_1,
                                                           "invert")  # First corner is where move comes in
                        util.convert_and_append()

                        if util.clockwise():  # Clockwise turns need 2 extra corners
                            if cfg.move_1[0] != cfg.move_2[0]:
                                cfg.corner = cfg.corner.replace(cfg.corner[0], util.moves_to_corners(cfg.move_1[0]))

                            elif cfg.move_1[1] != cfg.move_2[1]:
                                cfg.corner = cfg.corner.replace(cfg.corner[1], util.moves_to_corners(cfg.move_1[1]))

                            util.convert_and_append()

                            cfg.corner = util.moves_to_corners(cfg.move_1)
                            util.convert_and_append()

                        cfg.corner = util.moves_to_corners(cfg.move_2)  # Last corner is where move goes out
                        util.convert_and_append()

                    elif orientation_type == "Turn Gradual":
                        if not util.clockwise():
                            if len(cfg.move_1) == 1:
                                cfg.corner = util.moves_to_corners(cfg.move_2)

                            elif len(cfg.move_1) == 2:
                                cfg.corner = util.moves_to_corners(cfg.move_1, "invert")

                            util.convert_and_append()

                        elif util.clockwise():
                            if len(cfg.move_1) == 1:
                                if cfg.move_1 == "R":
                                    for i in ["T", "B"]:
                                        cfg.corner = "*R"
                                        cfg.corner = cfg.corner.replace("*", i)
                                        util.convert_and_append()

                                elif cfg.move_1 == "L":
                                    for i in ["B", "T"]:
                                        cfg.corner = "*L"
                                        cfg.corner = cfg.corner.replace("*", i)
                                        util.convert_and_append()

                                elif cfg.move_1 == "U":
                                    for i in ["L", "R"]:
                                        cfg.corner = "T*"
                                        cfg.corner = cfg.corner.replace("*", i)
                                        util.convert_and_append()

                                elif cfg.move_1 == "D":
                                    for i in ["R", "L"]:
                                        cfg.corner = "B*"
                                        cfg.corner = cfg.corner.replace("*", i)
                                        util.convert_and_append()

                            elif len(cfg.move_2) == 1:
                                if cfg.move_2 == "R":
                                    for i in ["B", "T"]:
                                        cfg.corner = "*L"
                                        cfg.corner = cfg.corner.replace("*", i)
                                        util.convert_and_append()

                                elif cfg.move_2 == "L":
                                    for i in ["T", "B"]:
                                        cfg.corner = "*R"
                                        cfg.corner = cfg.corner.replace("*", i)
                                        util.convert_and_append()

                                elif cfg.move_2 == "U":
                                    for i in ["R", "L"]:
                                        cfg.corner = "B*"
                                        cfg.corner = cfg.corner.replace("*", i)
                                        util.convert_and_append()

                                elif cfg.move_2 == "D":
                                    for i in ["L", "R"]:
                                        cfg.corner = "T*"
                                        cfg.corner = cfg.corner.replace("*", i)
                                        util.convert_and_append()

                    elif orientation_type == "Switchback Orthogonal":
                        if move_list == ["R", "L"]:
                            for i in ["T", "B"]:
                                cfg.corner = "*R"
                                cfg.corner = cfg.corner.replace("*", i)
                                util.convert_and_append()

                        elif move_list == ["L", "R"]:
                            for i in ["B", "T"]:
                                cfg.corner = "*L"
                                cfg.corner = cfg.corner.replace("*", i)
                                util.convert_and_append()

                        elif move_list == ["U", "D"]:
                            for i in ["L", "R"]:
                                cfg.corner = "T*"
                                cfg.corner = cfg.corner.replace("*", i)
                                util.convert_and_append()

                        elif move_list == ["D", "U"]:
                            for i in ["R", "L"]:
                                cfg.corner = "B*"
                                cfg.corner = cfg.corner.replace("*", i)
                                util.convert_and_append()

                    elif orientation_type == "Switchback Diagonal":
                        cfg.corner = util.moves_to_corners(cfg.move_1, "invert")
                        util.convert_and_append()

                        if cfg.move_1 == "UL" or cfg.move_1 == "DR":
                            cfg.corner = cfg.corner.replace(cfg.corner[1], util.moves_to_corners(cfg.move_1[1]))

                        elif cfg.move_1 == "DL" or cfg.move_1 == "UR":
                            cfg.corner = cfg.corner.replace(cfg.corner[0], util.moves_to_corners(cfg.move_1[0]))

                        util.convert_and_append()

                        cfg.corner = util.moves_to_corners(cfg.move_1)
                        util.convert_and_append()

                        if cfg.move_2 == "UL" or cfg.move_2 == "DR":
                            cfg.corner = cfg.corner.replace(cfg.corner[1], util.moves_to_corners(cfg.move_2[1]))

                        elif cfg.move_2 == "DL" or cfg.move_2 == "UR":
                            cfg.corner = cfg.corner.replace(cfg.corner[0], util.moves_to_corners(cfg.move_2[0]))

                        util.convert_and_append()

                        cfg.corner = util.moves_to_corners(cfg.move_2)
                        util.convert_and_append()

                if not finishing:
                    time.sleep(0.01)
                    update_polygon()
                    util.add_line_to_message_box("Input accepted!")

        if finishing:
            util.print_coord_list()
            root.clipboard_clear()
            root.clipboard_append(util.nice_string(cfg.coordinate_list).replace(",", " ")) # Temporary. Maybe make an option later
            util.add_line_to_message_box("(This string has been copied to your clipboard) \n")
            update_polygon()
            break

        # This is the bottom part of the big try block.
            # Should only be uncommented for releases, as it makes troubleshooting hard but keeps a person's work from being
            # irretrievably lost if they run into an error. This may be improvable.
            # except:
            #     print("The program ran into an unexpected error. Outputting coordinate list (as if you had input 'print').")
            #     util.print_coord_list()

# We use a function to fill in rowletters_to_numbers rather than just having it pre-set so that this will be compatible
# with any size of image. This makes the dict expand to as large as is needed.
util.populate_rowletters_to_numbers()
cfg.coordinate_list = []
cfg.input_mem = []

# Code below here handles the window itself.

# Again, it would be nice to have this in a separate module but I cannot figure out how to do that.
# (Attempts to put it in a different module run into me needing to use root.update() and other methods in the above
# functions, which means I need to import window.py into those modules, which leads to initialization order issues.)

# Current hierarchy:
#   root
#     - image_display
#         - imgmap_preview
#         - preview_ybar
#         - preview_xbar
#     - sidebar
#         - information_box
#         - message_frame
#             - message_canvas
#                 - message_interior_frame
#                     - message_box
#             - msg_box_ybar
#         - entry_box
#         - entry_box_go_button
#         - position_display

background_color = "#155352"
foreground_color = "#0F3B3A"
text_color = "#FFFFFF"

root = Tk()
root.title("Qud Imagemap Utility")
root.geometry("1400x750")

root.configure(bg=background_color)

# The frame containing the canvas which displays the line being drawn
image_display = Frame(root, bg=foreground_color, bd=2, relief=RIDGE)
image_display.pack(padx=10, side="left", expand=True)

# Loading the background image. Done early so that its size can be referenced later
preview_image_path = askopenfilename(title="Select the image you will be making an imagemap on")
background_image = Image.open(preview_image_path)
background_image = ImageTk.PhotoImage(background_image)

# 2 variables which control the maximum dimensions of the canvas. If the image is larger than these, one needs to scroll
# to see the whole thing.
max_img_width = 1300
max_img_height = 600

# The canvas which gives a preview of the imagemap being created
imgmap_preview = Canvas(image_display,
                        width=min(background_image.width(), max_img_width),
                        height=min(background_image.height(), max_img_height),
                        bg=foreground_color, scrollregion=(0, 0, background_image.width(), background_image.height()))

# Putting the background image on the canvas
imgmap_preview.create_image(background_image.width()/2, background_image.height()/2, image=background_image)

# The scrollbars which scrolls the canvas
preview_ybar = Scrollbar(image_display, troughcolor=foreground_color, orient=VERTICAL, command=imgmap_preview.yview)
preview_ybar.pack(side="right", fill=Y, padx=3, pady=3)

preview_xbar = Scrollbar(image_display, orient=HORIZONTAL, command=imgmap_preview.xview)
preview_xbar.pack(side="bottom", fill=X, padx=3, pady=3)

imgmap_preview.configure(yscrollcommand=preview_ybar.set)
imgmap_preview.configure(xscrollcommand=preview_xbar.set)

# For some reason, I have to pack the canvas down here if I want everything to work
imgmap_preview.pack(side="left", padx=3, pady=3)

# The frame containing the input and message display-handling widgets
sidebar = Frame(root, bg=background_color)
# sidebar is packed before image_display so that in small windows, image_display will be shrunk before the sidebar
sidebar.pack(side="right", expand=True, before=image_display)

sidebar.grid_rowconfigure(1, weight=1)  # setting row 1 to have a weight so that it will shrink when the window does
                                        # (row 1 contains the scrolling message box)

cfg.message_box_contents = StringVar()

# Creating and placing a box containing information on the program
information_box = Label(sidebar, text="Welcome to the Qud Imagemap Utility! \n"
                                      "To use this program, first select a mode (single-tile or multi-tile), "
                                      "then input tile coordinate pairs in the format XX Y, travelling CLOCKWISE "
                                      "around your desired polygon. \n"
                                      "Useful commands: \n"
                                      "  clear - fully clear the list of coordinates \n"
                                      "  print - print the current list of coordinates \n"
                                      "  finish - print the list of coordinates and stop the program \n"
                                      "For a full command list and instructions, see manual.txt.",
                        wraplength=400, bg=foreground_color, fg=text_color, relief=RIDGE, width=50, justify=LEFT, anchor=W)
information_box.grid(row=0, column=1, columnspan=3, padx=5, pady=3, sticky=EW)

# A frame containing the message box and its scrollbar so that I can use .pack on them rather than .grid
message_frame = Frame(sidebar, bg=foreground_color, relief=RIDGE, borderwidth=2, width=50)
message_frame.grid(row=1, column=1, columnspan=3, padx=5, pady=3, sticky=EW)

# A canvas that I put message_box inside of in order to make message_box scrollable
message_canvas = Canvas(message_frame, bg=foreground_color, width=454, height=325, highlightthickness=0, relief=RIDGE)
# padx and pady are set to 1 so the border of message_frame is visible
message_canvas.pack(side="left", padx=2, pady=2)

message_interior_frame = Frame(message_canvas)

# The label which displays all the user inputs and gives text outputs. Basically a glorified text terminal.
message_box = Label(message_interior_frame, textvariable=cfg.message_box_contents, justify=LEFT,
                    wraplength=430, bg=foreground_color, fg=text_color, highlightcolor="#FFFFFF")
message_box.pack(ipadx=5)

msg_box_ybar = Scrollbar(message_frame, orient=VERTICAL, command=message_canvas.yview,
                         bg=foreground_color, troughcolor=foreground_color)
msg_box_ybar.pack(side="right", fill=Y, padx=4, pady=4)

# Took this code from the internet, am like 90% sure that it just dynamically resizes the scroll region
message_box.bind("<Configure>", lambda e: message_canvas.configure(scrollregion=message_canvas.bbox("all")))

message_canvas.create_window((0, 325), window=message_interior_frame, anchor=SW)

message_canvas.configure(yscrollcommand=msg_box_ybar.set)

# The frame containing the entry box, enter button, and the coordinate display. Mainly just a style thing
entry_frame = Frame(sidebar, bg=foreground_color, relief=RIDGE, borderwidth=2)
entry_frame.grid(row=2, column=1, columnspan=3, padx=5, sticky=EW)

entry_box = Entry(entry_frame, bg=foreground_color, fg=text_color, insertbackground=text_color, relief=SUNKEN, width=40)
entry_box.bind('<Return>', lambda e: util.submit_entry(entry_box.get()))
entry_box.grid(row=2, column=1, padx=3, pady=3, sticky=N + S + W)

entry_box_go_button = Button(entry_frame, bg="#FFFFFF", text="Enter", width=6, relief=RAISED,
                             command=lambda: util.submit_entry(entry_box.get()))
entry_box_go_button.grid(row=2, column=2, padx=0, pady=3, sticky=N + S + W)

mouse_position = StringVar()  # DEBUG CODE. DELETE AT SOME POINT (or at least move it somewhere else)
position_display = Label(entry_frame, textvariable=mouse_position, width=4)  # DEBUG
position_display.grid(row=2, column=3, sticky=N + S + E, padx=3, pady=3)  # DEBUG

# Makes it so that clicking the mouse on a tile acts like inputting that tile's coordinates into the entry box.
# This is a little tacked-on, but *so* helpful
imgmap_preview.bind("<Button-1>", lambda e: util.submit_entry(mouse_position.get()))

root.after(1000, func=splitter)
root.mainloop()
