import random
import pygame


# global constants
WIDTH = 1080
HEIGHT = 720

PADDLE_W = 40
PADDLE_H = 120
PADDLE_SPEED = 700

BALL_SIZE = 40
BALL_SPEED_X = 23
BALL_SPEED_Y = 6

    #                      x  y
direction = pygame.Vector2(0, 0)
dt = 0
cooldown = 0.1   # for ball direction change
running = True


# pygame inits
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.key.set_repeat(0)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)


# paddle Rects
p1 = pygame.Rect(40, HEIGHT / 2 + PADDLE_H / 2, PADDLE_W, PADDLE_H)
p2 = pygame.Rect(WIDTH - PADDLE_W - 40, HEIGHT / 2 + PADDLE_H / 2, PADDLE_W, PADDLE_H)
# ball Rect
ball = pygame.Rect(WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)


def eventLoop():
    """
    Check for events: window close, key presses, mouse clicks, etc..
    """
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # user pressed red X
            running = False

    # smoother movement with key presses
    keys = pygame.key.get_pressed()
    p1.y += (keys[pygame.K_a] - keys[pygame.K_q]) * PADDLE_SPEED * dt
    p2.y += (keys[pygame.K_l] - keys[pygame.K_p]) * PADDLE_SPEED * dt

    # position clamping
    p1.y = min(max(p1.y, 0 - PADDLE_H), HEIGHT)
    p2.y = min(max(p2.y, 0 - PADDLE_H), HEIGHT)


def draw():
    """
    draw everything on screen in order
    """
    # background
    screen.fill("white")

    """ 
        Ball
    # pygame.draw.rect(screen, "orange", ball)
     ^^ Draw Rect OR draw circle (below)
      """
    radius = BALL_SIZE / 2
    # pygame.draw.circle(surface,    color,      center,                              radius,   width=0)
    pygame.draw.circle(screen, "orange", (ball.x + radius, ball.y + radius), radius, width=0)

    # paddles
    pygame.draw.rect(screen, "blue", p1)
    pygame.draw.rect(screen, "blue", p2)


def update(dt):
    """
    update ball position and cooldown every frame
    :param dt: delta time from clock.tick()
    """
    global cooldown
    ball.x += direction.x * dt * BALL_SPEED_X
    ball.y += direction.y * dt * BALL_SPEED_Y
    cooldown -= dt


def checkCollision():
    """
    Check all collisions between ball and paddles, ball and walls.
    """
    # paddle collision
    if ball.colliderect(p1):
        updateBallDir(p1)
    elif ball.colliderect(p2):
        updateBallDir(p2)

    # wall collision
    if ball.x < 0:
        gameOver(2)
    elif ball.x > WIDTH:
        gameOver(1)
    elif ball.y < 0:
        direction.y *= -1
    elif ball.y > HEIGHT - 30:   # handle annoying SDL screen centering issue
        direction.y *= -1


def updateBallDir(paddle):
    global cooldown
    if cooldown < 0:
        cooldown = 0.1   # reset cooldown
        # pong physics: ball bounces at a greater angle and speed the close the ball is to the edge of a paddle
        direction.y = (ball.y + BALL_SIZE / 2) - (paddle.y + PADDLE_H / 2)
        direction.x *= -1  # just reverse the x direction


def start():
    """
    Runs only when game starts.
    """
    global direction
    draw()   # need to to draw something before the wait() since we are not in the main loop yet
    screen.blit(font.render("Press any key to start", True, "black"), (WIDTH / 2 - 100, HEIGHT / 2))
    pygame.display.flip()
    wait()
    direction = pygame.Vector2(random.choice([-BALL_SPEED_X, BALL_SPEED_X]), 0)   # give ball initial velocity


def wait():
    """
    Custom wait function that stalls until a key is pressed or the window is closes.
    """
    global running
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.KEYDOWN:
                return
        clock.tick(120)   # this is needed to keep the clock from skipping in main loop


def gameOver(player):
    global running
    screen.blit(font.render("Game Over", True, "black"), (WIDTH / 2 - 100, HEIGHT / 2))
    screen.blit(font.render(f"Player {player} wins!", True, "black"), (WIDTH / 2 - 100, HEIGHT / 2 + 50))
    pygame.display.flip()
    running = False
    wait()  # wait until user presses a key or X to exit


### MAIN LOOP ###
if __name__ == "__main__":
    start()
    while running:
        eventLoop()
        update(dt)
        checkCollision()
        draw()

        pygame.display.flip()       # "flips" visual updates to display object
        dt = clock.tick(120) / 1000  # locks fps to 60

    pygame.quit()
