#Abdullah Kobaissi
#CS 2520-01
#Spring 2023
#Capstone Project - Snake Game Implementation

import pygame
import time
import random
from pygame.locals import * #this will help with recognizing the keys entered by the users
from pygame import mixer #this will be for music
import os
import sys

SIZE = 40  #constant variable to be used for size of blocks for spacing (initially 15)
BG_COLOR = (0,0,0) #constant to hold the background color to be used throughout the program execution

#constants to be used for consistency in scaling of objects (block, apple, bomb)
SCALE_X = SIZE
SCALE_Y = SIZE

#class for the apple
class Apple:
    #create the constructor and also pass it the window screen as a parent object so that the apple can be painted on the window
    def __init__(self, parent_screen):
        #draw and scale the apple image
        self.image = pygame.image.load('assets/apple.png').convert()
        #self.image = pygame.transform.scale(self.image,(SCALE_X,SCALE_Y))  #scale the size of the apple to make it reasonable relative to the window size
        self.parent_screen = parent_screen #initialize the parent screen in the constructor
        
        #set the x and y positions of the apple to be multiples of the SIZE variable so that the snake and apple can align on the grid
        self.x = SIZE*3#8
        self.y = SIZE*3#8

    def draw(self):
        #self.parent_screen.fill((0,0,0)) #call the .fill() function (and give it (0,0,0) to match the black background) again to fill the background at every keystroke so that the previous apple position does not still show after it has been eaten
        self.parent_screen.blit(self.image, (self.x,self.y)) #use .blit() to draw the apple onto the surface window (the background) at the given coordinates for each block in the snake
        pygame.display.update()  #must add this code to tell pygame to update the display - can also use pygame.display.flip()
        
    #function to move the apple to a new location after it has been eaten
    def move(self):
        self.x = random.randint(0,24) * SIZE  #1000/40 = 25 so we want to be less than that just to make sure it is within the bounds  #1000/15 = 67
        self.y = random.randint(0,19) * SIZE  #800/40 = 20 so we want to be less than that just to make sure it is within the bounds   #500/15 = 34
        

#class for the bomb
class Bomb:
    #create the constructor and also pass it the window screen as a parent object so that the apple can be painted on the window
    def __init__(self, parent_screen):
        #draw and scale the bomb image
        self.image = pygame.image.load('assets/green_bomb.png').convert()
        #self.image = pygame.transform.scale(self.image,(SCALE_X,SCALE_Y))  #scale the size of the apple to make it reasonable relative to the window size
        self.parent_screen = parent_screen #initialize the parent screen in the constructor
        
        #set the x and y positions of the apple to be multiples of the SIZE variable so that the snake and apple can align on the grid
        self.x = SIZE*3#8
        self.y = SIZE*3#8

    def draw(self):
        #self.parent_screen.fill((0,0,0)) #call the .fill() function (and give it (0,0,0) to match the black background) again to fill the background at every keystroke so that the previous apple position does not still show after it has been eaten
        self.parent_screen.blit(self.image, (self.x,self.y)) #use .blit() to draw the apple onto the surface window (the background) at the given coordinates for each block in the snake
        pygame.display.update()  #must add this code to tell pygame to update the display - can also use pygame.display.flip()
        
    #function to move the bomb to a new location
    def move(self):
        self.x = random.randint(0,24) * SIZE  #1000/40 = 25 so we want to be less than that just to make sure it is within the bounds  #1000/15 = 67
        self.y = random.randint(0,19) * SIZE  #800/40 = 20 so we want to be less than that just to make sure it is within the bounds   #500/15 = 34        


