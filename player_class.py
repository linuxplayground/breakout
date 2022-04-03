import pygame, random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.pos = pygame.math.Vector2(WIDTH//2, HEIGHT-5)
        self.create_player(65)
        self.score = 0
        self.lives = LIVES

    def create_player(self, width):
        self.image = pygame.Surface((width,5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(midbottom = self.pos)

    def update(self, ball_pos):
        if DEMO:
            self.pos.x = ball_pos.x# + random.randint(-5,5)
        else:
            if self.pos.x <0:
                self.pos.x = 0
            if self.pos.x > WIDTH:
                self.pos.x = WIDTH
        self.rect.midbottom = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

