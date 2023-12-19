import pygame
import time
import random
import json
import os
pygame.init()
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 30
font_style = pygame.font.SysFont(None, 35)
score_font = pygame.font.SysFont(None, 35)
def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])
def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - mesg.get_width() / 2, dis_height / 2 + y_displace])

def score(score):
    value = score_font.render("Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

def save_score(score):
    if not os.path.isfile('scores.json'):
        with open('scores.json', 'w') as f:
            json.dump([], f)
    with open('scores.json', 'r') as f:
        scores = json.load(f)
    if score not in scores:  # Vérifie si le score existe déjà
        scores.append(score)
        scores.sort(reverse=True)
    with open('scores.json', 'w') as f:
        json.dump(scores, f)

def display_scores():
    with open('scores.json', 'r') as f:
        scores = json.load(f)
    message("Top scores:", white, 50)
    for i, score in enumerate(scores[:5]):
        message(f"{i+1}. {score}", white, 70 + (i+1)*20)

def gameLoop():
    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    while not game_over:
        while game_close == True:
            dis.fill(blue)
            score_value = Length_of_snake - 1
            score(score_value)
            save_score(score_value)
            message("Vous avez perdu! Appuyez sur Q-Quitter ou C-Continuer", red)
            display_scores()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        our_snake(snake_block, snake_List)
        score(Length_of_snake - 1)
        pygame.display.update()
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block)/ 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
        clock.tick(snake_speed)
    pygame.quit()
    quit()
gameLoop()
