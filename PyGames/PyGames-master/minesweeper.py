import pygame
import sys
import random
import os

# creates game and sets the menu
WIDTH = 60
HEIGHT = 60
SIZE = 10
MARGIN = 5
MENU_SIZE = 40
LEFT_CLICK = 1
RIGHT_CLICK = 3
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Class that holds the game logic          
class Game:
    def __init__(self):
        # Creates grid
        self.grid = [[self.Cell(x, y) for x in range(SIZE)] for y in range(SIZE)]
        self.init = False
        self.game_lost = False
        self.game_won = False
        self.num_bombs = 10
        self.squares_x = SIZE
        self.squares_y = SIZE
        self.resize = False
        self.flag_count = 0

    def draw(self):
    # Set the screen background color
        screen.fill(BLACK)
    # Draw the grid
        for row in range(self.squares_y):
         for column in range(self.squares_x):
            color = WHITE
            if self.grid[row][column].is_visible:
                if self.grid[row][column].contains_bomb:
                        color = RED
                else:
                    color = GRAY
            elif self.grid[row][column].contains_flag:
                color = BLUE
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN + MENU_SIZE,
                              WIDTH,
                              HEIGHT])
            self.grid[row][column].show_text()

        
    # Adjusts the grid when the screen size has changed
    def adjust_grid(self, sizex, sizey):
        global screen
        self.squares_x = (sizex - MARGIN) // (WIDTH + MARGIN)
        self.squares_y = (sizey - MARGIN - MENU_SIZE) // (HEIGHT + MARGIN)
        if self.squares_x < 8:
            self.squares_x = 8
        if self.squares_y < 8:
            self.squares_y = 8
        if self.num_bombs > (self.squares_x * self.squares_y) // 3:
            self.num_bombs = self.squares_x * self.squares_y // 3
        self.grid = [[self.Cell(x, y) for x in range(self.squares_x)] for y in range(self.squares_y)]
        size = ((self.squares_x*(WIDTH + MARGIN) + MARGIN), (self.squares_y*(HEIGHT + MARGIN) + MARGIN + MENU_SIZE))
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    # Reveal bombs 
    def end_game(self):
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                if self.grid[row][column].contains_bomb:
                    self.grid[row][column].is_visible = True
                self.grid[row][column].contains_flag = False

    # Changes the number of bombs
    def change_num_bombs(self, bombs):
        self.num_bombs += bombs
        if self.num_bombs < 1:
            self.num_bombs = 1
        elif self.num_bombs > (self.squares_x * self.squares_y) // 3:
            self.num_bombs = self.squares_x * self.squares_y // 3
        self.restart() 

    # Puts bombs in random locations 
    def set_bomb(self, row, column):
        bombplaced = 0
        while bombplaced < self.num_bombs:
            x = random.randrange(self.squares_y)
            y = random.randrange(self.squares_x)
            if not self.grid[x][y].contains_bomb and not (row == x and column == y):
                self.grid[x][y].contains_bomb = True
                bombplaced += 1
        self.total_bombs()
        if self.grid[row][column].bomb_count != 0:
            self.restart()
            self.set_bomb(row, column)
        
    # Count all bombs 
    def total_bombs(self):
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                self.grid[row][column].count_bombs(self.squares_y, self.squares_x)
    
    # Restarts game
    def restart(self):
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                self.init = False
                self.grid[row][column].is_visible = False
                self.grid[row][column].contains_bomb = False
                self.grid[row][column].bomb_count = 0
                self.grid[row][column].test = False
                self.grid[row][column].contains_flag = False
                self.game_lost = False
                self.game_won = False
                self.flag_count = 0

    # checks if player has won 
    def check_win(self):   
        count = 0
        total = self.squares_x * self.squares_y
        for row in range(self.squares_y):
            for column in range(self.squares_x):
                if self.grid[row][column].is_visible:
                    count += 1
        if ((total - count) == self.num_bombs) and not self.game_lost:
            self.game_won = True
            for row in range(self.squares_y):
                for column in range(self.squares_x):
                    if self.grid[row][column].contains_bomb:
                        self.grid[row][column].contains_flag = True
        
    

    def click_handle(self, row, column, button):
        if button == LEFT_CLICK and self.game_won:
            self.restart()
        elif button == LEFT_CLICK and not self.grid[row][column].contains_flag:
            if not self.game_lost:
                if not self.init:
                    self.set_bomb(row, column)
                    self.init = True
                self.grid[row][column].is_visible = True
                self.grid[row][column].contains_flag = False
                if self.grid[row][column].contains_bomb:
                    self.end_game()
                    self.game_lost = True
                elif self.grid[row][column].bomb_count == 0:
                    self.grid[row][column].reveal_adjacent(self.squares_y, self.squares_x)
                self.check_win()
            else:
                self.game_lost = False
                self.restart()
        elif button == RIGHT_CLICK and not self.grid[row][column].is_visible:
            if not self.grid[row][column].contains_flag:
                self.grid[row][column].contains_flag = True
                self.flag_count += 1
            else:
                self.grid[row][column].contains_flag = False
                self.flag_count -= 1
    class Cell:

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.is_visible = False
            self.contains_bomb = False
            self.bomb_count = 0
            self.text = ""
            self.test = False
            self.contains_flag = False

        def show_text(self):
            if self.is_visible:
                if self.bomb_count == 0:
                    self.text = font.render("", True, BLACK)
                else:
                    self.text = font.render(str(self.bomb_count), True, BLACK)
                screen.blit(self.text, (self.x * (WIDTH + MARGIN) + 12, self.y * (HEIGHT + MARGIN) + 10 + MENU_SIZE))
            
        def count_bombs(self, squaresx, squaresy):
            if not self.test:
                self.test = True
                if not self.contains_bomb:
                    for column in range(self.x - 1 , self.x + 2):
                        for row in range(self.y - 1 , self.y + 2):
                            if (row >= 0 and row < squaresx and column >= 0 and column < squaresy
                                and not (column == self.x and row == self.y)
                                and game.grid[row][column].contains_bomb):
                                    self.bomb_count += 1
                                    
        
        def reveal_adjacent(self, squaresx, squaresy):
            column = self.x
            row = self.y
            for row_off in range(-1, 2):
                for column_off in range(-1, 2):
                    if ((row_off == 0 or column_off == 0) and row_off != column_off
                        and row+row_off >= 0 and column+column_off >=0 and row+row_off < squaresx and column+column_off < squaresy):
                            game.grid[row + row_off][column + column_off].count_bombs(game.squares_y, game.squares_x)
                            if not game.grid[row + row_off][column + column_off].is_visible and not game.grid[row + row_off][column + column_off].contains_bomb:  
                                    game.grid[row + row_off][column + column_off].is_visible = True
                                    game.grid[row + row_off][column + column_off].contains_flag = False
                                    if game.grid[row + row_off][column + column_off].bomb_count == 0: 
                                        game.grid[row + row_off][column + column_off].reveal_adjacent(game.squares_y, game.squares_x)


