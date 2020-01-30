#**********************************************************************#
#                             Python Pong                              #
#                       written by Gabriel Kutuzov                     #
#**********************************************************************#

import pygame

pygame.init()

# Window Properties
WIDTH = 1000
HEIGHT = 500
win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pong")

# game vars 
color_white = (255,255,255)
color_black = (0, 0, 0)
game_started = False
player1_score = 0
player2_score = 0
player1_next = False

# paddle vars
paddle_x = 50
paddle_y = 250

paddle_w = 15
paddle_h = 100

paddle_velocity = 3

# ball vars 
ball_x = WIDTH  / 2
ball_y = HEIGHT / 2
ball_w = 5
ball_h = 5
ball_velocity = 5
ball_velocity_increase = 0.2
ball_go_left = True
ball_go_up   = True

# paddle x location setup
paddle1_x = paddle_x
paddle2_x = WIDTH - paddle_x
#paddle y location setup
paddle1_y = (HEIGHT / 2) - (paddle_h / 2)
paddle2_y = (HEIGHT / 2) - (paddle_h / 2)

# sound effects
hit_sound   = pygame.mixer.Sound("hit.wav")
hit2_sound  = pygame.mixer.Sound("hit2.wav")
score_sound = pygame.mixer.Sound("score.wav")
start_sound = pygame.mixer.Sound("start.wav")

# welcome/description message
print("Welcome to Python Pong - written by Gabriel Kutuzov")
print("Description: very basic python version of pong. Pretty straight",
        "forward and completely procedural.")

#======================================================================#
#                            main game loop                            #
#======================================================================#

run = True
while run:
    win.fill(color_black) # fill the window with black pixels
    pygame.time.delay(10) # time delay

    # check for pygame 'QUIT' event to break out of game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # start game
    if keys[pygame.K_RETURN] and game_started == False:
        game_started = True
        pygame.mixer.Sound.play(start_sound)
        print("Game Started")

    if game_started == True:
        # check if ball hits top or bottom
        if ball_y >= HEIGHT or ball_y <= 0:
            ball_go_up = not ball_go_up
            pygame.mixer.Sound.play(hit2_sound)

        # check for score and reset game
        if ball_x <= 0 or ball_x >= WIDTH:
            ball_x = WIDTH  / 2
            ball_y = HEIGHT / 2
            game_started = False
            pygame.mixer.Sound.play(score_sound)
            if player1_next:
                player1_score += 1
            else:
                player2_score += 1
            print("Score: ", player1_score, " : ", player2_score)

        # update ball 'y' velocity
        if ball_go_up == True:
            ball_y -= ball_velocity
        else:
            ball_y += ball_velocity

        # update ball 'x' velocity
        if ball_go_left == True:
            ball_x -= ball_velocity
            # player 1 collision
            if ball_x == paddle1_x  and \
            ball_y >= paddle1_y and ball_y <= paddle1_y + (paddle_h): 
                    print("Player 1 blocked")
                    ball_go_left = False
                    player1_next = True # player 1 score check
                    pygame.mixer.Sound.play(hit_sound)
        else:
            ball_x += ball_velocity
            # player 2 collision
            if ball_x >= paddle2_x  and \
            ball_y >= paddle2_y and ball_y <= paddle2_y + (paddle_h): 
                    print("Player 2 blocked")
                    ball_go_left = True
                    player1_next = False # player 2 core check
                    pygame.mixer.Sound.play(hit_sound)

        # really simple AI
        if (paddle2_y > ball_y):
            paddle2_y -= paddle_velocity
        else:
            paddle2_y += paddle_velocity

    # paddle movement control
    if keys[pygame.K_w] and paddle1_y + paddle_h > paddle_h:
        paddle1_y -= paddle_velocity
    if keys[pygame.K_s] and paddle1_y + paddle_h < HEIGHT:
        paddle1_y += paddle_velocity
    if keys[pygame.K_UP] and paddle2_y + paddle_h > paddle_h:
        paddle2_y -= paddle_velocity
    if keys[pygame.K_DOWN] and paddle2_y + paddle_h < HEIGHT:
        paddle2_y += paddle_velocity

#----------------------------------------------------------------------#
#                           update graphics                            #
#----------------------------------------------------------------------#

    # draw paddle (player 1)
    pygame.draw.rect(win, color_white, (paddle1_x, paddle1_y, paddle_w, paddle_h))

    #draw paddle (player 2)
    pygame.draw.rect(win, color_white, (paddle2_x, paddle2_y, paddle_w, paddle_h))

    # draw ball
    pygame.draw.rect(win, color_white, (ball_x, ball_y, ball_w, ball_h))

    # draw center line
    #for x in range(100):
    #    pygame.draw.rect(win, color_white, (WIDTH / 2 + 1, (x * 5) * 2, 2, 5))

    pygame.display.update()


pygame.quit()
