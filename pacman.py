import pygame
from board import boards
import math



pygame.init()



WIDTH = 600
HEIGHT = 710
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards
color = 'blue'
PI = math.pi
player_images = []
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (30, 30)))

player_x = 35 #300
player_y = 35 #475
direction = 0
counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0


def draw_board():
    num1 = ((HEIGHT - 50) // 33)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color,(j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + (1 * num1)), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color,(j * num2, i * num1 + (0.5 * num1)), (j * num2 + (num2), i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, (j * num2 - (0.5 * num2), i * num1 + (0.5 * num1), num2, num1), 0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1), num2, num1), PI /2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, (j * num2 + (0.5 * num2), i * num1 - (0.5 * num1), num2, num1), PI , (3 * PI) / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, (j * num2 - (0.5 * num2), i * num1 - (0.5 * num1), num2, num1), (3 * PI) / 2 , 0, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white',(j * num2, i * num1 + (0.5 * num1)), (j * num2 + (num2), i * num1 + (0.5 * num1)), 3)



def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))



def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 33
    num2 = WIDTH // 30
    num3 = 10

    if centerx // 30 < 19:
        # Check go back
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 6 <= centerx % num2 <= 14:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 6 <= centery % num1 <= 14:
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
        
        if direction == 0 or direction == 1:
            if 6 <= centerx % num2 <= 14:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 6 <= centery % num1 <= 14:
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
    
    else:
        turns[0] = True
        turns[1] = True

    return turns
    pass



def move_player(play_x, play_y):
    # R, L, U, D
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    elif direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y



def check_collisions(scor):
    num2 = WIDTH // 30
    num1 = (HEIGHT - 50) // 33
    if 0 < player_x < 570:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
    
    return scor



def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'White')
    screen.blit(score_text, (10, 670))




run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    screen.fill('black')

    draw_board()
    draw_player()
    draw_misc()
    center_x = player_x + 15
    center_y = player_y + 15
    turns_allowed = check_position(center_x, center_y)
    player_x, player_y = move_player(player_x, player_y)
    score = check_collisions(score)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction


    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 600:
        player_x = -50
    elif player_x < -50:
        player_x = 597
    #pygame.draw.circle(screen, 'red', (50,50), 4)
    #screen.blit(player_images[1], (35,595))
    pygame.display.flip()
pygame.quit()
