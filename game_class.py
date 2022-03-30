import pygame, sys

from brick_class import Brick
from player_class import Player
from ball_class import Ball

from settings import *

class Game(object):

    def __init__(self):

        pygame.init()

        if FULLSCREEN:
            self.screen = pygame.display.set_mode(SCREENSIZE, flags=pygame.FULLSCREEN|pygame.SCALED)
        else:
            self.screen = pygame.display.set_mode(SCREENSIZE)
        self.background = pygame.Surface(SCREENSIZE)
        self.background.fill((15,15,15))

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Breakout")
        pygame.mouse.set_visible(False)
        
        self.impact_sound = pygame.mixer.Sound('impact.wav')
        self.impact_sound.set_volume(0.1)
        self.fail_sound = pygame.mixer.Sound('fail.wav')
        self.fail_sound.set_volume(0.1)
        self.pickup_sound = pygame.mixer.Sound('pickup.wav')
        self.pickup_sound.set_volume(0.1)

        self.brick_cooldown = 10
        self.font = pygame.font.SysFont('Arial Black', 16, True, False)
        self.player = Player()

    def init_game(self):
        self.gameover = False
        self.playing = False
        self.player.lives = LIVES
        self.player.score = 0
        self.hit_bricks = 0
        self.brick_group = pygame.sprite.Group()
        self.setup_bricks()
        self.ball = Ball(self.player.rect.center)    

    def setup_bricks(self):
        for y in range(5):
            for x in range(WIDTH // BRICKWIDTH):
                Brick((x * BRICKWIDTH, y * BRICKHEIGHT + TOP_BUFFER), ROWS[y], self.brick_group)
            
    def check_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.gameover = True
            if event.type == pygame.KEYDOWN:
                if pygame.K_ESCAPE:
                    self.gameover = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.playing = True
            if event.type == pygame.MOUSEMOTION:
                self.player.pos.x = pygame.mouse.get_pos()[0]

    def collisions(self):

        if self.ball.pos.y <= TOP_BUFFER + len(ROWS) * BRICKHEIGHT:
            hit_bricks = pygame.sprite.spritecollide(self.ball, self.brick_group, False)
            if hit_bricks and self.brick_cooldown == 0:
                self.impact_sound.play()
                self.brick_cooldown = FPS //2 - int(self.ball.speed  * 1.5)
                self.ball.dir.y *= -1
                self.player.score += 10
                self.brick_group.remove(hit_bricks[0])
                if self.player.score == 50:
                    self.ball.speed += 1
                if self.player.score == 400:
                    self.ball.speed += 1
                if self.player.score == 750:
                    self.ball.speed += 1

        if pygame.sprite.collide_rect(self.ball, self.player) and self.ball.dir.y == 1:
            self.pickup_sound.play()
            if self.player.pos.x - 40 < self.ball.pos.x <= self.player.pos.x - 20:
                self.ball.dir = pygame.math.Vector2(-2, -1)
            elif self.player.pos.x - 20 < self.ball.pos.x <= self.player.pos.x - 10:
                self.ball.dir = pygame.math.Vector2(-1, -1)
            elif self.player.pos.x - 10 < self.ball.pos.x <= self.player.pos.x:
                self.ball.dir = pygame.math.Vector2(-0.5, -1)
            elif self.player.pos.x <= self.ball.pos.x < self.player.pos.x + 10:
                self.ball.dir = pygame.math.Vector2(0.5, -1)
            elif self.player.pos.x + 10 <= self.ball.pos.x < self.player.pos.x + 20:
                self.ball.dir = pygame.math.Vector2(1, -1)
            else:
                self.ball.dir = pygame.math.Vector2(2, -1)
        
        if self.ball.pos.x + 4 >= WIDTH or self.ball.pos.x - 4 <= 0:
            self.impact_sound.play()
            self.ball.dir.x *= -1
        elif self.ball.pos.y + 4 >= HEIGHT:
            # self.ball.pos.y = HEIGHT - 8
            # self.ball.dir.y *= -1
            self.player.lives -= 1
            self.playing = False
            self.ball.set_initial_dir()
            self.fail_sound.play()
        elif self.ball.pos.y-4 <= 0:
            self.ball.dir.y *= -1
            self.ball.pos.y = 5
            self.impact_sound.play()

    def write_text(self, text, pos):
        text_surface = self.font.render(text, False, WHITE)
        text_rect = text_surface.get_rect(topleft = pos)
        self.screen.blit(text_surface, text_rect)

    def display_score(self):
        self.write_text(f'Score: {self.player.score}', (0,0))
        self.write_text(f'Lives: {self.player.lives}', (WIDTH-200, 0))

    def update(self):
        if self.brick_cooldown > 0:
            self.brick_cooldown -= 1
        self.ball.update(self.playing, self.player.pos)
        self.player.update(self.ball.pos)

    def render(self):
        self.screen.blit(self.background, (0,0))
        self.brick_group.draw(self.screen)
        self.ball.draw(self.screen)
        self.player.draw(self.screen)
        self.write_text(f'{FPS //2 - int(self.ball.speed  * 1.5)}', (500,0))
        self.display_score()


    def play(self):
        self.init_game()
        while not self.gameover:
            if self.player.lives <=0:
                self.gameover = True
            if self.player.score == 1000:
                self.gameover = True
            self.check_events()
            self.collisions()
            self.update()
            self.render()
            self.clock.tick(FPS)
            pygame.display.update()
        self.start()

    def start(self):
        intro = True
        play = False

        while intro:
            self.screen.blit(self.background, (0,0))
            self.write_text('Game Over', (WIDTH//2 - 200, HEIGHT//2))
            self.write_text('Left Click to start new game...', (WIDTH//2 - 200, HEIGHT//2 + 30))
            self.display_score()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    play = True
                    intro = False
                if event.type == pygame.QUIT:
                    intro = False
                if event.type == pygame.KEYDOWN:
                    if pygame.K_ESCAPE:
                        intro = False
            self.clock.tick(FPS)
            pygame.display.update()
        

        if play:
            self.play()
        else:
            pygame.quit()
            sys.exit()