#class for the snake
class Snake:
    #create the constructor and also pass it the window screen as a parent object and the length
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        
        #load in the 'block.png' image for the snake blocks
        self.block = pygame.image.load('assets/block.png').convert()
        #self.block = pygame.transform.scale(self.block, (SCALE_X,SCALE_Y))  #scale the size of the block to make it reasonable relative to the window size
        self.direction = 'down' #initialize the starting direction
        
        #set the initial position of the snake (half of width and height which will put it in the center)
        self.x = [SIZE] * length #this will account for the x position of each block in the entire snake object (by initializing an empty list of size length) #500
        self.y = [SIZE] * length #this will account for the y position of each block in the entire snake object (by initializing an empty list of size length) #250
        
    #helper function to increase snake length list and to append extra block as a new element
    def increaseLength(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    #function to draw/re-draw the snake at given position
    def draw(self):
        self.parent_screen.fill(BG_COLOR) #call the .fill() function (and give it (0,0,0) to match the black background) again to fill the background at every keystroke so that the blocks don't overlap and the previous position of the block does not still show
        # iterate through the length of the snake to update each block
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i],self.y[i])) #use .blit() to draw the block onto the surface window (the background) at the given coordinates for each block in the snake
        pygame.display.update()  #must add this code to tell pygame to update the display - can also use pygame.display.flip()
        
    #function to move up
    def moveUp(self):
        #ensure that snake can not move back on itself
        if self.direction != 'down':
            self.direction = 'up' #set the direction for keepMoving()
    
    #function to move down   
    def moveDown(self):
        #ensure that snake can not move back on itself
        if self.direction != 'up':
            self.direction = 'down' #set the direction for keepMoving()
        
    #function to move left
    def moveLeft(self):
        #ensure that snake can not move back on itself
        if self.direction != 'right':
            self.direction = 'left' #set the direction for keepMoving()
    
    #function to move right
    def moveRight(self):
        #ensure that snake can not move back on itself
        if self.direction != 'left':
            self.direction = 'right' #set the direction for keepMoving()
        
    #helper function to allow the snake block to keep moving continuously without user having to keep pressing the keys
    def keepMoving(self):
        #execute a for loop (working backwards) to shift all blocks in the list to the position of the previous block (so that the rest snake body can follow the head properly)
        #example: block2 will go to previous position of block1, block3 will go to previous position of block2, block4 will go to previous position of block3, etc.
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        if self.direction == 'up':
            self.y[0] -= SIZE  #move the position of the head of the snake (block at index 0) based on the SIZE variable to preserve the distance between blocks and prevent overlap
        if self.direction == 'down':
            self.y[0] += SIZE  #move the position of the head of the snake (block at index 0) based on the SIZE variable to preserve the distance between blocks and prevent overlap
        if self.direction == 'left':
            self.x[0] -= SIZE  #move the position of the head of the snake (block at index 0) based on the SIZE variable to preserve the distance between blocks and prevent overlap
        if self.direction == 'right':
            self.x[0] += SIZE #move the position of the head of the snake (block at index 0) based on the SIZE variable to preserve the distance between blocks and prevent overlap
            
            
        self.draw() #re-draw the snake at updated position
        
        

