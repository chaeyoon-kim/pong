import pygame
import sys
import json
from types import SimpleNamespace

def dict2obj(dict):
    # using json.loads method and passing json.dumps method and custom object hook as arguments
    return json.loads(json.dumps(dict), object_hook=lambda d: SimpleNamespace(**d))

width, height = 600, 400
score_one, score_two = 0, 0

# initializing the dictionaries
paddle_1 = {"x": 10, "y": 175, "width": 10, "height": 100, "color": "white"}
paddle_2 = {"x": 580, "y": 175, "width": 10, "height": 100, "color": "white"}
ball = {"x": 300, "y": 200, "radius": 5, "x_velocity": -5, "y_velocity": 0, "colour": "green"}
  
# calling the function dict2obj and passing the dictionary as argument
paddle_1 = dict2obj(paddle_1)
paddle_2 = dict2obj(paddle_2)
ball = dict2obj(ball)

pygame.init()
pygame.display.set_caption("Pong")
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 50)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # setting the paddles' movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and paddle_1.y >= 0:
        paddle_1.y -= 5
    if keys[pygame.K_s] and paddle_1.y <= height - paddle_1.height:
        paddle_1.y += 5

    if keys[pygame.K_UP] and paddle_2.y >= 0:
        paddle_2.y -= 5
    if keys[pygame.K_DOWN] and paddle_2.y <= height - paddle_2.height:
        paddle_2.y += 5

    # setting the ball's movement
    ball.x += ball.x_velocity
    ball.y += ball.y_velocity

    if ball.y <= 0 + ball.radius:
        ball.y_velocity *= 1
    if ball.y >= height - ball.radius:
        ball.y_velocity *= -1

    ### interaction between the ball and paddles
    ### control the ball
    if paddle_1.x - ball.radius <= ball.x <= paddle_1.x and ball.y in range(paddle_1.x-ball.radius, paddle_1.y+ball.radius):
        ball.x_velocity *= -1
    if paddle_2.x - ball.radius <= ball.x <= paddle_2.x and ball.y in range(paddle_2.x-ball.radius, paddle_2.y+ball.radius):
        ball.x_velocity *= 1

    # filling the window up to erase the previous markers
    window.fill("black")
    pygame.draw.rect(window, "white", (paddle_1.x, paddle_1.y, paddle_1.width, paddle_1.height))
    pygame.draw.rect(window, "white", (paddle_2.x, paddle_2.y, paddle_2.width, paddle_2.height))
    pygame.draw.circle(window, "green", (ball.x, ball.y), ball.radius)

    # adding the winner's score
    if ball.x <= 0:
        score_two += 1
        ball.x, ball.y = width/2, height/2
        ball.x_velocity, ball.y_velocity = 1, 1
    
    elif ball.x >= width:
        score_one += 1
        ball.x, ball.y = width/2, height/2
        ball.x_velocity, ball.y_velocity = 1, 1

    if score_one >= 5:
        winning_text = "Left player won"
        text_to_write = font.render(winning_text, 1, "white")
        window.blit(
            text_to_write,
            (width // 2 - text_to_write.get_width() // 2, 200 - text_to_write.get_height() // 2),
        )
        score_one, score_two = 0, 0
        pygame.display.update()
        pygame.time.delay(10000)

    if score_two >= 5:
        winning_text = "Right player won"
        text_to_write = font.render(winning_text, 1, "white")
        window.bilt(
            text_to_write,
            (width // 2 - text_to_write.get_width() // 2, 200 - text_to_write.get_height() // 2),
        )
        score_one, score_two = 0, 0
        pygame.display.update()
        pygame.time.delay(10000)

    score_one_text = font.render(f"{score_one}", 1, "white")
    score_two_text = font.render(f"{score_two}", 1, "white")
 
    window.blit(score_one_text, (width // 4 - score_one_text.get_width() // 2, 20))
    window.blit(score_two_text, (width * (3 / 4) - score_two_text.get_width() // 2, 20))

    pygame.draw.circle(window, ball.colour, (ball.x, ball.y), ball.radius)

    pygame.display.update()
