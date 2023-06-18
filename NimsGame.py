from graphics import Canvas
import time
import random
import string
CANVAS_WIDTH = 750
CANVAS_HEIGHT = 650
"""
The proportions of the width and height of the canvas structures are based on the canvas width and height respectively to be able
change the size of the game without affecting the distribution. The font sizes are calculated based on the width of the canvas.
"""

PILE_SIZE = CANVAS_WIDTH // 5
STONES_SIZE = CANVAS_WIDTH // 12

MIDDLE_WIDTH = CANVAS_WIDTH / 2
MIDDLE_HEIGHT = CANVAS_HEIGHT / 2
FONT_SIZE_GAME_TITLE= int(CANVAS_WIDTH//12)
FONT_SIZE_TITLE = int(CANVAS_WIDTH // 20)
FONT_SIZE_SUBTITLE = int(CANVAS_WIDTH // 33)
FONT_SIZE_SELECTOR = int(CANVAS_WIDTH // 25)
FONT_SIZE_PILE = int(CANVAS_WIDTH // 17)
KEYPAD_NUMBERS_SIZE = CANVAS_WIDTH // 25
KEYPAD_LETTERS_SIZE = CANVAS_WIDTH / 12.5
STONES_PILE_HEIGHT = (CANVAS_HEIGHT / 3) + (((CANVAS_HEIGHT / 1.4285) - (CANVAS_HEIGHT / 3))/2)
PRESS_MOVE_X = CANVAS_WIDTH / 250
PRESS_MOVE_Y = CANVAS_WIDTH / 125



SELECTOR_WIDTH_LEFT= CANVAS_WIDTH // 6.6
SELECTOR_WIDTH_RIGHT = CANVAS_WIDTH // 1.538

DEEP_BLUE = "#00264d"
EARTHY_GREEN = "#6d8764"
NEUTRAL_GRAY = "#808080"
SUBTLE_GOLD = "#d6b86c"
COOL_TEAL = "#3d9998"

"""
This is an animated version of the game of Nim using the graphics library and without the use of the terminal.
Without counting the versions where the number of stones is different than 20, the game has 45 different variations 
depending on the choices of the user(s):
1.  It can be played with a friend or against the computer.
2.  If the user is playing against the computer, they need choose to play with either the mouse or the keyboard.
    If the user is playing with a friend, player1 will use the mouse and player2 will use the keyboard.
3.  You choose if the last player to remove a stone is either the looser or the winner of the game.
4.  You choose if each player can remove a maximum of 2 or 3 stones per turn.
5.  You choose if the player can go again if after their turn the pile is divisible by 3.

"""
def main():
    
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    opening_and_closing_slide(canvas, winner = None, stones_pile = None, slide_type = "opening")
    
    new_rules, bot_mode, first_player = main_screen(canvas)
    
    stones_pile, choose_last_is_winner, choose_max_3_stones, choose_if_divisible_by_3 = determine_rules_of_game(canvas, new_rules)
    
    player1, player2, mouse_or_keyboard = ask_for_names(canvas, first_player, bot_mode)
    
    create_game_screen(canvas, player1, player2, choose_last_is_winner, choose_max_3_stones, choose_if_divisible_by_3)
    
    current_player = play_game_algo(canvas, bot_mode, player1, player2, choose_max_3_stones, stones_pile, choose_if_divisible_by_3, mouse_or_keyboard)
    
    announce_winner(canvas, current_player, player1, player2, choose_last_is_winner, stones_pile)

class Stone:
    """
    This class will be used to create a circle that simulates a stone being removed from the pile.
    The circle will have a random color, move to a random direction and move with a random speed.
    The circle will be deleted once it has reached the border of the canvas.
    """
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.shape = canvas.create_oval(x, y, x + STONES_SIZE, y + STONES_SIZE, color)

    def move(self, direction):
        x_velocity, y_velocity = self.get_velocity(direction)
    
        while True:
            self.x += x_velocity
            self.y += y_velocity

            self.canvas.moveto(self.shape, self.x, self.y)
            time.sleep(0.01)
            
            if not self.is_within_canvas():
                break

        self.canvas.delete(self.shape)

    def get_velocity(self, direction):
        velocity_range = range(40, 60)
        velocities = {
            "right_bottom": (random.choice(velocity_range), random.choice(velocity_range)),
            "left_top": (-random.choice(velocity_range), -random.choice(velocity_range)),
            "right_top": (random.choice(velocity_range), -random.choice(velocity_range)),
            "left_bottom": (-random.choice(velocity_range), random.choice(velocity_range))
        }
        return velocities[direction]

    def is_within_canvas(self):
        return 0 < self.x < CANVAS_WIDTH and 0 < self.y < CANVAS_HEIGHT

def opening_and_closing_slide(canvas, winner, stones_pile, slide_type):
    """
    This function is used both at the begining and at the end of the game.
    It creates a canvas with a pile of stones in the middle and will simulate that a number of stones
    is being removed from the pile.
    Each time a stone is removed, the pile will show the number of stones remaining.
    If it's the begining of the game, the number of stones is 20 since it's the number from the standard
    game. However at the end of the game, it will be the number of stones selected in the options of the 
    game; it could be 20, 10, 55, etc.
    If it's the end of the game, it will erase everything and print "Game Over".
    """
    
    game_canvas = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, DEEP_BLUE)
    game_name = canvas.create_text(CANVAS_WIDTH/2, CANVAS_HEIGHT/16, font="Lunatoire", font_size= FONT_SIZE_GAME_TITLE, text="THE GAME OF NIM",
                                    color=SUBTLE_GOLD, anchor="center")
    canvas.create_oval(MIDDLE_WIDTH - PILE_SIZE / 2, MIDDLE_HEIGHT - PILE_SIZE / 2,
                       MIDDLE_WIDTH + PILE_SIZE / 2, MIDDLE_HEIGHT + PILE_SIZE / 2, "slategrey")
    
    if slide_type == "opening":
        stones_pile = 20
        text = "WELCOME"
    
    else:
        stones_pile = stones_pile
        text = f"{winner} wins!"
    
    bottom_sign = canvas.create_text(MIDDLE_WIDTH, (CANVAS_HEIGHT - (CANVAS_HEIGHT/16) + (CANVAS_HEIGHT//70) ), font = "Lunatoire", font_size = FONT_SIZE_GAME_TITLE, text = text, color = SUBTLE_GOLD, anchor = "center")
    
    stones_animation(canvas, stones_pile)
    
    if slide_type == "closing":
        
        time.sleep(0.5)
        game_over(canvas)

def stones_animation(canvas, stones_pile):
    """
    This creates the iteration based on the number of stones in the game and uses the class called Stone to create each circle, move them
    and delete them.
    The loop only will stop if the user clicks the canvas.
    """
    
    directions = ["left_top", "left_bottom", "right_top", "right_bottom"]
    
    for i in range(stones_pile+1):
        x = MIDDLE_WIDTH - STONES_SIZE / 2
        y = MIDDLE_HEIGHT - STONES_SIZE / 2
        colors = [EARTHY_GREEN, NEUTRAL_GRAY, COOL_TEAL, "white", SUBTLE_GOLD]
        color = random.choice(colors)
        stone = Stone(canvas, x, y, color)
        display_stones_number = canvas.create_text(MIDDLE_WIDTH, MIDDLE_HEIGHT, font="Arial", font_size=FONT_SIZE_PILE, text=str(stones_pile),
                                               color=DEEP_BLUE, anchor="center")
        direction = random.choice(directions)
        stone.move(direction)
        stones_pile -= 1
        canvas.delete(display_stones_number)
        if canvas.get_last_click() is not None:
            break

def next_slide(canvas):
    canvas.clear()
    game_canvas = canvas.create_rectangle(0,0, CANVAS_WIDTH, CANVAS_HEIGHT, DEEP_BLUE)

def main_screen(canvas):
    """
    Creates the main screen where the user will decide if they want to:
    - Change the rules
    - Play against a friend or the computer
        - And if the user selects against the computer, they will choose if they want to play first or second.
        
    The function first creates all the canvas structures, then checks for where the user is clicking to determine
    the fields selected and returns the rules values.
    """
    next_slide(canvas)
    print_standard_rules(canvas)
    choose_if_new_rules_canvas_left, choose_if_new_rules_canvas_right = ask_if_new_rules(canvas)
    choose_if_bot_mode_left, choose_if_bot_mode_right = ask_if_bot_mode(canvas)

    return check_for_clicks_main_screen(canvas, choose_if_new_rules_canvas_left, choose_if_new_rules_canvas_right, choose_if_bot_mode_left, choose_if_bot_mode_right)

def print_standard_rules(canvas):
    """
    Creates the text structures explaining the standard rules of the game. To have the same space size on each "line", there are variables
    holding the value of the first rule and the proportion of the space between each rule.
    """
    text_width = CANVAS_WIDTH // 25
    text_starting_height = CANVAS_HEIGHT // 4.21
    text_space_proportion = CANVAS_WIDTH // 25
    
    title_text = canvas.create_text(MIDDLE_WIDTH, CANVAS_HEIGHT // 16, font = "Lunatoire", font_size = FONT_SIZE_GAME_TITLE, text = "THE GAME OF NIM", color = SUBTLE_GOLD , anchor = "center")
    title_standard_rules = canvas.create_text(CANVAS_WIDTH // 25, CANVAS_HEIGHT // 5.714, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE + 1, text = "Welcome. The standard rules of the game are as follows:", color = "white", anchor = "w")
    text_rule1 = canvas.create_text(text_width, text_starting_height, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "1. The game starts with a pile of 20 stones between the players.", color = "white", anchor = "w")
    text_rule2 = canvas.create_text(text_width, text_starting_height + (text_space_proportion*1), font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "2. The two players alternate turns.", color = "white", anchor = "w")
    text_rule3 = canvas.create_text(text_width, text_starting_height + (text_space_proportion*2), font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "3. On a given turn, a player may take either 1 or 2 stones from the center pile.", color = "white", anchor = "w")
    text_rule4 = canvas.create_text(text_width, text_starting_height + (text_space_proportion*3), font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "4. The two players continue until the center pile has run out of stones.", color = "white", anchor = "w")
    text_rule5 = canvas.create_text(text_width, text_starting_height + (text_space_proportion*4), font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "5. The last player to take a stone loses.", color = "white", anchor = "w")


class BuildStructures:
    """
    Builds the text canvas structures and the rectangles acting as selection boxes.
    And when called returns the range of the boxes to be compared to the place where the user clicked.
    """
    
    def __init__(self, canvas, top_x, top_y, text, color):
        self.canvas = canvas
        self.top_x = top_x
        self.top_y = top_y
        self.bottom_x = self.top_x + CANVAS_WIDTH // 5
        self.bottom_y = self.top_y + CANVAS_HEIGHT // 13.3
        self.shape = canvas.create_rectangle(self.top_x,  self.top_y, self.bottom_x, self.bottom_y, NEUTRAL_GRAY, SUBTLE_GOLD)
        self.text = text
        self.color = color
        self.text_x = self.top_x + ((self.bottom_x - self.top_x)/2)
        self.text_y = self.top_y + ((self.bottom_y - self.top_y)/2)
        self.text_on_canvas = self.canvas.create_text(self.text_x, self.text_y, font = "Lunatoire", font_size = FONT_SIZE_SELECTOR, text= self.text, color = self.color, anchor = "center")
   
    def range_selector(self):
        return [(self.top_x, self.bottom_x), (self.top_y, self.bottom_y)]   
    
    def change_print_text(self, text, color):
        self.text = text
        self.color = color
        self.text_x = self.top_x + ((self.bottom_x - self.top_x)/2)
        self.text_y = self.top_y + ((self.bottom_y - self.top_y)/2)
        self.canvas.delete(self.text_on_canvas)
        self.text_on_canvas = self.canvas.create_text(self.text_x, self.text_y, font = "Lunatoire", font_size = FONT_SIZE_SELECTOR, text= self.text, color = self.color, anchor = "center")

def ask_if_new_rules(canvas):
    # Using the class BuildStructures creates the fields to select if the user wants to play the standard game or wants to play with different rules.
    choose_if_new_rules = canvas.create_text(MIDDLE_WIDTH, CANVAS_HEIGHT//1.9, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "Do you want to play the standard game or do you want to change some rules?", color = SUBTLE_GOLD, anchor = "center")
    selector_height = CANVAS_HEIGHT // 1.77
    
    choose_if_new_rules_canvas_left = BuildStructures(canvas, SELECTOR_WIDTH_LEFT, selector_height, "Standard", "white")
    choose_if_new_rules_canvas_right = BuildStructures(canvas, SELECTOR_WIDTH_RIGHT, selector_height, "Change", "white")

    return choose_if_new_rules_canvas_left, choose_if_new_rules_canvas_right
    
def ask_if_bot_mode(canvas):
    # Using the class BuildStructures creates the fields to select if the user wants to play against a friend or the computer.
    selector_height = CANVAS_HEIGHT // 1.379
    previous_selector_height = (CANVAS_HEIGHT // 1.77) + (CANVAS_HEIGHT // 13.3)
    middle_height = ((selector_height - previous_selector_height)/ 2) + previous_selector_height
    
    text_bot_mode = canvas.create_text(MIDDLE_WIDTH, middle_height, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "Do you want to play with a friend or against the computer?", color = SUBTLE_GOLD, anchor = "center")
    choose_if_bot_mode_left = BuildStructures(canvas, SELECTOR_WIDTH_LEFT, selector_height, "Friend","white")
    choose_if_bot_mode_right = BuildStructures(canvas, SELECTOR_WIDTH_RIGHT, selector_height, "Computer","white")
    
    return choose_if_bot_mode_left, choose_if_bot_mode_right
   
def check_for_clicks_main_screen(canvas, choose_if_new_rules_canvas_left, choose_if_new_rules_canvas_right, choose_if_bot_mode_left, choose_if_bot_mode_right):
    """
    First there are two areas that are of concern for the function, the first one is  the area related to the fields about new rules
    and the second one is the one about bot_mode.
    
    Having in mind canvas.get_last_click() returns a width and a height of the mouse in a tuple, to determine if the user clicked in 
    each area the program needs to compare if the click width is within the top_x, bottom_x of the area and if the click height is 
    within the top_y and bottom_y of the same area.
    
    To do the this, using the ranges of the areas and using the zip function, the function compares the first value of the tuple
    (width) and determines if the value is within the top_x and bottom_x of the area, and after that compares the second value (height)
    and determines if it is within the top_y and bottom_y of the same area.
    
    If both are true to the first area, this will call another function to obtain the answer about new rules. If both are true about the second one,
    it will call the one to obtain the answer about bot_mode.
    The aforementioned functions will also return the text canvas structures with the name of the box field and the color of the text in 
    case the user change their mind and want to select another one while the loop is still running.
    
    This sort of comparing will be widely used in the game each time the user is going to use the mouse to select something. 
    
    Once both new_rules and bot_mode have boolean values, if bot_mode is True it will call a new function to create the box field that will
    determine if the user plays first or second. 
    """
    new_rules = None
    bot_mode = None
    range_ask_if_bot_mode = [ (0, CANVAS_WIDTH), (CANVAS_HEIGHT // 1.6 , CANVAS_HEIGHT//1.176)] 
    range_ask_if_new_rules = [ (0, CANVAS_WIDTH), (CANVAS_HEIGHT//1.9, CANVAS_HEIGHT//1.6)]
    
    while new_rules is None or bot_mode is None:
        canvas.wait_for_click()

        click_main_screen = canvas.get_last_click()

        if all(start <= value <= end for (start, end), value in zip(range_ask_if_new_rules, click_main_screen)):
            new_rules, choose_if_new_rules_canvas_left, choose_if_new_rules_canvas_right = click_if_new_rules(canvas, new_rules, click_main_screen, choose_if_new_rules_canvas_left, choose_if_new_rules_canvas_right)
            
        elif all(start <= value <= end for (start, end), value in zip(range_ask_if_bot_mode, click_main_screen)):
            bot_mode, choose_if_bot_mode_left, choose_if_bot_mode_right = click_if_bot_mode(canvas, bot_mode, click_main_screen, choose_if_bot_mode_left, choose_if_bot_mode_right)
            
    if bot_mode is True and new_rules is not None:
        first_player = ask_who_plays_first(canvas)
    
    else:
        first_player = None
     
    return new_rules, bot_mode, first_player

def click_if_new_rules(canvas, new_rules, click_main_screen, choose_if_new_rules_canvas_left, choose_if_new_rules_canvas_right):
    # Using the strategy explained in check_for_clicks_main_screen(), returns the variables related to new_rules
    
    if all(start <= value <= end for (start, end), value in zip(choose_if_new_rules_canvas_left.range_selector(), click_main_screen)):
        if new_rules != None:
            choose_if_new_rules_canvas_right.change_print_text("Change", "white")
        new_rules = False
        choose_if_new_rules_canvas_left.change_print_text("Standard", DEEP_BLUE)
        
    if all(start <= value <= end for (start, end), value in zip(choose_if_new_rules_canvas_right.range_selector(), click_main_screen)):
        if new_rules != None:
            choose_if_new_rules_canvas_left.change_print_text("Standard", "white")
        new_rules = True
        choose_if_new_rules_canvas_right.change_print_text("Change", DEEP_BLUE)

    return new_rules, choose_if_new_rules_canvas_left, choose_if_new_rules_canvas_right

def click_if_bot_mode(canvas, bot_mode, click_main_screen, choose_if_bot_mode_left, choose_if_bot_mode_right ):
    # Using the strategy explained in check_for_clicks_main_screen(), returns the variables related to bot_mode
    if all(start <= value <= end for (start, end), value in zip(choose_if_bot_mode_left.range_selector(), click_main_screen)):
        if bot_mode != None:
            choose_if_bot_mode_right.change_print_text("Computer","white")
        bot_mode = False
        choose_if_bot_mode_left.change_print_text("Friend", DEEP_BLUE)
        
    if all(start <= value <= end for (start, end), value in zip(choose_if_bot_mode_right.range_selector(), click_main_screen)):
        if bot_mode != None:
            choose_if_bot_mode_left.change_print_text("Friend", "white")
        bot_mode = True
        choose_if_bot_mode_right.change_print_text("Computer",DEEP_BLUE)

    return bot_mode, choose_if_bot_mode_left, choose_if_bot_mode_right

def ask_who_plays_first(canvas):
    #   Using the class BuildStructures creates the fields to select if the user wants to play first or second when previously the user selected
    #   that they want to play against the computer
    selector_height = CANVAS_HEIGHT // 1.126
    previous_selector_height = (CANVAS_HEIGHT // 1.379) + (CANVAS_HEIGHT // 13.3)
    middle_height = ((selector_height - previous_selector_height)/ 2) + previous_selector_height
    computer_or_player_first = canvas.create_text(MIDDLE_WIDTH, middle_height, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "Do you want to be the first player to remove stones?", color = SUBTLE_GOLD, anchor = "center")
    
    choose_first_player_left = BuildStructures(canvas, SELECTOR_WIDTH_LEFT, selector_height, "Yes", "white")
    choose_first_player_right = BuildStructures(canvas, SELECTOR_WIDTH_RIGHT, selector_height, "No", "white")

    return click_who_plays_first_computer_vs_player(canvas, choose_first_player_left,choose_first_player_right )

def click_who_plays_first_computer_vs_player(canvas, choose_first_player_left,choose_first_player_right):
    # Using the strategy explained in check_for_clicks_main_screen(), returns the variables related to who plays first
    first_player = None
  
    while first_player is None:
        canvas.wait_for_click()
        click_main_screen = canvas.get_last_click()
        
        if all(start <= value <= end for (start, end), value in zip(choose_first_player_left.range_selector(), click_main_screen)):
            if first_player != None:
                choose_first_player_right.change_print_text("No", "white")
            first_player = "User"
            choose_first_player_left.change_print_text("Yes", DEEP_BLUE)
            break        
        if all(start <= value <= end for (start, end), value in zip(choose_first_player_right.range_selector(), click_main_screen)):
            if first_player != None:
                choose_first_player_left.change_print_text("Yes", "white")
            first_player = "Computer"
            choose_first_player_right.change_print_text("No", DEEP_BLUE)
                
    return first_player

def determine_rules_of_game(canvas, new_rules):
    """
    If the user chose to change the rules, the program will run other functions to determine the value of each rule. But if they chose to play
    the standard game, it will assign to each rule the standard values.
    """
    if new_rules is True:
        stones_pile, choose_last_is_winner, choose_max_3_stones, choose_if_divisible_by_3 = new_rules_screen(canvas)
        
    else:
        stones_pile = 20
        choose_last_is_winner = False
        choose_max_3_stones = False
        choose_if_divisible_by_3 = False
        
    return stones_pile, choose_last_is_winner, choose_max_3_stones, choose_if_divisible_by_3    

def new_rules_screen(canvas):
    """
    The new rules screen has 4 areas:
    1. Keypad to select the number of stones
    2. Selection boxes to choose if the last player to take a stone loses or wins.
    3. Selection boxes to choose the maximum number of stones a player can remove per turn.
    4. Selection boxes to choose if a player can again when the pile is divisible by 3 after their turn.
    """
    next_slide(canvas)
    title_text = canvas.create_text(MIDDLE_WIDTH, CANVAS_HEIGHT// 16, font = "Lunatoire", font_size = FONT_SIZE_TITLE, text = "New rules", color = SUBTLE_GOLD , anchor = "center")
    keypad_numbers_dict = choose_no_stones(canvas)
    choose_last_is_winner_canvas_left, choose_last_is_winner_canvas_right = choose_last_is_winner_rule(canvas)
    choose_max_3_stones_canvas_left, choose_max_3_stones_canvas_right  = choose_max_3_stones_rule(canvas)
    choose_if_divisible_by_3_canvas_left, choose_if_divisible_by_3_canvas_right = choose_if_divisible_by_3_rule(canvas)
   
    return check_for_clicks_new_rules(canvas, choose_last_is_winner_canvas_left, choose_last_is_winner_canvas_right , choose_max_3_stones_canvas_left, choose_max_3_stones_canvas_right , choose_if_divisible_by_3_canvas_left, choose_if_divisible_by_3_canvas_right, keypad_numbers_dict)

class Number:
    """
    Creates a key number that will act as a key of the keypad.
    
    Note: The order of the file's name corresponds to each number between 1 and 9 with ".png" at the end.
    10, corresponds to "delete", 11 to "0" and 12 belongs to "stop".
    """
    def __init__(self, canvas, top_x, top_y, new_file_number):
        self.canvas = canvas
        self.top_x = top_x
        self.top_y = top_y
        self.new_file_number = new_file_number
        self.size = KEYPAD_NUMBERS_SIZE
        self.bottom_x = self.top_x + self.size
        self.bottom_y = self.top_y + self.size
        self.text_number = self.text_in_key()
        self.square_color = "white" if self.text_number not in ["Back", "Done"] else NEUTRAL_GRAY
        self.square = canvas.create_rectangle(top_x, top_y, self.bottom_x, self.bottom_y, self.square_color, SUBTLE_GOLD)
        self.font_size = FONT_SIZE_SUBTITLE if self.text_number not in ["Back", "Done"] else 12
        self.text_x = (self.top_x + self.bottom_x) / 2
        self.text_y = (self.top_y + self.bottom_y) / 2
        self.text_color = SUBTLE_GOLD if self.text_number in ["Back", "Done"] else DEEP_BLUE
        self.text = canvas.create_text(self.text_x, self.text_y, text = self.text_number, font_size = self.font_size , color = self.text_color, anchor = "center")
    
    # Determines the text that will be on the key
    def text_in_key(self):
        if self.new_file_number == 10:
            return "Back"
        elif self.new_file_number == 11:
            return "0"
        elif self.new_file_number == 12:
            return "Done"
        else:
            return str(self.new_file_number)
    
    # Returns the range of the key number        
    def range(self):
        return [(self.top_x, self.bottom_x), (self.top_y, self.bottom_y)]
    
    # Moves the key number and returns the number or string associated with it.       
    def press(self):
        self.canvas.move(self.square, PRESS_MOVE_X, PRESS_MOVE_Y)
        self.canvas.set_hidden(self.text, True)
        self.new_color = SUBTLE_GOLD if self.text_color == DEEP_BLUE else DEEP_BLUE
        self.move_text = self.canvas.create_text(self.text_x + PRESS_MOVE_X, self.text_y + PRESS_MOVE_Y, text = self.text_number, font_size = self.font_size, color = self.new_color , anchor = "center")
        time.sleep(0.1)
        self.canvas.move(self.square, -PRESS_MOVE_X, -PRESS_MOVE_Y)
        self.canvas.delete(self.move_text)
        self.canvas.set_hidden(self.text, False)
        
        if self.new_file_number == 10:
            return "delete"
        elif self.new_file_number == 11:
            return "0"
        elif self.new_file_number == 12:
            return "stop"
        else:
            return str(self.new_file_number)    

def choose_no_stones(canvas):
    # Creates the keypad to select the number of stones in the game and stores each key number with its range in a dictionary
    pile_stones_text= canvas.create_text(MIDDLE_WIDTH, CANVAS_HEIGHT // 8, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "How many stones do you want to have in the game?:        ", color = SUBTLE_GOLD , anchor = "center")
    canvas.create_text(MIDDLE_WIDTH, CANVAS_HEIGHT // 6.5, font = "Lunatoire", font_size = int(CANVAS_WIDTH // 41.66) , text = "Remember to press ¨Done¨", color = "white" , anchor = "center")
    last_file_number = 0
    keypad_numbers_dict = {} 
    top_x = CANVAS_WIDTH / 2.6
    top_y = CANVAS_HEIGHT / 5.8
    for i in range (4):
        for i in range (3):
            new_file_number = last_file_number + 1
            key_number = Number(canvas, top_x, top_y, new_file_number)
            keypad_numbers_dict[key_number] = key_number.range()
            top_x += CANVAS_WIDTH / 12.5
            last_file_number = new_file_number
            
        top_y = top_y + CANVAS_HEIGHT / 13.3
        top_x = CANVAS_WIDTH / 2.6

    return keypad_numbers_dict    

def choose_last_is_winner_rule(canvas):
    # Using the BuildStructures class creates selection boxes to choose if the last player to take a stone loses or wins.
    
    selector_height = CANVAS_HEIGHT // 1.77
    canvas.create_text(MIDDLE_WIDTH, CANVAS_HEIGHT//1.9, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "The one who takes the last stones is the:", color = SUBTLE_GOLD, anchor = "center")
    choose_last_is_winner_canvas_left = BuildStructures(canvas, SELECTOR_WIDTH_LEFT, selector_height, "Loser", "white")
    choose_last_is_winner_canvas_right = BuildStructures(canvas, SELECTOR_WIDTH_RIGHT, selector_height, "Winner", "white")
    
    return choose_last_is_winner_canvas_left, choose_last_is_winner_canvas_right

def choose_max_3_stones_rule(canvas):
    # Using the BuildStructures class creates selection boxes to choose the maximum number of stones a player can remove per turn.
    
    selector_height = CANVAS_HEIGHT // 1.379
    previous_selector_height = (CANVAS_HEIGHT // 1.77) + (CANVAS_HEIGHT // 13.3)
    middle_height = ((selector_height - previous_selector_height)/ 2) + previous_selector_height
    choose_max_3_stones_question = canvas.create_text(MIDDLE_WIDTH, middle_height, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "What is the maximum stones that can be removed per turn?", color = SUBTLE_GOLD, anchor = "center")
    
    choose_max_3_stones_canvas_left = BuildStructures(canvas, SELECTOR_WIDTH_LEFT, selector_height, "Two", "white")
    choose_max_3_stones_canvas_right = BuildStructures(canvas, SELECTOR_WIDTH_RIGHT, selector_height, "Three", "white")
    
    return choose_max_3_stones_canvas_left, choose_max_3_stones_canvas_right

def choose_if_divisible_by_3_rule(canvas):
    # Using the BuildStructures class creates selection boxes to choose if a player can again when the pile is divisible by 3 after their turn
    selector_height = CANVAS_HEIGHT // 1.126
    previous_selector_height = (CANVAS_HEIGHT // 1.379) + (CANVAS_HEIGHT // 13.3)
    middle_height = ((selector_height - previous_selector_height)/ 2) + previous_selector_height
    choose_if_divisible_by_3_question = canvas.create_text(MIDDLE_WIDTH, middle_height, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "If the pile is divisible by 3, the player should go again?", color = SUBTLE_GOLD, anchor = "center")
    
    choose_if_divisible_by_3_canvas_left = BuildStructures(canvas, SELECTOR_WIDTH_LEFT, selector_height, "No", "white")
    choose_if_divisible_by_3_canvas_right = BuildStructures(canvas, SELECTOR_WIDTH_RIGHT, selector_height, "Yes", "white")
    
    return choose_if_divisible_by_3_canvas_left, choose_if_divisible_by_3_canvas_right

def divisible_by_3(stones_pile):
    # Checks if the number of stones in the pile is divisible by 3
    return stones_pile != 0 and stones_pile % 3 == 0 

def check_for_clicks_new_rules(canvas, choose_last_is_winner_canvas_left, choose_last_is_winner_canvas_right , choose_max_3_stones_canvas_left, choose_max_3_stones_canvas_right , choose_if_divisible_by_3_canvas_left, choose_if_divisible_by_3_canvas_right, keypad_numbers_dict):
    """
    Using the strategy explained in check_for_clicks_main_screen(), depending on the location of the click, this will call the function
    related to the field where the user clicked.
    Until all of the new rules have been assigned the loop will keep running allowing the user to also change their mind about one or more 
    of the rules when at least one of the rules is empty.
    """
    title_no_stones = None
    no_stones = []
    no_stones_complete = False
    choose_last_is_winner = None
    choose_max_3_stones = None
    choose_if_divisible_by_3 = None
    range_choose_no_stones = [ (0, CANVAS_WIDTH), (0, CANVAS_HEIGHT // 1.9)]
    range_last_is_winner_rule = [ (0, CANVAS_WIDTH), (CANVAS_HEIGHT//1.9, CANVAS_HEIGHT//1.6)]
    range_max_3_stones_rule =  [ (0, CANVAS_WIDTH), (CANVAS_HEIGHT // 1.6 , CANVAS_HEIGHT//1.176)] 
    range_if_divisible_by_3_rule = [ (0, CANVAS_WIDTH), (CANVAS_HEIGHT // 1.38, CANVAS_HEIGHT)] 
    
    while no_stones_complete is False or choose_last_is_winner is None or choose_max_3_stones is None or choose_if_divisible_by_3 is None:
        canvas.wait_for_click()
            
        click_new_rules = canvas.get_last_click()
  
        if all(start <= value <= end for (start, end), value in zip(range_choose_no_stones, click_new_rules)):
            no_stones_complete, title_no_stones, no_stones = click_no_stones (canvas, no_stones, click_new_rules, title_no_stones, no_stones_complete, keypad_numbers_dict )
            continue            
        elif all(start <= value <= end for (start, end), value in zip(range_last_is_winner_rule, click_new_rules)):
            choose_last_is_winner, choose_last_is_winner_canvas_left, choose_last_is_winner_canvas_right = click_last_is_winner(canvas, choose_last_is_winner, click_new_rules, choose_last_is_winner_canvas_left, choose_last_is_winner_canvas_right)
            continue
        elif all(start <= value <= end for (start, end), value in zip(range_max_3_stones_rule, click_new_rules)):
            choose_max_3_stones,  choose_max_3_stones_canvas_left, choose_max_3_stones_canvas_right = click_max_3_stones(canvas, choose_max_3_stones, click_new_rules,  choose_max_3_stones_canvas_left, choose_max_3_stones_canvas_right)
            continue        
        elif all(start <= value <= end for (start, end), value in zip(range_if_divisible_by_3_rule, click_new_rules)):
            choose_if_divisible_by_3, choose_if_divisible_by_3_canvas_left, choose_if_divisible_by_3_canvas_right = click_if_divisible_by_3(canvas, choose_if_divisible_by_3, click_new_rules, choose_if_divisible_by_3_canvas_left, choose_if_divisible_by_3_canvas_right)
    
    full_no_stones = "".join(no_stones)
    stones_pile = int(full_no_stones)
    
    return stones_pile, choose_last_is_winner, choose_max_3_stones, choose_if_divisible_by_3

def click_no_stones(canvas, no_stones, click_new_rules, title_no_stones, no_stones_complete, keypad_numbers_dict):
    """
    Checks for the location of the click, moves the key number associated with that click and prints the number
    The keypad only will stop adding numbers when:
    1. The user pressed the "done" key and at least a number greater tan zero has been selected
    2. The length of the stones number is greater than 3 (this means the maximum possible number of stones is 9999 )
    The delete key can be used even after having pressed the done key before when at least one other rule 
    is still empty.
    """
    new_number = None
    
    if no_stones_complete is False:
        for range_key, range_value in keypad_numbers_dict.items():
            if all(start <= value <= end for (start, end), value in zip(range_value, click_new_rules)):
                new_number = Number.press(range_key)
                break
            
        if new_number == "0" and len(no_stones) == 0:
            new_number = None
            
        elif new_number == "stop":
            if len(no_stones) == 0:
                new_number = None
            else:    
                no_stones_complete = True
        
        elif new_number == "delete" and len(no_stones)>= 1:
            no_stones.pop()
    
        if new_number not in ["stop", "delete", None]:
            no_stones.append(new_number)
            if len(no_stones) > 3:
                no_stones_complete = True
                
    else:
        if all(start <= value <= end for (start, end), value in zip(list(keypad_numbers_dict.values())[-3], click_new_rules)):
            no_stones_complete = False
            new_number = Number.press(list(keypad_numbers_dict.keys())[-3])
            no_stones.clear()
    
    title_no_stones, full_no_stones = display_number(canvas, no_stones, title_no_stones)
    
    return no_stones_complete, title_no_stones, no_stones

def display_number(canvas, no_stones, title_no_stones):
    #prints the stones number in the canvas
    if title_no_stones is not None:
        canvas.delete(title_no_stones)
        
    full_no_stones = "".join(no_stones)
    
    title_no_stones = canvas.create_text(CANVAS_WIDTH //1.234, CANVAS_HEIGHT// 8, font = "Lunatoire", font_size = FONT_SIZE_PILE, text = full_no_stones, color = "white", anchor = "w")
        
    return title_no_stones, full_no_stones
        
def click_last_is_winner(canvas, choose_last_is_winner, click_new_rules, choose_last_is_winner_canvas_left, choose_last_is_winner_canvas_right):
    # Using the strategy explained in check_for_clicks_main_screen(), returns the variables related to who wins the game with respect to
    # who takes the last stone.
    if all(start <= value <= end for (start, end), value in zip(choose_last_is_winner_canvas_left.range_selector(), click_new_rules)):
        if choose_last_is_winner != None:
            choose_last_is_winner_canvas_right.change_print_text("Winner","white")
        choose_last_is_winner = False
        choose_last_is_winner_canvas_left.change_print_text("Loser",DEEP_BLUE)
        
    if all(start <= value <= end for (start, end), value in zip(choose_last_is_winner_canvas_right.range_selector(), click_new_rules)):
        if choose_last_is_winner != None:
            choose_last_is_winner_canvas_left.change_print_text("Loser","white")
        choose_last_is_winner = True
        choose_last_is_winner_canvas_right.change_print_text("Winner",DEEP_BLUE)
        
    return choose_last_is_winner, choose_last_is_winner_canvas_left, choose_last_is_winner_canvas_right

def click_max_3_stones(canvas, choose_max_3_stones, click_new_rules, choose_max_3_stones_canvas_left, choose_max_3_stones_canvas_right):
    # Using the strategy explained in check_for_clicks_main_screen(), returns the variables related to the maximum number of stones
    # than can be removed per turn.    
    if all(start <= value <= end for (start, end), value in zip(choose_max_3_stones_canvas_left.range_selector(), click_new_rules)):
        if choose_max_3_stones != None:
            choose_max_3_stones_canvas_right.change_print_text("Three", "white")
        choose_max_3_stones = False
        choose_max_3_stones_canvas_left.change_print_text("Two", DEEP_BLUE)
        
    if all(start <= value <= end for (start, end), value in zip(choose_max_3_stones_canvas_right.range_selector(), click_new_rules)):
        if choose_max_3_stones != None:
            choose_max_3_stones_canvas_left.change_print_text("Two", "white")
        choose_max_3_stones = True
        choose_max_3_stones_canvas_right.change_print_text("Three", DEEP_BLUE)
  
    return choose_max_3_stones, choose_max_3_stones_canvas_left, choose_max_3_stones_canvas_right
    
def click_if_divisible_by_3(canvas, choose_if_divisible_by_3, click_new_rules, choose_if_divisible_by_3_canvas_left, choose_if_divisible_by_3_canvas_right):
    # Using the strategy explained in check_for_clicks_main_screen(), returns the variables related to the possibility to have another turn
    # if the pile is divisible by 3 
    if all(start <= value <= end for (start, end), value in zip(choose_if_divisible_by_3_canvas_left.range_selector(), click_new_rules)):
        if choose_if_divisible_by_3 != None:
            choose_if_divisible_by_3_canvas_right.change_print_text("Yes", "white")
        choose_if_divisible_by_3 = False
        choose_if_divisible_by_3_canvas_left.change_print_text("No", DEEP_BLUE)
                
    if all(start <= value <= end for (start, end), value in zip(choose_if_divisible_by_3_canvas_right.range_selector(), click_new_rules)):
        if choose_if_divisible_by_3 != None:
            choose_if_divisible_by_3_canvas_left.change_print_text("No", "white")
        choose_if_divisible_by_3 = True
        choose_if_divisible_by_3_canvas_right.change_print_text("Yes", DEEP_BLUE)
              
    return choose_if_divisible_by_3, choose_if_divisible_by_3_canvas_left, choose_if_divisible_by_3_canvas_right

def ask_for_names(canvas, first_player, bot_mode):
    """
    If bot_mode is True, the program will:
    1. Ask the user if they want to play with the keyboard or the mouse
    2. Ask for their name
    If bot_mode is False, the program ask for the names of both players
    """
    if bot_mode is True:
        mouse_or_keyboard = ask_mouse_or_keyboard(canvas) 
        player1, player2 = create_alphabet_bot_mode_true(canvas, first_player, mouse_or_keyboard)
    else:
        mouse_or_keyboard = None
        player1, player2 = create_alphabet_bot_mode_false(canvas, mouse_or_keyboard)
    
    return player1, player2, mouse_or_keyboard    

def ask_mouse_or_keyboard(canvas):
    # Asks the user if they want to use the mouse or the keyboard in the game
    next_slide(canvas)
    half_of_rectangle_height = (CANVAS_HEIGHT / 13.3)/2

    choose_mouse_or_keyboard = canvas.create_text(MIDDLE_WIDTH, MIDDLE_HEIGHT - half_of_rectangle_height*2, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE + 1, text = "Do you want to use the mouse or the keyboard?", color = SUBTLE_GOLD, anchor = "center")
    game_name = canvas.create_text(MIDDLE_WIDTH, CANVAS_HEIGHT/13.333, font="Lunatoire", font_size = FONT_SIZE_GAME_TITLE, text="THE GAME OF NIM",
                                    color=SUBTLE_GOLD, anchor="center")    
    choose_mouse_or_keyboard_left = BuildStructures(canvas, SELECTOR_WIDTH_LEFT, MIDDLE_HEIGHT - half_of_rectangle_height, "Mouse", "white")
    choose_mouse_or_keyboard_right = BuildStructures(canvas, SELECTOR_WIDTH_RIGHT, MIDDLE_HEIGHT - half_of_rectangle_height, "Keyboard", "white") 
    
    return clicks_mouse_or_keyboard(canvas, choose_mouse_or_keyboard_left, choose_mouse_or_keyboard_right)

def clicks_mouse_or_keyboard(canvas, choose_mouse_or_keyboard_left, choose_mouse_or_keyboard_right):
    # Using the strategy explained in check_for_clicks_main_screen(), returns the variable with either mouse or keyboard as values
    mouse_or_keyboard = None
    
    while mouse_or_keyboard is None:
        canvas.wait_for_click()
    
        click_main_screen = canvas.get_last_click()
    
        if all(start <= value <= end for (start, end), value in zip(choose_mouse_or_keyboard_left.range_selector(), click_main_screen)):
            if mouse_or_keyboard is not None:
                choose_mouse_or_keyboard_right.change_print_text("Keyboard", "white")
            mouse_or_keyboard = "Mouse"
            choose_mouse_or_keyboard_left.change_print_text("Mouse",  DEEP_BLUE)
                    
        if all(start <= value <= end for (start, end), value in zip(choose_mouse_or_keyboard_right.range_selector(), click_main_screen)):
            if mouse_or_keyboard is not None:
                choose_mouse_or_keyboard_left.change_print_text("Mouse",  "white")
            mouse_or_keyboard = "Keyboard"
            choose_mouse_or_keyboard_right.change_print_text("Keyboard", DEEP_BLUE)
                
    return mouse_or_keyboard

class Letters:
    """ 
    Creates a key letter for the alphabet keypad. The file name is the name of the letter plus ".png"
    
    Note: the name of the files and the letters values are the same from a to z. However, "|" has the value "delete",
    "}" is " " and "~" is "stop".
    
    """
    def __init__(self, canvas, top_x, top_y, new_letter):
        self.canvas = canvas
        self.top_x = top_x
        self.top_y = top_y
        self.size = KEYPAD_LETTERS_SIZE
        self.bottom_x = self.top_x + self.size
        self.bottom_y = self.top_y + self.size
        self.new_letter = new_letter
        self.box_color = "white" if self.new_letter not in ["|", "}", "~" ] else NEUTRAL_GRAY
        self.shape = canvas.create_rectangle(self.top_x, self.top_y, self.bottom_x , self.bottom_y, self.box_color, SUBTLE_GOLD)
        self.text_color = DEEP_BLUE if self.new_letter not in ["|", "}", "~" ] else SUBTLE_GOLD
        self.text_letter = self.text_in_key()
        self.text_x = (self.top_x + self.bottom_x) / 2
        self.text_y = (self.top_y + self.bottom_y) / 2
        self.text = canvas.create_text(self.text_x, self.text_y, text = self.text_letter, font_size = FONT_SIZE_SUBTITLE, color = self.text_color , anchor = "center")
    
    # Determines the text that will be on the key
    def text_in_key(self):
        if self.new_letter == "{":
            return " "
        if self.new_letter == "|":
            return "Back"
        elif self.new_letter  == "}":
            return "_"
        elif self.new_letter == "~":
            return "Done"
        else:
            return self.new_letter.capitalize()
    
    # Returns the range of the key letter
    def range(self):
        return [(self.top_x, self.bottom_x), (self.top_y, self.bottom_y)]

    def press(self):
        self.change_color = SUBTLE_GOLD if self.text_color == DEEP_BLUE else DEEP_BLUE
        self.canvas.move(self.shape, PRESS_MOVE_X, PRESS_MOVE_Y)
        self.canvas.set_hidden(self.text, True)
        self.move_text = self.canvas.create_text(self.text_x + PRESS_MOVE_X, self.text_y + PRESS_MOVE_Y, text = self.text_letter, font_size = FONT_SIZE_SUBTITLE, color = self.change_color, anchor = "center")
        time.sleep(0.01)
        self.canvas.move(self.shape, -PRESS_MOVE_X, -PRESS_MOVE_Y)
        self.canvas.delete (self.move_text)
        self.canvas.set_hidden(self.text, False)
        
        if self.new_letter == "|":
            return "delete"
        elif self.new_letter  == "}":
            return " "
        elif self.new_letter == "~":
            return "stop"
        elif self.new_letter == "{":
            return None
        else:
            return self.new_letter    
    
def build_letters_keypad(canvas):
    #Creates the loop that builds the alphabet keypad and returns each letter as a key and the range as its value in a dictionary
    keypad_alphabet_dict = {}
    top_x = CANVAS_WIDTH / 16.666
    top_y = CANVAS_HEIGHT / 4.8192
    counter = 0
    for i in range (5):
        for i in range (6):
            letter_key = Letters(canvas, top_x, top_y, chr(ord('a') + counter))
            top_x += CANVAS_WIDTH /6.25
            counter += 1
            keypad_alphabet_dict[letter_key] = letter_key.range()
        top_y = top_y + CANVAS_HEIGHT / 7.547
        top_x = CANVAS_WIDTH / 16.666
    
    return  keypad_alphabet_dict      

def create_alphabet_bot_mode_true(canvas, first_player, mouse_or_keyboard): 
    """
    Creates the screen with the titles and the keypad to write the name of the user and depending if they chose mouse or keyboard
    as their preferred way to play, it will print a reminder
    
    If the user wanted to play first, player1 will be the name of the user and player 2 will be computer. Otherwise it will be the
    other way around
    """
    next_slide(canvas)
    title_text = canvas.create_text(CANVAS_WIDTH / 25, CANVAS_HEIGHT / 8, font = "Lunatoire", font_size = FONT_SIZE_SELECTOR, text = "Your name is: ", color = SUBTLE_GOLD, anchor = "w")
    player = None
    keypad_alphabet_dict = build_letters_keypad(canvas)
    
    if mouse_or_keyboard == "Mouse":
        reminder_text = "You chose to use the mouse in the game. Remember to press ¨Done¨"
    elif mouse_or_keyboard == "Keyboard":
        reminder_text = "You chose to use the keyboard in the game. Remember to press ¨Enter¨"
        
    reminder = canvas.create_text(MIDDLE_WIDTH, CANVAS_HEIGHT / 1.081, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = reminder_text, color = SUBTLE_GOLD, anchor = "center")
    
    if first_player == "User":
        player1 = write_name(canvas, keypad_alphabet_dict, player, mouse_or_keyboard)
        while player1 == "Computer":
            player1 = write_name(canvas, keypad_alphabet_dict, player, mouse_or_keyboard)
        player2 = "Computer"
        
        
    elif first_player == "Computer":
        player1 = "Computer"
        player2 = write_name(canvas, keypad_alphabet_dict, player, mouse_or_keyboard)
        while player2 == "Computer":
            player2 = write_name(canvas, keypad_alphabet_dict, player, mouse_or_keyboard)
        
    return player1, player2
    
def create_alphabet_bot_mode_false(canvas, mouse_or_keyboard):
    # This is one is called when the user is playing with a friend so the users take turns to write their names.
    # If the second player writes the same name of the first one, it will print the same screen until both are different
    next_slide(canvas)
    
    player1 = create_alphabet_player1(canvas, mouse_or_keyboard)
    
    next_slide(canvas)
    
    player2 = create_alphabet_player2(canvas, mouse_or_keyboard)
    
    while player2 == player1:
        next_slide(canvas)
        player2 = create_alphabet_player2(canvas, mouse_or_keyboard)
        
    return player1, player2

def create_alphabet_player1(canvas, mouse_or_keyboard):
    # Creates the screen with the keypad and the titles to write the name of the first player
    title_text = canvas.create_text(CANVAS_WIDTH / 25, CANVAS_HEIGHT / 8, font = "Lunatoire", font_size = FONT_SIZE_SELECTOR, text = "The name of the first player is: ", color = SUBTLE_GOLD, anchor = "w")
    canvas.create_text(MIDDLE_WIDTH, CANVAS_HEIGHT / 1.081, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "You will use the mouse in the game. Remember to press ¨Done¨", color = SUBTLE_GOLD, anchor = "center")
    player = "player1"
    
    keypad_alphabet_dict = build_letters_keypad(canvas)
    
    player1 = write_name(canvas, keypad_alphabet_dict, player, mouse_or_keyboard)
   
    return player1
    
def create_alphabet_player2(canvas, mouse_or_keyboard):
    # Creates the screen with the keypad and the titles to write the name of the second player
    title_text = canvas.create_text(CANVAS_WIDTH/ 25, CANVAS_HEIGHT/8 , font = "Lunatoire", font_size = FONT_SIZE_SELECTOR, text = "The name of the second player is: ", color = SUBTLE_GOLD, anchor = "w")
    canvas.create_text(MIDDLE_WIDTH, CANVAS_HEIGHT / 1.081, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = "You will use the keyboard in the game. Remember to press ¨Enter¨", color = SUBTLE_GOLD, anchor = "center")
    player = "player2"
    keypad_alphabet_dict = build_letters_keypad(canvas)
    
    player2 = write_name(canvas, keypad_alphabet_dict, player, mouse_or_keyboard)
    
    return player2

def write_name(canvas, keypad_alphabet_dict, player, mouse_or_keyboard):
    """
    If mouse_or_keyboard is not None, means bot_mode is True. Hence, it will use either the mouse or the keyboard
    depending on the selection of the user.
    However if mouse_or_keyboard is None, means the user is playing with a friend and the first player to write their name
    will use the mouse and the second one will use the keyboard in the game
    
    """
    if mouse_or_keyboard == "Mouse":
        return name_with_mouse(canvas, mouse_or_keyboard, keypad_alphabet_dict)
    elif mouse_or_keyboard == "Keyboard":
        return name_with_keyboard(canvas, mouse_or_keyboard, keypad_alphabet_dict)
   
    else:
        if player == "player1":
            return name_with_mouse(canvas, mouse_or_keyboard, keypad_alphabet_dict)
            
        elif player == "player2":
            return name_with_keyboard(canvas, mouse_or_keyboard, keypad_alphabet_dict)

def name_with_mouse(canvas, mouse_or_keyboard, keypad_alphabet_dict):
    """
    Using the strategy explained in check_for_clicks_main_screen(), it will check which letter key is clicked 
    and add it to the name.
    
    The loop will end if the name are 12 letters or more or if the player clicked "done". However that key will have no effect if there are no letters in the name.
    The key called "{" is a blank space in the keypad to make it more uniform so if pressed will have no effect.
    The name of the player cannot be "Computer" so it will keep showing the keypad until a different name is given.
    Every time a letter key is clicked, it will move to make it more realistic.  
    """
    name = []
    title_name = None
    new_letter = None
    full_name = None
    
    while new_letter != "stop":
        
        click_mouse_alphabet = canvas.get_last_click()
        if click_mouse_alphabet is not None:
        
            for letter_key, letter_range in keypad_alphabet_dict.items():
                if all(start <= value <= end for (start, end), value in zip(letter_range, click_mouse_alphabet)):
                    new_letter = Letters.press(letter_key)
                    if new_letter == " " and not name:
                        new_letter = None
                    break
            
            if new_letter not in [None, "delete", "stop"]:
                name.append(new_letter)
                new_letter = None
                if len(name) > 15:
                    break        
                
            elif new_letter == "delete" and len(name) >= 1:
                name.pop()
                            
            elif new_letter == "stop":
                if not name:
                    new_letter = None
                    continue
                if full_name == "Computer":
                    new_letter = None
                    name.clear()
                    
            else:
                continue
                
            full_name, title_name = display_name(canvas, name, title_name, mouse_or_keyboard)    
                        
    return full_name
        

def name_with_keyboard(canvas, mouse_or_keyboard, keypad_alphabet_dict):
    """
    Each key of keypad_alphabet_dict is a canvas structure for each of the letters from the keypad and they have access to "self.new_letter" which is the 
    variable containing the letter printed in the key and the values are the ranges. To be able to use each letter: 
    1. A list was created containing each of the keys of the keypad_alphabet_dict.
    2. The new keys of the letters_dict will be the letters using the self.new_letter from each of the keys.
    3. The values of the letters_dict will be the variables holding the canvas structures from the Letters class.
    Note: the old dictionary keys are now the dictionary values.
    Note 2: The symbols used for "Enter", " ", and "Backspace" are the automatic characters assigned by Python when the counter goes over the letter "z".
    
    Since canvas.get_last_key_press() will return a letter, that letter can be used to call it as it was self.new_letter
    and use the press function from the Letters class.
    The process is:
    - letters_dict[self.new_letter] = canvas_structure from Letters class
    - If canvas.get_last_key_press() = self.new_letter:
        letter_dict[self.new_letter] = letter_dict[canvas.get_last_key_press()]
    
    Once it has found the letter it will move the keypad letter using letter_dict[canvas.get_last_key_press()] calling Letters.press().
    
    The loop will end if the name are 12 letters or more or if the player pressed "enter". However that key will have no effect if there are no letters in the name.
    The function will only add letters from the a to z whether lowercase or not, and the keys " ", "Backspace" or "Enter".
    
    The name of the player cannot be "Computer" so it will keep showing the keypad until a different name is given.
    Every time a letter key is pressed, it will move to make it more realistic. 
    
    """
    name = []
    title_name = None
    new_letter = None
    full_name = None
    letters_dict = {letter_key.new_letter: letter_key for letter_key in list(keypad_alphabet_dict.keys())}
    
    while new_letter != "stop":
        
        click_keyboard_alphabet = canvas.get_last_key_press()
        
        if click_keyboard_alphabet is not None:
        
            if click_keyboard_alphabet.lower() in string.ascii_lowercase or click_keyboard_alphabet in [" ", "Backspace", "Enter"]:
                
                if click_keyboard_alphabet.lower() in string.ascii_lowercase:
                    new_letter = Letters.press(letters_dict[click_keyboard_alphabet.lower()])
                
                elif click_keyboard_alphabet == "Enter":
                    new_letter = Letters.press(letters_dict["~"])
                    
                elif click_keyboard_alphabet == " ":
                    if len(name) == 0:
                        new_letter = None
                        continue
                    else:    
                        new_letter = Letters.press(letters_dict["}"]) 
                
                elif click_keyboard_alphabet == "Backspace":
                    new_letter = Letters.press(letters_dict["|"])
                
            else:
                new_letter = None
                continue
                  
            if new_letter not in [None, "delete", "stop"]:
                name.append(new_letter)
                new_letter = None
                if len(name) > 15:
                    break 
            
            elif new_letter == "delete" and len(name) >= 1:
                name.pop()
            
            elif new_letter == "stop":
                if not name:
                    new_letter = None
                    continue
                if full_name == "Computer":
                    new_letter = None
                    name.clear()
                        
            full_name, title_name = display_name(canvas, name, title_name, mouse_or_keyboard)
        
    return full_name

def display_name(canvas, name, title_name, mouse_or_keyboard):
    # Displays the name capitalized so the first letter will always be uppercase and the other letters will be lower case.
    # When there is a space, the first letter of the new word will follow the same rule
    
    if title_name != None:
        canvas.delete(title_name)
    
    if len(name) > 0:
        full_name = "".join(name).title()
        if mouse_or_keyboard is not None:
            title_name = canvas.create_text(CANVAS_WIDTH / 3.3333, CANVAS_HEIGHT / 8, font = "Lunatoire", font_size = FONT_SIZE_SELECTOR, text = full_name, color = "white", anchor = "w")
        else:
            title_name = canvas.create_text(CANVAS_WIDTH / 1.666, CANVAS_HEIGHT / 8, font = "Lunatoire", font_size = FONT_SIZE_SELECTOR, text = full_name, color = "white", anchor = "w")
    else:
        full_name = None
    return full_name, title_name
  
def create_game_screen(canvas, player1, player2, choose_last_is_winner, choose_max_3_stones, choose_if_divisible_by_3):
    """
    Creates the game screen showing all the canvas structures whether figures or text. It includes all the values that will act as rules in the 
    game depending on the selection of the user(s).
    """
    next_slide(canvas)
    half_of_stones_pile_size = (CANVAS_WIDTH/3.84) / 2
    font_size_main_titles = int(CANVAS_WIDTH // 35.7142)
    font_size_print_statements = int(CANVAS_WIDTH // 38.4615)
    text_width = CANVAS_WIDTH * 0.02
    
    title_text = canvas.create_text(MIDDLE_WIDTH, CANVAS_HEIGHT / 13.3333, font = "Lunatoire", font_size = FONT_SIZE_GAME_TITLE, text = "THE GAME OF NIM", color = SUBTLE_GOLD , anchor = "center")
    rules_canvas = canvas.create_rectangle (0,CANVAS_HEIGHT / 8, CANVAS_WIDTH, CANVAS_HEIGHT / 3, EARTHY_GREEN)
    stones_canvas =canvas.create_oval (MIDDLE_WIDTH - half_of_stones_pile_size, STONES_PILE_HEIGHT - half_of_stones_pile_size, MIDDLE_WIDTH + half_of_stones_pile_size, STONES_PILE_HEIGHT + half_of_stones_pile_size, "slategrey")
 
    player1_canvas = canvas.create_rectangle (CANVAS_WIDTH * 0.02, CANVAS_HEIGHT / 1.4285, CANVAS_WIDTH / 2.2727, CANVAS_HEIGHT * 0.98, NEUTRAL_GRAY, SUBTLE_GOLD)
    player2_canvas = canvas.create_rectangle (CANVAS_WIDTH / 1.818, CANVAS_HEIGHT / 1.4285 , CANVAS_WIDTH * 0.98 , CANVAS_HEIGHT * 0.98, NEUTRAL_GRAY, SUBTLE_GOLD)
    text_player1 = canvas.create_text (CANVAS_WIDTH / 4.5454, CANVAS_HEIGHT / 1.3333, font = "Lunatoire", font_size = FONT_SIZE_SELECTOR, text = player1, color = "white", anchor = "center")   
    text_player2 = canvas.create_text(CANVAS_WIDTH // 1.3157, CANVAS_HEIGHT / 1.3333, font = "Lunatoire", font_size = FONT_SIZE_SELECTOR, text = player2, color = "white", anchor = "center")
    rules = canvas.create_text(text_width, CANVAS_HEIGHT / 6.4516, font = "Lunatoire", font_size = font_size_main_titles, text = "Active rules", color = SUBTLE_GOLD, anchor = "w")
    rule_3 = canvas.create_text(CANVAS_WIDTH * 0.02, CANVAS_HEIGHT / 4.8192, font = "Lunatoire" , font_size = font_size_print_statements, text = "The last player to take a stone wins:", color = "white", anchor = "w")
    rule_3_answer = canvas.create_text(MIDDLE_WIDTH - CANVAS_WIDTH / 15 , CANVAS_HEIGHT / 4.8192 , font = "Lunatoire" , font_size = font_size_main_titles, text = str(choose_last_is_winner), color = DEEP_BLUE, anchor = "center")
    rule_4 = canvas.create_text(text_width, CANVAS_HEIGHT / 3.9215, font = "Lunatoire" , font_size = font_size_print_statements, text = "Maximum 3 stones removed per turn:", color = "white", anchor = "w")
    rule_4_answer = canvas.create_text(MIDDLE_WIDTH - CANVAS_WIDTH / 20, CANVAS_HEIGHT / 3.9215, font = "Lunatoire" , font_size = font_size_main_titles, text = str(choose_max_3_stones), color = DEEP_BLUE, anchor = "center")
    rule_5 = canvas.create_text(text_width, CANVAS_HEIGHT / 3.2786, font = "Lunatoire" , font_size = font_size_print_statements, text = "Player can go again if after their turn the pile is divisible by 3: ", color = "white", anchor = "w")
    rule_5_answer = canvas.create_text(CANVAS_WIDTH /1.48, CANVAS_HEIGHT / 3.2786, font = "Lunatoire" , font_size = font_size_main_titles, text = str(choose_if_divisible_by_3), color = DEEP_BLUE, anchor = "w")

def play_game_algo (canvas, bot_mode, player1, player2, choose_max_3_stones, stones_pile, choose_if_divisible_by_3, mouse_or_keyboard):
    """ 
    The major differences in the game depend on whether the bot_mode is True or not. When it's false, the program will have to check for clicks
    or pressed keys on each turn. When it's true it will only check for clicks or pressed keys on the turn of the user depending if they're playing
    as player1 or player2
    """
    if bot_mode is False:
        return check_for_removed_stones_player_vs_player(canvas, player1, player2, choose_max_3_stones, stones_pile, choose_if_divisible_by_3, mouse_or_keyboard)
    
    elif bot_mode is True:
        return check_for_removed_stones_player_vs_computer(canvas, player1, player2, choose_max_3_stones, stones_pile, choose_if_divisible_by_3, mouse_or_keyboard)
   
def check_for_removed_stones_player_vs_player(canvas, player1, player2, choose_max_3_stones, stones_pile, choose_if_divisible_by_3, mouse_or_keyboard):
    # When the user is playing with a friend, they will take turns to remove stones and print the respective signs in the canvas.
    current_player = player1
    text_stones_player1 = None
    text_stones_player2 = None

    while stones_pile >= 1:
        stones_text = canvas.create_text(MIDDLE_WIDTH, STONES_PILE_HEIGHT, font = "Lunatoire", font_size = FONT_SIZE_GAME_TITLE , text = str(stones_pile), color = "white", anchor = "center")
        
        if current_player == player1:
            
            stones_pile, current_player, text_stones_player1 = turn_player1(canvas, stones_pile, current_player, player2, choose_max_3_stones, choose_if_divisible_by_3, mouse_or_keyboard, text_stones_player1)
            
        elif current_player == player2:
            
            stones_pile, current_player, text_stones_player2 = turn_player2(canvas, stones_pile, current_player, player1, choose_max_3_stones, choose_if_divisible_by_3, mouse_or_keyboard,  text_stones_player2)
            
        canvas.delete(stones_text)
    
    return current_player

class StonesToRemove:
    """
    Creates the stones that will be pressed, clicked or move by the computer on each turn.
    Depending on the number of stones in the pile ant the max 3 stones rule, it will print 
    either 1, 2 or 3 stones.
    """
    def __init__ (self, canvas, stones_pile, choose_max_3_stones, player, text_stones):
        self.canvas = canvas
        self.stones_pile = stones_pile
        self.choose_max_3_stones = choose_max_3_stones
        self.player = player
        self.text_stones = text_stones
        self.size = CANVAS_WIDTH / 33.333
        self.top_y = CANVAS_HEIGHT / 1.223
        self.bottom_y = self.top_y + self.size
        self.prompt_y = CANVAS_HEIGHT / 1.194
        self.turn_y = CANVAS_HEIGHT / 1.081
        self.divisible_y = CANVAS_HEIGHT / 1.081
        
        if self.text_stones is not None:
            self.canvas.delete(self.text_stones)
        
        if self.player == "player1":
            self.player_1()
        
        else:
            self.player_2() 
        
        if self.stones_pile == 1:
            self.text = "Stone to remove:"
        else:
            self.text = "Stones to remove:"
        
        self.print_structures()
    
    # Depending on the turn of each player it will create the stones on the left or the right.    
    def player_1(self):    
        self.prompt_x = CANVAS_WIDTH / 25
        self.turn_x = CANVAS_WIDTH / 4.5454
        self.top_x_1 = CANVAS_WIDTH / 3.5714
        self.top_x_2 = CANVAS_WIDTH / 3.125
        self.top_x_3 = CANVAS_WIDTH / 2.777
        self.divisible_x = CANVAS_WIDTH /4.5454
        
    def player_2(self):
        self.prompt_x =  CANVAS_WIDTH / 1.7543
        self.turn_x =  CANVAS_WIDTH / 1.3157
        self.top_x_1 = CANVAS_WIDTH / 1.2345
        self.top_x_2 = CANVAS_WIDTH / 1.1764
        self.top_x_3 = CANVAS_WIDTH / 1.12359
        self.divisible_x = CANVAS_WIDTH / 1.3157
    
    def print_structures(self):
        self.text_x_1 = ((self.top_x_1 * 2) + self.size) / 2
        self.text_x_2 = ((self.top_x_2 * 2) + self.size) / 2
        self.text_x_3 = ((self.top_x_3 * 2) + self.size) / 2
        self.text_y = (((self.top_y * 2) + self.size) / 2) + 2
        self.print_statement = self.canvas.create_text(self.prompt_x, self.prompt_y, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = self.text, color = DEEP_BLUE, anchor = "w")
        self.your_turn = self.canvas.create_text(self.turn_x, self.turn_y , font = "Lunatoire", font_size = int(CANVAS_WIDTH / 27.777), text = "IT'S YOUR TURN", color = SUBTLE_GOLD, anchor = "center") 
        self.stone1 = self.canvas.create_rectangle(self.top_x_1, self.top_y, self.top_x_1 + self.size, self.bottom_y,  "white", DEEP_BLUE)
        self.text_stone1 = self.canvas.create_text(self.text_x_1, self.text_y, text = "1",  font_size = FONT_SIZE_SUBTITLE, color = DEEP_BLUE, anchor = "CENTER")
        if self.stones_pile >= 2:
            self.stone2 = self.canvas.create_rectangle(self.top_x_2, self.top_y, self.top_x_2 + self.size, self.bottom_y,  "white", DEEP_BLUE)
            self.text_stone2 = self.canvas.create_text(self.text_x_2, self.text_y, text = "2", font_size = FONT_SIZE_SUBTITLE, color = DEEP_BLUE, anchor = "center")
        else:
            self.stone2 = None

        if self.choose_max_3_stones is True and self.stones_pile >= 3:
            self.stone3 = self.canvas.create_rectangle(self.top_x_3, self.top_y, self.top_x_3 + self.size, self.bottom_y,  "white", DEEP_BLUE)
            self.text_stone3 = self.canvas.create_text(self.text_x_3, self.text_y, text = "3", font_size = FONT_SIZE_SUBTITLE, color = DEEP_BLUE, anchor = "center")        
        else:
            self.stone3 = None
            
    # Deletes the sign that shows which player has their turn
    def delete_your_turn(self):
        self.canvas.delete(self.your_turn)
    
    # Deletes all the canvas structures of the player including the stones, the "your turn" sign and the "it's divisible by 3" sign
    def delete_structures(self):
        self.canvas.delete(self.print_statement)
        self.canvas.delete(self.stone1)
        self.canvas.delete(self.text_stone1)
        if self.your_turn is not None:
            self.canvas.delete(self.your_turn)
        if self.stone2 is not None:
            self.canvas.delete(self.stone2)
            self.canvas.delete(self.text_stone2)
        if self.stone3 is not None:
            self.canvas.delete(self.stone3)
            self.canvas.delete(self.text_stone3)
    
        if self.divisible_by_3 is not None:
            time.sleep(0.2)
            self.canvas.delete(self.divisible_by_3)
    
    # Returns the range of the stone called in the function.
    def ranges(self, stone_no):
        self.stone_no = stone_no
        if self.stone_no == "stone1" or self.stone_no == self.stone1:
            self.top_x = self.top_x_1
        elif self.stone_no == "stone2" or self.stone_no == self.stone2:
            self.top_x = self.top_x_2
        elif self.stone_no == "stone3" or self.stone_no == self.stone3:
            self.top_x = self.top_x_3
            
        self.bottom_x = self.top_x + self.size
        return [(self.top_x, self.bottom_x), (self.top_y, self.bottom_y)]
    
    # Moves the key of the stone and returns it's value
    def press_stone1(self):
        self.press_movement(self.stone1)
        return 1

    def press_stone2(self):
        self.press_movement(self.stone2)
        return 2
        
    def press_stone3(self): 
        self.press_movement(self.stone3)
        return 3
    
    # Only moves the key of the stone(used when the computer is playing)
    def press_movement(self, stone_no):
        self.stone_no = stone_no
        self.text_no = self.determine_square()
        self.canvas.set_hidden(self.text_no, True)
        self.text_x = self.determine_x()
        self.text_pressed = self.determine_text()
        self.canvas.move(self.stone_no, PRESS_MOVE_X , PRESS_MOVE_Y)
        self.moved_text = self.canvas.create_text(self.text_x + PRESS_MOVE_X, self.text_y + PRESS_MOVE_Y, text = self.text_pressed, font_size = FONT_SIZE_SUBTITLE, color = SUBTLE_GOLD, anchor = "center")
        time.sleep(0.1)
        self.canvas.move(self.stone_no, -PRESS_MOVE_X, -PRESS_MOVE_Y)
        self.canvas.delete(self.moved_text)
        self.canvas.set_hidden(self.text_no, False)
    
    def determine_x(self):
        if self.stone_no == "stone1" or self.stone_no == self.stone1:
            return self.text_x_1
        elif self.stone_no == "stone2" or self.stone_no == self.stone2:
            return self.text_x_2
        elif self.stone_no == "stone3" or self.stone_no == self.stone3:
            return self.text_x_3
            
    def determine_square(self):  
        if self.stone_no == "stone1" or self.stone_no == self.stone1:
            return self.text_stone1
        elif self.stone_no == "stone2" or self.stone_no == self.stone2:
            return self.text_stone2
        elif self.stone_no == "stone3" or self.stone_no == self.stone3:
            return self.text_stone3
        
    def determine_text(self):
        if self.stone_no == "stone1" or self.stone_no == self.stone1:
            return "1"
        elif self.stone_no == "stone2" or self.stone_no == self.stone2:
            return "2"
        elif self.stone_no == "stone3" or self.stone_no == self.stone3:
            return "3"
            
    # Prints the "it's divisible by 3" sign  
    def print_divisible_by_3(self, option):
        self.option = option
        if self.option is True:
            self.divisible_by_3 = self.canvas.create_text(self.divisible_x, self.divisible_y, font = "Lunatoire", font_size = int(CANVAS_WIDTH//27.7777), text = "The pile is divisible by 3", color = SUBTLE_GOLD, anchor = "center")
        else:
            self.divisible_by_3 = None

def turn_player1(canvas, stones_pile, current_player, player2, choose_max_3_stones, choose_if_divisible_by_3, mouse_or_keyboard, text_stones_player1):
    """
    1. Creates on the left side on the canvas the keys of the stones to remove and the text showing that it's player1's turn.
    2. Then checks for which key was pressed
    3. If the rule about the pile being divisible by 3 is True and in fact the condition is met in the game, prints a sign and doesn't changes the current player.
    If the rule is False or the condition is not met, changes the current player to player2
    4. Print the number of stones removed
    """
    player = "player1"
    
    keypad_stones = StonesToRemove(canvas, stones_pile, choose_max_3_stones, player, text_stones_player1)
    stones_pile, stones_player1 = check_for_clicks_player1(canvas, stones_pile, current_player, keypad_stones, choose_max_3_stones, mouse_or_keyboard)
    
    if divisible_by_3(stones_pile) is True and choose_if_divisible_by_3 is True:
        keypad_stones.delete_your_turn()
        keypad_stones.print_divisible_by_3(True)
    else:
        keypad_stones.print_divisible_by_3(False)
        current_player = player2 
    
    keypad_stones.delete_structures()
    text_stones_player1 = canvas.create_text(CANVAS_WIDTH/ 25, CANVAS_HEIGHT / 1.1940, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = f"Stones removed: {stones_player1}", color = DEEP_BLUE, anchor = "w")
    
    return stones_pile, current_player, text_stones_player1

def turn_player2(canvas, stones_pile, current_player, player1, choose_max_3_stones, choose_if_divisible_by_3, mouse_or_keyboard,  text_stones_player2):
    """
    1. Creates on the right side on the canvas the keys of the stones to remove and the text showing that it's player2's turn.
    2. Then checks for which key was pressed
    3. If the rule about the pile being divisible by 3 is True and in fact the condition is met in the game, prints a sign and doesn't changes the current player.
    If the rule is False or the condition is not met, changes the current player to player1
    4. Print the number of stones removed
    """
    player = "player2"
    keypad_stones = StonesToRemove(canvas, stones_pile, choose_max_3_stones, player, text_stones_player2)

    stones_pile, stones_player2 = check_for_clicks_player2(canvas, stones_pile, player, keypad_stones, choose_max_3_stones, mouse_or_keyboard)
    
    if divisible_by_3(stones_pile) and choose_if_divisible_by_3:
        keypad_stones.delete_your_turn()
        keypad_stones.print_divisible_by_3(True)
    else:
        keypad_stones.print_divisible_by_3(False)
        current_player = player1 
    
    keypad_stones.delete_structures()
    text_stones_player2 = canvas.create_text(CANVAS_WIDTH / 1.7543, CANVAS_HEIGHT / 1.1940, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE , text = f"Stones removed: {stones_player2}", color = DEEP_BLUE, anchor = "w")
            
    return stones_pile, current_player, text_stones_player2
    
def check_for_clicks_player1(canvas, stones_pile, current_player, keypad_stones, choose_max_3_stones, mouse_or_keyboard):
    """
    Using the strategy explained in check_for_clicks_main_screen(), it will check which key from the left side was clicked or which key was pressed.
    
    If the mouse_or_keyboard is None, this means that bot_mode is False, then it ill use the mouse since player1 will always use 
    the mouse when playing against a friend.
    
    Since this function is also used when bot_mode is True, then it depends on the selection about mouse_or_keyboard.
    
    Whether the player uses the mouse or the keyboard to play, the function will move the corresponding key and return
    the respective number that belongs to it and will subtract this number from the pile.
    """
    stones_player1 = None
    
    while stones_player1 is None:
    
        if mouse_or_keyboard is None or mouse_or_keyboard == "Mouse":
            canvas.wait_for_click()
            click_player1 = canvas.get_last_click()
            
            if all(start <= value <= end for (start, end), value in zip(keypad_stones.ranges("stone1"),  click_player1)):
                stones_player1 = keypad_stones.press_stone1()
                                
            elif all(start <= value <= end for (start, end), value in zip(keypad_stones.ranges("stone2"), click_player1)):
                if stones_pile >= 2: 
                    stones_player1 = keypad_stones.press_stone2()
                        
            elif choose_max_3_stones is True and stones_pile >=3:            
                if all(start <= value <= end for (start, end), value in zip(keypad_stones.ranges("stone3"), click_player1)):
                    stones_player1 = keypad_stones.press_stone3()
        else:
            key_press_player1 = canvas.get_last_key_press()
            
            if key_press_player1 is not None:
                if key_press_player1 == "1":
                    stones_player1 = keypad_stones.press_stone1()
                               
                elif key_press_player1 == "2" and stones_pile >= 2:
                    stones_player1 = keypad_stones.press_stone2()
                    
                elif choose_max_3_stones is True and key_press_player1 == "3" and stones_pile >=3:
                    stones_player1 = keypad_stones.press_stone3()
              
    time.sleep(0.1)
    stones_pile = stones_pile - stones_player1    
    
    return stones_pile, stones_player1

def check_for_clicks_player2(canvas, stones_pile, current_player, keypad_stones, choose_max_3_stones, mouse_or_keyboard):
    """
    Using the strategy explained in check_for_clicks_main_screen(), it will check which key from the right side was clicked or which key was pressed.
    
    If the mouse_or_keyboard is None, this means that bot_mode is False, then it ill use the mouse since player2 will always use 
    the mouse when playing against a friend.
    
    Since this function is also used when bot_mode is True, then it depends on the selection about mouse_or_keyboard.
    
    Whether the player uses the mouse or the keyboard to play, the function will move the corresponding key and return
    the respective number that belongs to it and will subtract this number from the pile.
    
    """
    stones_player2 = None
    
    while stones_player2 is None:

        if mouse_or_keyboard is None or mouse_or_keyboard == "Keyboard":
            key_press_player2 = canvas.get_last_key_press()
                    
            if  key_press_player2 == "1":
                stones_player2 = keypad_stones.press_stone1()
                           
            elif key_press_player2 == "2" and stones_pile >=2:
                stones_player2 = keypad_stones.press_stone2()
                
            elif choose_max_3_stones is True and key_press_player2 == "3" and stones_pile >= 3:
                stones_player2 = keypad_stones.press_stone3()
        
        elif mouse_or_keyboard == "Mouse":
            canvas.wait_for_click()
            click_player2_mouse = canvas.get_last_click()
        
            if all(start <= value <= end for (start, end), value in zip(keypad_stones.ranges("stone1"), click_player2_mouse)):
                stones_player2 = keypad_stones.press_stone1()
                        
            elif all(start <= value <= end for (start, end), value in zip(keypad_stones.ranges("stone2"), click_player2_mouse)):
                if stones_pile >= 2:
                    stones_player2 = keypad_stones.press_stone2()
                    
            elif choose_max_3_stones is True and stones_pile >= 3:            
                if all(start <= value <= end for (start, end), value in zip(keypad_stones.ranges("stone3"), click_player2_mouse)):
                    stones_player2 = keypad_stones.press_stone3()
                  
    time.sleep(0.1)
    stones_pile = stones_pile - stones_player2

    return stones_pile, stones_player2

def check_for_removed_stones_player_vs_computer(canvas, player1, player2, choose_max_3_stones, stones_pile, choose_if_divisible_by_3, mouse_or_keyboard):
    """
    When the user is playing against the computer, they will take turns to remove stones and print the respective signs in the canvas.
    
    Since the computer can be either player1 or player2 depending on the selection in the main screen, it will use different variables when calling the turn_computer function,
    and it could be either text_stones_player1 or text_stones_player2.
    
    With respect to the user, depending if they're player1 or player2 it will call the corresponding function.
    
    While the number of stones in the pile is equal or larger than 1, it will:
    1. Print the number of stones in the pile.
    2. If it's not none deletes the text structure showing the number of stones that were removed by the player in the previous turn.
    3. Update the number of stones in the pile after the subtraction 
    4. Update the current player
    5. Delete the number of stones in the pile
    """
    current_player = player1
    text_stones_player1 = None
    text_stones_player2 = None
  
    while stones_pile >= 1:
        stones_text = canvas.create_text(MIDDLE_WIDTH, STONES_PILE_HEIGHT, font = "Lunatoire", font_size = FONT_SIZE_GAME_TITLE + 10, text = str(stones_pile), color = "white", anchor = "center", )
        
        if current_player == "Computer":
            if current_player == player1:
                stones_pile, current_player, text_stones_player1 = turn_computer(canvas, current_player, choose_max_3_stones, player1, player2, stones_pile, text_stones_player1, choose_if_divisible_by_3)
            else:
                stones_pile, current_player, text_stones_player2 = turn_computer(canvas, current_player, choose_max_3_stones, player1, player2, stones_pile, text_stones_player2, choose_if_divisible_by_3)
        
        else:
            if current_player == player1:
                if text_stones_player1 is not None:
                    canvas.delete(text_stones_player1)
                stones_pile, current_player, text_stones_player1 = turn_player1(canvas, stones_pile, current_player, player2, choose_max_3_stones, choose_if_divisible_by_3, mouse_or_keyboard, text_stones_player1)
            else:
                if text_stones_player2 is not None:
                    canvas.delete(text_stones_player2)
                stones_pile, current_player, text_stones_player2 = turn_player2(canvas, stones_pile, current_player, player1, choose_max_3_stones, choose_if_divisible_by_3, mouse_or_keyboard,  text_stones_player2)
        
        canvas.delete(stones_text)
    
    return current_player

def turn_computer(canvas, current_player, choose_max_3_stones, player1, player2, stones_pile, text_stones, choose_if_divisible_by_3):
    """
    It is used whether the computer is playing as player1 or player 2.
    1.  Creates the keys that correspond to 1, 2 or 3 stones to be removed depending on the choose_max_3_stones rule and the stones remaining in the pile
    2.  Calls the function that selects the number of stones to remove and subtracts it from the pile of stones
    3.  If the rule related to the pile being divisible by 3 and the condition is met, deletes the "your turn" sign and print the one with "it's divisible by 3".
        Otherwise changes the current_player to the other one.
    4.  Deletes all the structures canvas    
    """
    if current_player == player1:
        player = "player1"
    elif current_player == player2:
        player = "player2"
        
    keypad_stones = StonesToRemove(canvas, stones_pile, choose_max_3_stones, player, text_stones)

    stones_pile, stones_removed = computer_chooses_stones(canvas, choose_max_3_stones, stones_pile, keypad_stones)
    
    stones_pile = stones_pile - stones_removed
    
    if divisible_by_3(stones_pile) is True and choose_if_divisible_by_3 is True:
        keypad_stones.delete_your_turn()
        keypad_stones.print_divisible_by_3(True)
    else:
        keypad_stones.print_divisible_by_3(False)
        if current_player == player1:
            current_player = player2
        else:
            current_player = player1 
    
    keypad_stones.delete_structures()
    
    if player == "player1":
        text_stones = canvas.create_text(CANVAS_WIDTH/ 25, CANVAS_HEIGHT / 1.1940, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE, text = f"Stones removed: {stones_removed}", color = DEEP_BLUE, anchor = "w")
    else:
        text_stones = canvas.create_text(CANVAS_WIDTH / 1.7543, CANVAS_HEIGHT / 1.1940, font = "Lunatoire", font_size = FONT_SIZE_SUBTITLE , text = f"Stones removed: {stones_removed}", color = DEEP_BLUE, anchor = "w")
                

    return stones_pile, current_player, text_stones    

def computer_chooses_stones(canvas, choose_max_3_stones, stones_pile, keypad_stones): 
    """
    1.  The function sleep from the time library is used to give a sense of "thinking" while the program chooses a random number.
        The time it waits to give the result it's also random to be more realistic since people take different time to
        decide in each opportunity.
    
    2.  The values for the random number selection will vary depending on the choose_max_3_stones and the stones on the pile.
    
    3.  Once the random number is chosen, the program will use the class StonesToRemove to be able to move the key corresponding
        to the chosen number.
    
    4. It will return the subtraction of the random number from the stones pile.    
        
    """
    time.sleep(random.uniform(0.5, 2))
        
    if choose_max_3_stones is False:
        if stones_pile > 1:
            values = [1, 2]
            stones_removed = random.choice(values)
            
        elif stones_pile == 1:
            stones_removed = 1
    
    elif choose_max_3_stones is True:
        if stones_pile >= 3:
            values = [1, 2, 3]
            stones_removed = random.choice(values)
            
        elif stones_pile == 2:
            values = [1, 2]
            stones_removed = random.choice(values)
         
        elif stones_pile == 1:   
            stones_removed = 1
        
    if stones_removed == 1:
        keypad_stones.press_movement(keypad_stones.stone1)
    elif stones_removed == 2:    
        keypad_stones.press_movement(keypad_stones.stone2)
    elif stones_removed == 3:
        keypad_stones.press_movement(keypad_stones.stone3)
    
    time.sleep(0.1)
    keypad_stones.delete_your_turn()
  
    return stones_pile, stones_removed

def announce_winner(canvas, current_player, player1, player2, choose_last_is_winner, stones_pile):
    # Depending on the selection of the rule related to the winner, it will announce the corresponding player and show the closing animation.
    if choose_last_is_winner:
        winner = player2 if current_player == player1 else player1
    else:
        winner = current_player
            
    opening_and_closing_slide(canvas, winner, stones_pile, slide_type = "closing")
    
def game_over(canvas):
    #Prints game over
    next_slide(canvas)
    game_canvas = canvas.create_rectangle(0,0, CANVAS_WIDTH, CANVAS_HEIGHT, DEEP_BLUE)
    canvas.create_text(MIDDLE_WIDTH, MIDDLE_HEIGHT, font = "Lunatoire", font_size = FONT_SIZE_GAME_TITLE, text = "GAME OVER", color = SUBTLE_GOLD , anchor = "center")

if __name__ == '__main__':
    main()



    




