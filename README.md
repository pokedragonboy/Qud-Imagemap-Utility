# Qud-Imagemap-Utility
    OVERVIEW:
        This is a program designed to help create imagemap links which conform exactly to a grid, designed for usage in wikis for tile-based games.
        More specifically, this was designed for the Caves of Qud Wiki.


    SETUP:
        This program requires that one installs Pillow, a python module for image processing, before running the program.
	
	When creating an imagemap, one needs an image to work on. Upon opening the program, it will bring up a file select dialogue for you to choose the image. 
	(For practice, I recommend using the image of the Qud World Map which is included in the folder, but you can use anything, just as long as the edges of the image align with the grid for your game.)


    GENERAL INFO:
        This program uses a coordinate system, where each tile in the image has a number and a letter associated with it, as follows:

         00 01 02 03 04 05	    00	   01	  02     03     04     05
        A[] [] [] [] [] []	A [00 A] [01 A] [02 A] [03 A] [04 A] [05 A]
        B[] [] [] [] [] []	B [00 B] [01 B] [02 B] [03 B] [04 B] [05 B]
        C[] [] [] [] [] []	C [00 C] [01 C] [02 C] [03 C] [04 C] [05 C]
        D[] [] [] [] [] []	D [00 D] [01 D] [02 D] [03 D] [04 D] [05 D]
        E[] [] [] [] [] []	E [00 E] [01 E] [02 E] [03 E] [04 E] [05 E]
        F[] [] [] [] [] []	F [00 F] [01 F] [02 F] [03 F] [04 F] [05 F]

        So, tile 09 G would be column 9, row G

	The coordinates of the currently highlighted tile are displayed next to the entry box, near the bottom-right of the window.


    SINGLE-TILE MODE:
        INSTRUCTIONS:
        This mode is designed as a complement to the multi-tile mode, and allows the user to quickly and easily get the coordinates of a box around a single tile.
        It is thus well-suited to defining single-tile items, such as a single creature in a screenshot, or a one-tile map feature (such as the Six-Day Stilt).
        If you wish to define a shape any larger or more complex than a single tile, use the multi-tile function.
        
	1. To draw these custom boxes, you must provide the coordinates of the single tile which you intend to draw a box around. There are 2 ways to do this:
		1. Manually typing the tile's coordinates into the entry box
        	   Using this method, the input for a box around the Six-Day Stilt would be:
		   05 C
		
		2. Moving one's mouse cursor over the tile and simply clicking on it. (Highly recommended)

	2. After providing these coordinates, the program will output the list of coordinate pairs for a rectangle around that tile.
	   (It will also copy those pairs into the user's clipboard)

	3. After outputting those pairs, the program will return to the mode select.
	

        SPECIAL COMMANDS:
        * None currently implemented

        EXTRA RULES / NOTES:
        * The program outputs corrdinates in a format suitable only for imagemap links which are specified to be rectangles.

    MULTI-TILE MODE:
        INSTRUCTIONS:
        This mode is designed to help draw multi-tile polygons for use in imagemaps which conform exactly to the grid used in Caves of Qud.
        
	1. To draw these polygons, you (again) must provide the program with tile coordinates. It will then use these coordinates (along with some context) to come up with a series of coordinate pair waypoints which stretch around the outside of the shape you define. As with single-tile mode, there are 2 methods for providing these tiles:
		1. Manually typing the tile coordinates into the entry box.
        	   Using this method, the first 5 inputs for a polygon around the Great Salt Desert seen on the world map (assuming one starts on the top-leftmost tile) would be:
        	   XX Y > 00 A
        	   XX Y > 08 A
        	   XX Y > 07 A
        	   XX Y > 07 C
        	   XX Y > 08 C

		2. Inputting your tiles by moving your mouse over the tile you want to input and clicking on it. (Again, highly recommended)
	
	2. Continue providing these tile coordinates, moving CLOCKWISE around the polygon you want an imagemap link for.
	   For a simple use case, inputting a large rectangle would require you to click, in order:
		1. the top-left corner
		2. the top-right corner
		3. the bottom-right corner
		4. the bottom-left corner

	  	[1][ ][ ][ ][2]
	  	[ ][ ][ ][ ][ ]
	  	[ ][ ][ ][ ][ ]
	   	[4][ ][ ][ ][3]
	
	   A few more complex examples are shown below:

	  	[1][ ][ ][2]      [6][5][7]
	  	[ ][ ][ ][ ]         [ ][ ]
	  	[ ][ ][ ][3][ ][ ][ ][4][ ]
	   	[9][ ][ ][ ][ ][ ][ ][ ][8]

	  	[01][02]    [05][06]        [09][  ][10]
	  	[  ][03][  ][04][  ]        [  ][  ][  ]
	  	[  ][  ][  ][18][07][  ][17][08][  ][  ]
	   	[  ][  ][  ][  ]        [16][15][12][11]
		[20][  ][  ][19]            [14][13]   

	  Finally, an additional example is also included in the download for this program, with an image showing the sequence of tiles one must click to outline the salt dunes.
	  [beta note, that example image is currently kind of jpeged to hell]
	
	3. To finish the shape, continue going clockwise around the polygon until you come back to the tile you started on. Input that first tile, then write "finish" in the entry box and press enter.


        SPECIAL COMMANDS:
        * Inputting "print" will give the current coordinate list.
        * Inputting "finish" will finish the current shape and return to mode select.
        * Inputting "delete" will delete the last point added to the line. (currently a WIP and doesn't work very well)
        * Inputting "clear" clear the coordinate list.

        EXTRA RULES / NOTES:
        * Keep in mind that the numbering for columns starts at 0, not 1.
        * You *need* to go clockwise around any polygon you want to draw.
        * When finishing a shape (by using the finish command), you must end on the same tile you began on, then input "finish"
        * Currently, the program does not handle diagonals well. It won't crash, but the imagemap will be wonky.


    OTHER GAMES:
        If, however improbably, you are using this program for something other than Caves of Qud, you will need to change a few things.
        This program assumes a 80x25 grid in which each tile is 16 pixels wide and 24 pixels tall, and you will need to change this.

        Open config.py in a text editor and change the lines that say

            tile_width = 16
            tile_height = 24

        to

            tile_width = (however many pixels wide each tile is)
            tile_height = (however many pixels tall each tile is)

        Also in config.py, change the lines that say

            grid_width = 80
            grid_height = 25

        to

            grid_width = (how many tiles wide a single screenshot of your game is)
            grid_height = (how many tiles tall a single screenshot of your game is)
