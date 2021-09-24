# Imports
import pygame
import os

pygame.init()


# Draw Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_icon(pygame.image.load("img/player/Idle/0.png"))

pygame.display.set_caption("Unga Chunga :: Modern Warfare")


# Clock
clock = pygame.time.Clock()


# Game Variables
BG = (144, 120, 210)
BLACK = (0, 0, 0)
FPS = 60
JUMP = -11
GRAVITY = 0.75

# Player Variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# Images
bullet_img = pygame.image.load("img/icons/bullet.png").convert_alpha()
grenade_img = pygame.image.load("img/icons/grenade.png").convert_alpha()


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
    def __init__(self, char_type: str, x: int, y: int, scale, speed, ammo, grenades):
        # Inherit sprite class
        pygame.sprite.Sprite.__init__(self)

        # Variables
        self.alive = True
        self.jump = False
        self.in_air = True
        self.char_type = char_type
        self.speed = int(speed * 5)
        self.ammo = ammo
        self.start_ammo = ammo
        self.grenades = grenades
        self.shoot_cooldown = 0
        self.fire_rate = 20  # Lower is better
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Add animations
        animation_types = ["Idle", "Run", "Jump", "Death"]
        for animation in animation_types:
            temp_list = []
            number_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))

            for i in range(number_of_frames):
                # Load Image
                img = pygame.image.load(
                    f"img/{self.char_type}/{animation}/{i}.png"
                ).convert_alpha()

                # Scale Image
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale))
                )

                temp_list.append(img)  # Add Image to list

            self.animation_list.append(temp_list)

        # Draw rectangle
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

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

    def fire(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            # Draw bullet
            self.shoot_cooldown = self.fire_rate
            bullet = Bullet(
                self.rect.centerx + (self.rect.size[0] * 0.6 * self.direction),
                self.rect.centery,
                self.direction,
            )
            bullet_group.add(bullet)

            # Reduce ammo
            self.ammo -= 1

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
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # Move bullet
        self.rect.x += self.speed * self.direction

        # Is bullet off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # Check character collision
        if pygame.sprite.spritecollide(player, bullet_group, False) and player.alive:
            player.health -= 5
            self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False) and enemy.alive:
            enemy.health -= 25
            self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        # Check floor collision
        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom
            self.speed = 0

        # Check walls
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        # Update position
        self.rect.x += dx
        self.rect.y += dy


# Create sprite groups
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()

# Create Assets
player = Soilder("player", 200, 200, 3, 1, 20, 5)
enemy = Soilder("enemy", 400, 350, 3, 1, 20, 0)

run = True
while run:
    clock.tick(FPS)
    draw_bg()

    enemy.update()
    enemy.draw()
    player.update()
    player.draw()

    # Update and draw groups
    bullet_group.update()
    grenade_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)

    # Update player action
    if player.alive:
        if shoot:
            player.fire()
        elif grenade and not grenade_thrown and player.grenades > 0:
            grenade_group.add(
                Grenade(
                    player.rect.centerx
                    + (player.rect.size[0] * 0.5 * player.direction),
                    player.rect.top,
                    player.direction,
                )
            )
            grenade_thrown = True
            player.grenades -= 1

        if player.in_air:
            player.update_action(2)  # Run
        elif moving_left or moving_right:
            player.update_action(1)  # Run
        else:
            player.update_action(0)  # Idle
        player.move(moving_left, moving_right)

    # Player events
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
            if event.key == pygame.K_g:
                grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # Keyboard releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_g:
                grenade = False
                grenade_thrown = False
            if event.key == pygame.K_SPACE:
                shoot = False

    # Draw screen
    pygame.display.update()

pygame.quit()  # Quit game once loop is broken
