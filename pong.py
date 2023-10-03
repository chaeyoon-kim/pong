import pygame

df = (
    spark.read.format('csv').load('dbfs:/Filestore/...')
)
display(df)


paddle_1 = {"x": 10, "y": 175, "width": 10, "height": 100, "color": (255, 255, 255)}
paddle_2 = {"x": 580, "y": 175, "width": 10, "height": 100, "color": (255, 255, 255)}

ball = {"x": 300, "y": 200, "radius": 5, "x_velocity": -5, "y_velocity": 0, "colour": (0, 255, 0)}

score_one = 0
score_two = 0

pygame.init()
pygame.display.set_caption("Pong")
window = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and paddle_1["y"] >= 0:
        paddle_1["y"] -= 5
    if keys[pygame.K_s] and paddle_1["y"] <= 400 - paddle_1["height"]:
        paddle_1["y"] += 5

    if keys[pygame.K_UP] and paddle_2["y"] >= 0:
        paddle_2["y"] -= 5
    if keys[pygame.K_DOWN] and paddle_2["y"] <= 400 - paddle_2["height"]:
        paddle_2["y"] += 5

    ball["x"] += ball["x_velocity"]
    ball["y"] += ball["y_velocity"]

    if ball["y"] <= 0 + ball["radius"]:
        ball["y_velocity"] *= -1
    if ball["y"] >= 400 - ball["radius"]:
        ball["y_velocity"] *= -1

    if ball["y"] >= paddle_1["y"] and ball["y"] <= paddle_1["y"] + paddle_1["height"]:
        if ball["x"] - ball["radius"] <= paddle_1["x"] + paddle_1["width"]:
            ball["x_velocity"] *= -1
            if ball["y"] <= paddle_1["y"] + (paddle_1["height"] // 2):
                difference = (paddle_1["y"] + (paddle_1["height"] // 2)) - ball["y"]
                reduction = (paddle_1["height"] / 2) / 4
                ball["y_velocity"] = (difference / reduction) * -1
            else:
                difference = (paddle_1["y"] + (paddle_1["height"] // 2)) - ball["y"]
                reduction = (paddle_1["height"]) / 4
                ball["y_velocity"] = (difference / reduction) * -1

    if ball["y"] >= paddle_2["y"] and ball["y"] <= paddle_2["y"] + paddle_2["height"]:
        if ball["x"] + ball["radius"] >= paddle_2["x"]:
            ball["x_velocity"] *= -1
            if ball["y"] <= paddle_2["y"] + (paddle_2["height"] // 2):
                difference = (paddle_2["y"] + (paddle_2["height"] // 2)) - ball["y"]
                reduction = (paddle_2["height"] / 2) / 4
                ball["y_velocity"] = (difference / reduction) * -1
            else:
                difference = (paddle_2["y"] + (paddle_2["height"] // 2)) - ball["y"]
                reduction = (paddle_2["height"]) / 4
                ball["y_velocity"] = (difference / reduction) * -1

    window.fill((0, 0, 0))
    pygame.draw.rect(
        window,
        paddle_1["color"],
        (paddle_1["x"], paddle_1["y"], paddle_1["width"], paddle_1["height"]),
    )
    pygame.draw.rect(
        window,
        paddle_2["color"],
        (paddle_2["x"], paddle_2["y"], paddle_2["width"], paddle_2["height"]),
    )

    if ball["x"] <= 0:
        score_two += 1
        ball["x"] = 300
        ball["y"] = 200
        ball["x_velocity"] *= -1
        ball["y_velocity"] = 0

    elif ball["x"] >= 600:
        score_one += 1
        ball["x"] = 300
        ball["y"] = 200
        ball["x_velocity"] *= -1
        ball["y_velocity"] = 0

    font = pygame.font.SysFont("comicsans", 50)

    if score_one >= 5:
        winning_text = "Left player won"
        text_to_write = font.render(winning_text, 1, (255, 255, 255))
        window.blit(
            text_to_write,
            (600 // 2 - text_to_write.get_width() // 2, 200 - text_to_write.get_height() // 2),
        )
        score_one, score_two = 0, 0
        pygame.display.update()
        pygame.time.delay(10000)
    
    if score_two >= 5:
        winning_text = "Right player won"
        text_to_write = font.render(winning_text, 1, (255, 255, 255))
        window.blit(
            text_to_write,
            (600 // 2 - text_to_write.get_width() // 2, 200 - text_to_write.get_height() // 2),
        )
        score_one, score_two = 0, 0
        pygame.display.update()
        pygame.time.delay(10000)

    score_one_text = font.render(f"{score_one}", 1, (255, 255, 255))
    score_two_text = font.render(f"{score_two}", 1, (255, 255, 255))

    window.blit(score_one_text, (600 // 4 - score_one_text.get_width() // 2, 20))
    window.blit(score_two_text, (600 * (3 / 4) - score_two_text.get_width() // 2, 20))

    pygame.draw.circle(window, ball["colour"], (ball["x"], ball["y"]), ball["radius"])

    pygame.display.update()

pygame.quit()
