# Imports
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
icon = pygame.image.load("img/player/Idle/0.png")
pygame.display.set_icon(icon)


class Soilder(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        # Inherit sprite class
        pygame.sprite.Sprite.__init__(self)

        # Draw soilder
        image = pygame.image.load("img/player/Idle/0.png")
        self.img = pygame.transform.scale(
            image, (int(image.get_width() * scale), int(image.get_height() * scale))
        )

        # Draw rectangle
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.img, self.rect)


player = Soilder(200, 200, 3)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Unga Chunga")

run = True

while run:

    player.draw()

    for event in pygame.event.get():
        # Quit Game
        if event.type == pygame.QUIT:
            run = False

        # Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pass

    pygame.display.update()

pygame.quit()