#class for the game creation/initialization
class Game:
    def __init__(self):
        os.environ['SDL_Video_CENTERED'] = '1' #center the game window
        pygame.init() #initializes the game
        
        #set the dimentsions for the window surface
        self.width = 1280 #1000
        self.height = 800
        self.timeValue = 0.15 #to be used for the movement delay timer
        self.surface = pygame.display.set_mode((self.width, self.height))   #initialize game window (first argument is window size - in this case 500x500 pixels)
        self.surface.fill(BG_COLOR)  #if you want to change the color of the background (by default it is black) - this uses rgb color values from 0 to 255
        self.snake = Snake(self.surface, 1) #also create the snake object when initializing the game (and pass it the window screen surface)
        self.snake.draw()  #draw the snake
        
        self.apple = Apple(self.surface) #create the apple object when initializing the game (and pass it the window screen surface)
        self.apple.move() #draw the apple and move it to a random initial position
        
        # self.bomb = Bomb(self.surface)
        # self.bomb.draw()
        
        #load in the music file and play it
        mixer.init()
        mixer.music.load('assets/background_music.ogg')
        mixer.music.play(-1) #passing -1 makes the background music loop
        
    
    #function to check if snake head has collided with apple or itself
    def checkCollision(self, x1, y1, x2, y2):
        #check if there is overlap between x1 (snake head x position) and x2 (apple x position)
        if x1 == x2 and x1 <= x2 + SIZE:
            #must also check if there is an overlap between y1 (snake head y position) and y2 (apple y postion) at the same time
            if y1 == y2 and y1 <= y2 + SIZE:
                return True #means there is a collision
        return False #otherwise no collision
    
    #function to check if snake head has collided with borders of window
    def checkWallCollision(self, x, y):
        if x < 0 or x > self.width - SIZE or y < 0 or y > self.height - SIZE:
            return True
        else:
            return False
    
    #helper function to keep the game playing in the same state throughout the frames of the snake moving
    def continuePlaying(self):
        self.snake.keepMoving() #call the keepMoving function to keep the snake moving continuously
        self.apple.draw() #also call the apple.draw() function to not clear the apple with every frame that the snake has moved
        self.showScore() #show the updated score on the screen
        pygame.display.update() #must add this code to tell pygame to update the display after changing score - can also use pygame.display.flip()

        #if a collision has been detected between snake and apple
        if self.checkCollision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            ding = pygame.mixer.Sound('assets/ding.mp3')
            pygame.mixer.Sound.play(ding) #create and play the sound effect
            #print('collison detected')
            self.snake.increaseLength() #increase the length of the snake
            self.apple.move() #move the apple to new position
            if self.timeValue > 0.01:
                self.timeValue -= 0.01 #speed up the time value slightly to make it more challening after each apple is eaten
            else:
                #pass
                self.timeValue = 0.01
                self.timeValue = self.timeValue
            
        #if a collision has been detected between snake and itself (start from index 1 because 0 is head of the snake) 
        #iterate through entire length of snake and check for collision between head of snake and the block at that index
        for i in range(1, self.snake.length):
            if self.checkCollision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                gameOverSound = pygame.mixer.Sound('assets/game_over.mp3')
                pygame.mixer.Sound.play(gameOverSound) #play game over sound
                raise "GAME OVER!" #end the game by raising an exception
            
        #if a collision has been detected between snake and borders of window
        if self.checkWallCollision(self.snake.x[0], self.snake.y[0]):
                gameOverSound = pygame.mixer.Sound('assets/game_over.mp3')
                pygame.mixer.Sound.play(gameOverSound) #play game over sound
                raise "GAME OVER!" #end the game by raising an exception
            
    
    def showScore(self):
        font = pygame.font.SysFont('assets/SnakeFont',30) #create the font (and font size) to be used for the score
        score = font.render(f"SCORE: {self.snake.length}", True, (255,255,255)) #update the score (which will just be the snake length) by using render and also set the color of the score - (255,255,255) = white
        self.surface.blit(score, (1150, 10)) #use .blit() to draw the score onto the surface window (the background) at the given coordinates
        #875
    def showGameOverScreen(self):
        self.surface.fill(BG_COLOR)  #re-initialize the screen which essentially clears it
        font = pygame.font.SysFont('assets/SnakeFont',85) #set the font type and size
        line2 = font.render("         GAME OVER!", True, (255,255,255)) #show the Game Over message
        self.surface.blit(line2, (250,200)) #use .blit() to draw the message onto the surface window (the background) at the given coordinates
        line2 = font.render(f"            SCORE: {self.snake.length}", True, (255,255,255)) #show the final score (255,255,255) = white font color
        self.surface.blit(line2, (250,300)) #show second line a bit lower than first line
        line3 = font.render("Press Enter to play again", True, (255,255,255))
        self.surface.blit(line3, (250,400)) #show last line a bit lower than second line
        line4 = font.render("       Press Esc to exit", True, (255,255,255))
        self.surface.blit(line4, (225,500)) #show last line a bit lower than second line
        pygame.display.update()  #must add this code to tell pygame to update the display - can also use pygame.display.flip()
        
    
    #function to reset the game after losing
    def reset(self):
        #recreate the game objects as new
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        self.apple.move() #move the apple to a random initial position
        self.timeValue = 0.15 #reset the time value for speed 
        
    
    #function to run the game
    def run(self):
        #set up the event loop to keep the game running (instead of using a timer)
        running = True # initialize flag to keep track of running status of game
        paused = False #flag for keeping track of when game state is paused (for the game over screen)
        while running:
            # use pygame.event.get() to get all event types from the user and respond to keystrokes accordingly
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        mixer.music.stop()
                        with open("menu.py", "r") as rnf:
                            exec(rnf.read())
                        running = False
                        #mixer.music.stop()
                    if event.key == K_RETURN:
                        paused = False
                        self.reset()
                    #disable movement keys when game is paused
                    if not paused:
                        if event.key == K_UP:
                            self.snake.moveUp()
                        if event.key == K_DOWN:
                            self.snake.moveDown()
                        if event.key == K_LEFT:
                            self.snake.moveLeft()
                        if event.key == K_RIGHT:
                            self.snake.moveRight()
                elif event.type == QUIT:
                    pygame.exit()
                    sys.exit()
                    running = False
                    mixer.music.stop()
            
            #try-catch block to catch the GAME OVER! exception
            try:
                if not paused:
                    self.continuePlaying() #try calling the continuePlaying() function to keep the game playing
            except Exception as e:
                self.showGameOverScreen()  #handle exception by ending game
                paused = True
            
            time.sleep(self.timeValue) #introduce the timer delay which will be used to slow down the loop while moving the block continuously (so here we are moving the block every 0.1 sec)
            #note: once the value given to time.sleep() i.e. the timeValue reaches 0, the game will stop running

#main
if __name__ == "__main__":
    
    #obj oriented stuff starts-----
    
    game = Game()  #initialize the Game object
    game.run()  #run the game
    
    #obj oriented stuff ends-------

    
    