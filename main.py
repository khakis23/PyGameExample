import pygame, random


######## SETUP ########

# Globals
WIDTH = 800
HEIGHT = 800
RUNNING = True

PLAYER_SPRITE = "assets/CatSprite.png"
ENEMY_SPRITE = "assets/Spider1.png"

SPRITE_WIDTH = 32
SPRITE_HEIGHT = 32
LASER_SIZE = 6

PLAYER_SPEED = 40
LASER_SPEED = 100
LASER_COOLDOWN = 0.2


### other important vars ###
dt = 0      # use delta time for smoother player/object movement
score = 0

# laser
laser = []
laser_cooldown = 0

# enemies
enemies = []
spawn_time = 2.0    # spawn every X seconds
enemy_speed = 50    # starting speed
enemy_sprite = pygame.image.load(ENEMY_SPRITE)


# pygame inits   (required)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 3)   # MacOS specific, might need to tweak vals for other OS's
font = pygame.font.Font(None, 32)


### player ###
player_stating_pos = pygame.Vector2(WIDTH / 2, HEIGHT - SPRITE_HEIGHT * 2)
              # Rect(x,                     y,                   width,        height      )
player = pygame.Rect(player_stating_pos.x, player_stating_pos.y, SPRITE_WIDTH, SPRITE_HEIGHT)   # for drawing and collision
player_sprite = pygame.image.load(PLAYER_SPRITE).convert_alpha()                                    # load sprite
player_sprite = pygame.transform.scale(player_sprite, (1.5 * SPRITE_WIDTH, 1.5 * SPRITE_HEIGHT))   # scale sprite if needed


######## FUNCS ########

def eventLoop():
    """
    All key presses and mouse clicks are checked here.
    """
    global RUNNING, laser_cooldown
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        # red close button pressed
        if event.type == pygame.QUIT:
            RUNNING = False
        # movement keys
        if keys[pygame.K_a] and player.x > 0:
            player.x -= PLAYER_SPEED * dt
        if keys[pygame.K_d] and player.x < WIDTH - SPRITE_WIDTH / 2:
            player.x += PLAYER_SPEED * dt
        # lazer key
        if keys[pygame.K_SPACE] and laser_cooldown < 0:
            laser_cooldown = LASER_COOLDOWN
            spawnLazer()


def draw():
    """
    Everything that is being displayed lives in here.
    Things get drawn in order, so we want to start with the background and move to the foreground.
    """
    global score

    screen.fill("black")

    # draw lazers
    for l in laser:
        pygame.draw.rect(screen, "green", l)

    # draw enemies
    for enemy in enemies:
        # pygame.draw.rect(screen, "red", enemy)   # rect option
        screen.blit(enemy_sprite, enemy)

    # draw player
    # pygame.draw.rect(screen, "white", player)   # rect option
    screen.blit(player_sprite, player)

    # score text
    score_text = font.render(str(score), True, "white")   # create text
    screen.blit(score_text, (10, 10))                              # place on screen (blit to screen)


def gameOver():
    global RUNNING, score

    # display score
    game_over_text = font.render(f"GAME OVER", True, "white")
    score_text = font.render(f"Score: {score}", True, "white")
    screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) / 2, HEIGHT / 2 - 20))
    screen.blit(score_text, ((WIDTH - score_text.get_width()) / 2, HEIGHT / 2 + 20))
    pygame.display.flip()

    # stop main loop and exit program safely
    while True:
        event = pygame.event.wait()     # blocks until an event arrives
        if event.type == pygame.QUIT:
            RUNNING = False
            break


"""
    All funcs below could be written by student.
"""

def spawnEnemy():
    global spawn_time, enemy_speed

    if spawn_time < 0:
        spawn_time = random.randrange(1, 5)  # reset spawn time (seconds)
        enemy_speed += 3   # enemies get faster over time

        # create new enemy          place randomly on x axis
        new_enemy = pygame.Rect(random.randint(0 + SPRITE_WIDTH, WIDTH - SPRITE_WIDTH), 0, SPRITE_WIDTH, SPRITE_HEIGHT)
        enemies.append(new_enemy)   # keep track of all the enemies on the screen


def moveObjects():
    # enemies
    for enemy in enemies:
        enemy.y += enemy_speed * dt

    # lazers
    for l in laser:
        l.y -= LASER_SPEED * dt


def checkCollisions():
    global score

    for enemy in enemies:
        # enemy has gone below screen      or player has a collision with enemy
        if enemy.y >= player_stating_pos.y or player.colliderect(enemy):
            gameOver()

    for l in laser:
        # laser hit an enemy
        for enemy in enemies:    # check all enemies against al lazers
            if l.colliderect(enemy):   # laser has collision with enemy
                enemies.remove(enemy)
                laser.remove(l)
                score += 10 + enemy_speed
                break   # a lazer can only hit one enemy so no need to check anymore

        # lazer went off the top of the screen
        if l.y < 0:
            laser.remove(l)


def spawnLazer():
    global score

    laser.append(
        pygame.Rect(player.x + 6, player.y, LASER_SIZE, LASER_SIZE)
    )
    score -= 2


######## MAIN LOOP #########

while RUNNING:
    # check events
    eventLoop()

    # update game - game logic
    spawnEnemy()
    moveObjects()
    checkCollisions()

    # redraw everything to screen
    draw()

    # subtract time from timers
    spawn_time -= dt
    laser_cooldown -= dt

    pygame.display.flip()        # "flips" visual updates to display object
    dt = clock.tick(60) / 1000   # locks fps to 60

pygame.quit()

