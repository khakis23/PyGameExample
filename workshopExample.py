import pygame
import random


WIDTH = 800
HEIGHT = 800
PLAYER_SIZE = 40
PLAYER_SPEED = 400
ENEMY_SPEED = 50

running = True
dt = 0.0
respawn_time = 5   # TODO add respawn timer


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = pygame.Rect(WIDTH / 2, HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE)
enemies = []   # TODO store enemies in a list

# TODO remove this:
# enemy = pygame.Rect(WIDTH / 2 + 100, HEIGHT / 2 + 100, CHARACTER_WIDTH, CHARACTER_WIDTH)
#
# ENEMY_SPEED = 50
# enemy_dir = pygame.Vector2(random.randint(0, 5), random.randint(0, 5))


def events():
    global running
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if keys[pygame.K_w]:
            player.y -= PLAYER_SPEED * dt
        if keys[pygame.K_s]:
            player.y += PLAYER_SPEED * dt
        if keys[pygame.K_a]:
            player.x -= PLAYER_SPEED * dt
        if keys[pygame.K_d]:
            player.x += PLAYER_SPEED * dt


def draw():
    screen.fill("white")

    # TODO iterate through all the enemies
    for en in enemies:
        pygame.draw.rect(screen, "green", en["enemy"])
    pygame.draw.rect(screen, "red", player)
    pygame.display.flip()


def checkCollision():
    global running

    # TODO now have to check collision with all enemies
    for en in enemies:
        if player.colliderect(en["enemy"]):
            running = False


def update():
    global respawn_time

    # TODO count down respawn time
    respawn_time -= dt

    # TODO respawn enemies when timer is up
    if respawn_time < 0:
        respawn_time = random.randint(1, 5)   # reset timer
        enemies.append({
            "enemy": pygame.Rect(WIDTH / 2, HEIGHT / 2, PLAYER_SIZE, PLAYER_SIZE),   # store a dict
            "dir": pygame.Vector2(random.randint(-5,5), random.randint(-5,5))   # {"enemy": Rect, "dir": Vector2}
        })

    # TODO change direction of enemies
    for en in enemies:
        pos = en["enemy"]   # Rect
        if pos.x > WIDTH or pos.x < 0:
            en["dir"].x *= -1
        if pos.y > HEIGHT or pos.y < 0:
            en["dir"].y *= -1

        pos.x += ENEMY_SPEED * en["dir"].x * dt
        pos.y += ENEMY_SPEED * en["dir"].y * dt


while running:
    events()
    draw()
    checkCollision()
    update()

    dt = clock.tick(60) / 1000

pygame.quit()
