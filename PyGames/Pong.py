import sys
import random
import pygame
import os

def lose():
    screen.fill((0, 0, 0))
    title = font.render('You Lose!', True, (255, 255, 255))
    screen.blit(title, (width / 2 - title.get_width() / 2, height / 2 - title.get_height() / 3))
    pygame.display.update()

def win():
    screen.fill((0, 0, 0))
    title = font.render('You Win!', True, (255, 255, 255))
    screen.blit(title, (width / 2 - title.get_width() / 2, height / 2 - title.get_height() / 3))
    pygame.display.update()

os.environ['SDL_Video_CENTERED'] = '1' #center the game window
pygame.init()
clk = pygame.time.Clock()

width = 1280
height = 800#960

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

pong = pygame.Rect(width/2 - 15, height/2 - 15, 30, 30)
p1 = pygame.Rect(width - 30, height/2 - 70 - 70, 10, 140)
p2 = pygame.Rect(20, height/2 - 70 - 70, 10, 140)

bg = pygame.Color('black')
white = (255, 255, 255)

x_speed = 6 * random.choice((1, -1))
y_speed = 6 * random.choice((1, -1))
p1_speed = 0
p2_speed = 6
center = (width/2, height/2)
p1_score = 0
p2_score = 0

font = pygame.font.SysFont('arial', 100)

game = "cont"
win = 0
cont = True
while cont:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game == "cont":
            # player 1 input movements
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    p1_speed += 6
                if event.key == pygame.K_DOWN:
                    p1_speed -= 6
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p1_speed -= 6
                if event.key == pygame.K_DOWN:
                    p1_speed += 6
                if event.key == pygame.K_ESCAPE:
                    with open("menu.py", "r") as rnf:
                        exec(rnf.read())
                    cont = False
        if game == "over":
            if win == 1:
                win()
            elif win == 0:
                lose()
            game = "over"
    if game != "over":
        pong.x = pong.x + x_speed
        pong.y = pong.y + y_speed

        # pong collision
        if pong.top <= 0 or pong.bottom >= height:
            y_speed *= -1

        if pong.colliderect(p1) or pong.colliderect(p2):
            x_speed *= -1

        if pong.left <= 0:
            p1_score = p1_score + 1
            pong.center = center
            y_speed *= random.choice((1, -1))
            x_speed *= random.choice((1, -1))
            if p1_score == 5:
                game = "over"
                win = 1

        if pong.right >= width:
            pong.center = center
            y_speed *= random.choice((1, -1))
            x_speed *= random.choice((1, -1))
            p2_score = p2_score + 1
            if p2_score == 5:
                game = "over"
                win = 0

        p1.y += p1_speed
        # bound player movements to screen only
        if p1.top <= 0:
            p1.top = 0
        if p1.bottom >= height:
            p1.bottom = height

        # player 2 movements
        if p2.top < pong.y:  # if pong is above player 2 go up
            p2.top += p2_speed
        if p2.bottom > pong.y:  # if pong is below player 2 go down
            p2.bottom -= p2_speed
        # player 2 collision with borders
        if p2.top <= 0:
            p2.top = 0
        if p2.bottom >= height:
            p2.bottom = height

        screen.fill(bg)
        pygame.draw.rect(screen, white, p1)
        pygame.draw.rect(screen, white, p2)
        pygame.draw.ellipse(screen, white, pong)
        pygame.draw.aaline(screen, white, (width/2, 0), (width/2, height))
        p1_text = font.render(f'{p1_score}', False, white)
        screen.blit(p1_text, (900, 100))

        p2_text = font.render(f'{p2_score}', False, white)
        screen.blit(p2_text, (360, 100))

        pygame.display.flip()
        clk.tick(60)

