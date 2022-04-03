import pygame

from settings import BRICKSIZE

class Brick(pygame.sprite.Sprite):

    def __init__(self, pos, color, group):
        super().__init__(group)
        self.pos = pos
        self.color = color

        #self.image = pygame.Surface(BRICKSIZE)
        #self.image.fill(color)
        self.image = pygame.image.load(f'./graphics/{color}/img_0.png').convert()
        self.rect = self.image.get_rect(topleft=pos)

    def render(self, screen):
        screen.blit(self.image, self.rect)
