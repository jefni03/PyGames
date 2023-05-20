import sys
import random
import pygame
import os
from minesweeper import *
'''
In order to run first install pygame, instructions can be found at https://pypi.org/project/pygame/

then run the menu.py file

'''

os.environ['SDL_Video_CENTERED'] = '1' #center the game window
pygame.init()
clk = pygame.time.Clock()

w = 1280
h = 800 #960


# self.width = 1000
# self.height = 800
# self.timeValue = 0.15 #to be used for the movement delay timer
# self.surface = pygame.display.set_mode((self.width, self.height))   #initialize game window (first argument is window size - in this case 500x500 pixels)
# self.surface.fill(BG_COLOR)  #if you want to change the color of the background (by default it is black) - this uses rgb color values from 0 to 255


screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("PyGame Retro Games")

bg = pygame.Color('black')
white = (255, 255, 255)

#font = pygame.font.SysFont('arial', 50)
font = pygame.font.SysFont('assets/SnakeFont',70)
headerFont = pygame.font.SysFont('assets/SnakeFont',100)
menuRunning = True



while menuRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                with open("minesweeper.py", "r") as rnf:
                    exec(rnf.read())
            elif event.key == pygame.K_2:
                with open("Pong.py", "r") as rnf:
                    exec(rnf.read())
            elif event.key == pygame.K_3:
                with open("Snake.py", "r") as rnf:
                    exec(rnf.read())
            elif event.key == pygame.K_4 or event.key == pygame.K_ESCAPE:
                menuRunning = False
    
    text = headerFont.render(f'PYGAME RETRO GAMES', False, white)
    text2 = font.render(f'1) MINESWEEPER', False, white)
    text3 = font.render(f'2) PONG', False, white)
    text4 = font.render(f'3) SPEED SNAKE', False, white)
    text5 = font.render(f'4) QUIT', False, white)
    
    text_rect = text.get_rect(center=(w // 2, h // 4))
    text2_rect = text2.get_rect(center=(w // 2, h // 2))
    text3_rect = text3.get_rect(center=(w // 2, h // 2))
    text4_rect = text4.get_rect(center=(w // 2, h // 2))
    text5_rect = text5.get_rect(center=(w // 2, h // 2))
    
    screen.fill(bg)
    screen.blit(text, (225,100))#text_rect)
    screen.blit(text2, (400,300))#text2_rect)
    screen.blit(text3, (400,400))#text3_rect)
    screen.blit(text4, (400,500))#text4_rect)
    screen.blit(text5, (400,600))#text5_rect)
    
    pygame.display.update()
    clk.tick(60)
