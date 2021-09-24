# Imports
from matplotlib.pyplot import draw
import pygame

pygame.init()


# Draw Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_icon(pygame.image.load("img/player/Idle/0.png"))

pygame.display.set_caption("Unga Chunga")


# Clock
clock = pygame.time.Clock()
FPS = 60


# Player Variables
moving_left = False
moving_right = False


# Define Colours
BG = (144, 201, 120)

# Functions
def draw_bg():
    screen.fill(BG)


# Classes
class Soilder(pygame.sprite.Sprite):
    def __init__(self, char_type: str, x: int, y: int, scale, speed):
        # Inherit sprite class
        pygame.sprite.Sprite.__init__(self)

        # Variables
        self.char_type = char_type
        self.speed = int(speed * 5)
        self.direction = 1
        self.flip = False

        # Draw soilder
        image = pygame.image.load(f"img/{self.char_type}/Idle/0.png")
        self.img = pygame.transform.scale(
            image, (int(image.get_width() * scale), int(image.get_height() * scale))
        )

        # Draw rectangle
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # reset variables
        dx = 0
        dy = 0

        # assign variables
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if moving_left and moving_right:
            dx = 0

        # update positon
        self.rect.x += dx
        self.rect.x += dy

    def draw(self):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)


# Create Assets
player = Soilder("player", 200, 200, 3, 1)
enemy = Soilder("enemy", 400, 200, 3, 1)

run = True

while run:
    clock.tick(FPS)
    draw_bg()

    enemy.draw()
    player.draw()
    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        # Quit Game
        if event.type == pygame.QUIT:
            run = False

        # Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True

        # Keyboard releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_ESCAPE:
                run = False

    pygame.display.update()

pygame.quit()
