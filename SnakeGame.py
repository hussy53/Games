import random #Importing random number generator
import curses #Importing actions and different behaviours on the screen

s = curses.initscr() #Initialising the screen
curses.curs_set(0) #Cursor is not to be shown

sh, sw = s.getmaxyx() #Getting the max height and width of the initialised screen
w = curses.newwin(sh, sw, 0, 0) #Creating a new window starting at top left
                                #hand corner (0, 0)
w.keypad(1) #Accepts keypad input
w.timeout(100) #Refreshes the screen every 100 milliseconds

#Initial position of the snake (left-centered)
snk_x = int(sw/4)
snk_y = int(sh/2)

#Snake body parts
snake = [
    [snk_y, snk_x], #Head
    #[snk_y, snk_x - 1], #One left up the head
    #[snk_y, snk_x - 2sw] #Two left up the head

]

food = [int(sh/2), int(sw/2)] #Add the position of the initial food
w.addch(food[0], food[1], curses.ACS_PI) #The food added is PI

key = curses.KEY_RIGHT #Direct where initially will the snake move

while True:
    next_key = w.getch() #Get the next key
    key = key if next_key == -1 else next_key #Checks if the next key is either nothing (-1 or false)
                                              # or the next key

    #Checks if the game is lost either hits the top or side of the screen or itself
    if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
        curses.endwin() #Kill the window
        quit()

    #Creating a new head by taking the position of the old head
    new_head = [snake[0][0], snake[0][1]]

    #Which key is being clicked
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    #Inserting the new head
    snake.insert(0, new_head)

    if snake[0] == food: #Snake ran into the food
        food = None
        while food is None: #Select new food
            nf = [
                random.randint(1, sh - 1), #Within the height of the window
                random.randint(1, sw - 1) #Within the widht of the window
            ]
            food = nf if nf not in snake else None #If nf not in snake then create new food and
                                                #put it in the original food, then continue doing the loop
        w.addch(food[0], food[1], curses.ACS_PI) #add nf
    else:
        tail = snake.pop() #Remove the current tail
        w.addch(int(tail[0]), int(tail[1]), ' ') #Increase the tail length

    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD) #Update the new snake on the board