class Menu():

    def __init__(self):
        self.width = pygame.display.get_surface().get_width() - 2*MARGIN
        self.button_minus = self.Button(10, 10, 20, 20, "-", 6, -3)
        self.button_plus = self.Button(150, 10, 20, 20, "+", 3, -4)
        self.button_flags = self.Button(280, 16, 10, 10, "")
        self.button_flags.background = BLUE
        self.label_bombs = self.Label(30, 10)
        self.label_game_end = self.Label(100, 10)
        self.label_flags = self.Label(450, 10)

    def click_handle(self, obj):
        if self.button_minus.click_handle():
            obj.change_num_bombs(-1)
        if self.button_plus.click_handle():
            obj.change_num_bombs(1)
        
    def draw(self, obj):
        self.width = pygame.display.get_surface().get_width() - 2*MARGIN 
        pygame.draw.rect(screen, GRAY, [MARGIN, 0, self.width, MENU_SIZE])
        self.button_minus.draw(screen)
        self.button_plus.draw(screen)
        self.label_bombs.show(screen, str(game.num_bombs) + " bombs")
        self.label_flags.show(screen, "Flags used: " + str(game.flag_count))

        if obj.game_lost:
            self.label_game_end.show(screen, "            You Lost!")
        elif obj.game_won:
            self.label_game_end.show(screen, "            You Won!")
    
    class Label:
    
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.text = ""
        
        def show(self, surface, value): 
            text = str(value)
            self.text = font.render(text, True, BLACK)     
            surface.blit(self.text, (self.x, self.y))
    

    class Button:

        def __init__(self, x, y, width, height, text, xoff=0, yoff=0):
            self.x = x
            self.y = y
            self.height = height
            self.width = width
            self.background = WHITE
            self.text = text
            self.x_offset = xoff
            self.y_offset = yoff

        def draw(self, surface):
            pygame.draw.ellipse(surface, self.background, [self.x, self.y, self.width, self.height], 0)
            text = font.render(self.text, True, BLACK)     
            surface.blit(text, (self.x + self.x_offset, self.y + self.y_offset))
        
        def click_handle(self):
            pos = pygame.mouse.get_pos()
            if pos[0] > self.x and pos[1] > self.y and pos[0] < (self.x + self.width) and pos[1] < (self.y + self.height):
                return True
            else:
                return False



if __name__ == "__main__":
    os.environ['SDL_Video_CENTERED'] = '1' #center the game window
    pygame.init()
    size = (SIZE*(WIDTH + MARGIN) + MARGIN, (SIZE*(HEIGHT + MARGIN) + MARGIN) + MENU_SIZE)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption("Minesweeper")
    font = pygame.font.Font('freesansbold.ttf', 24)
    game = Game()
    menu = Menu()
    clock = pygame.time.Clock()
    # Main loop
    cont = True
    while cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    with open("menu.py", "r") as rnf:
                        exec(rnf.read())
                    cont = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    column = position[0] // (WIDTH + MARGIN)
                    row = (position[1] - MENU_SIZE) // (HEIGHT + MARGIN)
                    if row >= game.squares_y:
                        row = game.squares_y - 1
                    if column >= game.squares_x:
                        column = game.squares_x - 1
                    if row >= 0:
                        game.click_handle(row, column, event.button)
                    else:
                        menu.click_handle(game)
            elif event.type == pygame.VIDEORESIZE:
                if game.resize: 
                    game.adjust_grid(event.w, event.h)
                    game.restart()
                else:  
                    game.resize = True
        game.draw()
        menu.draw(game)
        clock.tick(60)
        pygame.display.flip()