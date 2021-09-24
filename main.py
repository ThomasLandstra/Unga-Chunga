# Imports
import black
import pygame
import os

pygame.init()


# Draw Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_icon(pygame.image.load("img/player/Idle/0.png"))

pygame.display.set_caption("Unga Chunga")


# Clock
clock = pygame.time.Clock()


# Game Variables
BG = (144, 201, 120)
BLACK = (0, 0, 0)
FPS = 60
JUMP = -11
GRAVITY = 0.75

# Player Variables
moving_left = False
moving_right = False


# Functions
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(
        screen,
        BLACK,
        (0, 400),
        (SCREEN_WIDTH, 400),
    )


# Classes
class Soilder(pygame.sprite.Sprite):
    def __init__(self, char_type: str, x: int, y: int, scale, speed):
        # Inherit sprite class
        pygame.sprite.Sprite.__init__(self)

        # Variables
        self.alive = True
        self.jump = False
        self.in_air = True
        self.char_type = char_type
        self.speed = int(speed * 5)
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Add animations
        animation_types = ["Idle", "Run", "Jump"]
        for animation in animation_types:
            temp_list = []
            number_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))
            for i in range(number_of_frames):
                img = pygame.image.load(f"img/{self.char_type}/{animation}/{i}.png")
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale))
                )
                temp_list.append(img)

            self.animation_list.append(temp_list)

        # Draw rectangle
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
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

        # Jump
        if self.in_air:
            self.jump = False
        if self.jump and not self.in_air:
            self.vel_y = JUMP
            self.jump = False
            self.in_air = True

        # Apply Gravity
        self.vel_y += GRAVITY
        if self.vel_y > 11:  # Terminal Velocity
            self.vel_y = 11
        dy += self.vel_y

        # Check floor collision
        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom
            self.in_air = False

        # update positon
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # Update animation
        ANIMATION_COOLDOWN = 100

        # Update Image
        self.image = self.animation_list[self.action][self.frame_index]

        # Check time
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


# Create Assets
player = Soilder("player", 200, 200, 3, 1)
enemy = Soilder("enemy", 400, 200, 3, 1)

run = True

while run:
    clock.tick(FPS)
    draw_bg()

    enemy.draw()
    player.update_animation()
    player.draw()

    # Update player action
    if player.alive:
        if player.in_air:
            player.update_action(2)  # Run
        elif moving_left or moving_right:
            player.update_action(1)  # Run
        else:
            player.update_action(0)  # Idle
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
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # Keyboard releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()
