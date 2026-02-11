import pygame
import math
import sys

# -----------------------------
# Init
# -----------------------------
pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street XI")
clock = pygame.time.Clock()

# -----------------------------
# Colors
# -----------------------------
GREEN = (30, 143, 62)
WHITE = (255, 255, 255)
BLUE = (50, 120, 255)
RED = (220, 50, 50)

# -----------------------------
# Game Objects
# -----------------------------
score = 0

player = {"x": 200, "y": 250, "r": 12, "speed": 4}
ball = {"x": 230, "y": 250, "r": 8, "vx": 0, "vy": 0}
goalie = {"x": 860, "y": 250, "r": 15, "speed": 2}


# -----------------------------
# Functions
# -----------------------------
def reset_ball():
    ball["x"] = 230
    ball["y"] = 250
    ball["vx"] = 0
    ball["vy"] = 0


def draw_field():
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 3)
    pygame.draw.line(screen, WHITE, (450, 0), (450, HEIGHT), 3)
    pygame.draw.rect(screen, WHITE, (880, 180, 20, 140))  # Goal


def update_player(keys):
    if keys[pygame.K_w]:
        player["y"] -= player["speed"]
    if keys[pygame.K_s]:
        player["y"] += player["speed"]
    if keys[pygame.K_a]:
        player["x"] -= player["speed"]
    if keys[pygame.K_d]:
        player["x"] += player["speed"]

    # Keep player in bounds
    player["x"] = max(player["r"], min(WIDTH - player["r"], player["x"]))
    player["y"] = max(player["r"], min(HEIGHT - player["r"], player["y"]))


def kick_ball(keys):
    dx = ball["x"] - player["x"]
    dy = ball["y"] - player["y"]
    dist = math.hypot(dx, dy)

    if dist < player["r"] + ball["r"] + 5 and keys[pygame.K_SPACE]:
        if dist != 0:
            ball["vx"] = (dx / dist) * 10
            ball["vy"] = (dy / dist) * 10


def update_ball():
    global score

    ball["x"] += ball["vx"]
    ball["y"] += ball["vy"]

    ball["vx"] *= 0.98
    ball["vy"] *= 0.98

    # Bounce top/bottom
    if ball["y"] <= ball["r"] or ball["y"] >= HEIGHT - ball["r"]:
        ball["vy"] *= -1

    # Goal detection
    if ball["x"] > 880 and 180 < ball["y"] < 320:
        score += 1
        reset_ball()

    # Stop tiny movement
    if abs(ball["vx"]) < 0.05:
        ball["vx"] = 0
    if abs(ball["vy"]) < 0.05:
        ball["vy"] = 0


def update_goalie():
    if ball["y"] < goalie["y"]:
        goalie["y"] -= goalie["speed"]
    if ball["y"] > goalie["y"]:
        goalie["y"] += goalie["speed"]

    dx = ball["x"] - goalie["x"]
    dy = ball["y"] - goalie["y"]
    dist = math.hypot(dx, dy)

    if dist < goalie["r"] + ball["r"]:
        ball["vx"] *= -1


def draw_objects():
    pygame.draw.circle(screen, BLUE, (int(player["x"]), int(player["y"])), player["r"])
    pygame.draw.circle(screen, WHITE, (int(ball["x"]), int(ball["y"])), ball["r"])
    pygame.draw.circle(screen, RED, (int(goalie["x"]), int(goalie["y"])), goalie["r"])


def draw_score():
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"YOU {score}", True, WHITE)
    screen.blit(text, (20, 20))

# -----------------------------
# Game Loop
# -----------------------------
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    draw_field()
    update_player(keys)
    kick_ball(keys)
    update_ball()
    update_goalie()
    draw_objects()
    draw_score()

    pygame.display.flip()

pygame.quit()
sys.exit()