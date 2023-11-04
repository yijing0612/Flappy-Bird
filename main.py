#Reference: https://github.com/sourabhv/FlapPyBird/blob/master/flappy.py

import pygame
from pygame.locals import *
import random
import sys

#create pipes
def create_pipe():
    pipeHeight = game_sprites['pipe'][0].get_height()
    offset = screen_height / 3
    y2 = offset + random.randrange(0, int(screen_height - game_sprites['base'].get_height() - 1.2 * offset))
    pipeX = screen_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': y2}  # lower Pipe
    ]
    return pipe

#player collide with pipe
def check_collide(player_x, player_y, upper_pipe, lower_pipe):
    run = False
    if player_y > ground - 25 or player_y < 0:
        game_music['hit'].play()
        screen.blit(game_sprites['game_over'], (screen_width / 2, screen_height / 2))
        game_music['game over'].play()
        run=True
        return run

    for pipe in lower_pipe:
        if (player_y + game_sprites['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < \
                game_sprites['pipe'][0].get_width():
            game_music['hit'].play()
            screen.blit(game_sprites['game_over'], (screen_width / 2, screen_height / 2))
            game_music['game over'].play()
            run = True
            return run

    for pipe in upper_pipe:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if (player_y < pipeHeight + pipe['y'] and abs(player_x - pipe['x']) < game_sprites['pipe'][0].get_width()):
            game_music['hit'].play()
            screen.blit(game_sprites['game_over'], (screen_width / 2, screen_height / 2))
            game_music['game over'].play()
            run = True
            return run

    return run

# Variables
bird = 'Image/Flappy Bird/bird.png'
bg = 'Image/Flappy Bird/background.png'
pipe = 'Image/Flappy Bird/pipe.png'
FPS = 32
game_sprites = {}
game_music = {}
screen_width = 289
screen_height = 511
screen = pygame.display.set_mode((screen_width, screen_height))
ground = screen_height * 0.8

#welcome screen before main game start
def welcomeScreen():
    start_button = pygame.Rect(110,200,80,40)
    exit_button = pygame.Rect(110,300,80,40)
    player_x = int(screen_width / 5)
    player_y = int((screen_height - game_sprites['player'].get_height()) / 2)
    menu_x = int((screen_width - game_sprites['message'].get_width()) / 2)
    menu_y = int(screen_height * 0.13)
    run=True

    while run is True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # If the user click start button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    return
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
            else:
                screen.blit(game_sprites['background'], (0, 0))
                screen.blit(game_sprites['player'], (player_x, player_y))
                screen.blit(game_sprites['message'], (menu_x, menu_y))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

#main game flow
def main_flow():
    player_x = int(screen_width / 5)
    player_y = int(screen_width / 2)
    base_x = 0
    score = 0
    pipe_1 = create_pipe()
    pipe_2 = create_pipe()
    pipe_vel_x = -4
    player_vel_y = -9
    player_max_vel_y = 10
    player_acc_y = 1
    flap_height = -10  # height of single flapping
    run = True
    flapped = False  # It is true only when the bird is flapping

    # List of upper pipes
    upper_pipe = [
        {'x': screen_width + 200, 'y': pipe_1[0]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': pipe_2[0]['y']},
    ]
    # List of lower pipes
    lower_pipe = [
        {'x': screen_width + 200, 'y': pipe_1[1]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': pipe_2[1]['y']},
    ]

    while run is True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) or\
                    event.type == pygame.MOUSEBUTTONDOWN:
                if player_y > 0:
                    player_vel_y = flap_height
                    flapped = True
                    game_music['wing'].play()

        # check collison by calling function check_collide
        is_crash = check_collide(player_x, player_y, upper_pipe, lower_pipe)
        
        if is_crash:
            screen.blit(game_sprites['game_over'], (screen_width / 2, screen_height / 2))
            return

        # check score
        player_mid_position = player_x + game_sprites['player'].get_width() / 2
        for pipe in upper_pipe:
            pipe_mid_pos = pipe['x'] + game_sprites['pipe'][0].get_width() / 2
            if pipe_mid_pos <= player_mid_position < pipe_mid_pos + 4:
                score += 1
                game_music['point'].play()

        if not flapped and player_vel_y < player_max_vel_y:
            player_vel_y += player_acc_y

        if flapped:
            flapped = False
        player_height = game_sprites['player'].get_height()
        player_y = player_y + min(player_vel_y, ground - player_y - player_height)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upper_pipe, lower_pipe):
            upperPipe['x'] += pipe_vel_x
            lowerPipe['x'] += pipe_vel_x

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upper_pipe[0]['x'] < 5:
            new_pipe = create_pipe()
            upper_pipe.append(new_pipe[0])
            lower_pipe.append(new_pipe[1])

        # if the pipe is out of the screen, remove it
        if upper_pipe[0]['x'] < -game_sprites['pipe'][0].get_width():
            upper_pipe.pop(0)
            lower_pipe.pop(0)

        # blit sprites
        screen.blit(game_sprites['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upper_pipe, lower_pipe):
            screen.blit(game_sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(game_sprites['base'], (base_x, ground))
        screen.blit(game_sprites['player'], (player_x, player_y))
        player_score = [int(x) for x in list(str(score))]
        width = 0

        for my_score in player_score:
            width += game_sprites['numbers'][my_score].get_width()
        Xoffset = (screen_width - width) / 2

        for my_score in player_score:
            screen.blit(game_sprites['numbers'][my_score], (Xoffset, screen_height * 0.12))
            Xoffset += game_sprites['numbers'][my_score].get_width()

        # when player score 100, he or she win the game
        if player_score == 100:
            screen.blit(game_sprites['win'], (Xoffset, screen_height * 0.12))
            game_music['victory'].play()
            return

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    # This will be the main point from where our game will start
    run = True
    pygame.init()  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    game_sprites['numbers'] = (
        pygame.image.load('Image/Flappy Bird/0.png').convert_alpha(),
        pygame.image.load('Image/Flappy Bird/1.png').convert_alpha(),
        pygame.image.load('Image/Flappy Bird/2.png').convert_alpha(),
        pygame.image.load('Image/Flappy Bird/3.png').convert_alpha(),
        pygame.image.load('Image/Flappy Bird/4.png').convert_alpha(),
        pygame.image.load('Image/Flappy Bird/5.png').convert_alpha(),
        pygame.image.load('Image/Flappy Bird/6.png').convert_alpha(),
        pygame.image.load('Image/Flappy Bird/7.png').convert_alpha(),
        pygame.image.load('Image/Flappy Bird/8.png').convert_alpha(),
        pygame.image.load('Image/Flappy Bird/9.png').convert_alpha(),
    )
    game_sprites['message'] = pygame.image.load('Image/Flappy Bird/message.png').convert_alpha()
    game_sprites['base'] = pygame.image.load('Image/Flappy Bird/base.png').convert_alpha()
    game_sprites['win'] = pygame.image.load('Image/Flappy Bird/win.png').convert_alpha()
    game_sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
                            pygame.image.load(pipe).convert_alpha())
    game_sprites['game_over'] = pygame.image.load('Image/Flappy Bird/game over.png').convert_alpha()
    game_music['die'] = pygame.mixer.Sound('Image/Flappy Bird/die.wav')
    game_music['hit'] = pygame.mixer.Sound('Image/Flappy Bird/hit.wav')
    game_music['point'] = pygame.mixer.Sound('Image/Flappy Bird/point.wav')
    game_music['swoosh'] = pygame.mixer.Sound('Image/Flappy Bird/swoosh.wav')
    game_music['wing'] = pygame.mixer.Sound('Image/Flappy Bird/wing.wav')
    game_music['game over'] = pygame.mixer.Sound('Image/Flappy Bird/game over.wav')
    game_music['victory'] = pygame.mixer.Sound('Image/Flappy Bird/victory.wav')
    game_sprites['background'] = pygame.image.load(bg).convert()
    game_sprites['player'] = pygame.image.load(bird).convert_alpha()

    while run is True:
        welcomeScreen()  # Shows welcome screen to the user until he presses a button
        main_flow()  #main game function after press start button
