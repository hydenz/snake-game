import pygame
from pygame.locals import *
import random
import os


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load(
                dir_path + "\\assets\\square.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (35, 35))
            self.rect = self.image.get_rect()
            self.rect[0] = 0
            self.rect[1] = 0
            self.x = 0
            self.y = 0
            self.score = 0

        def move(self):
            for index, part in reversed(list(enumerate(snk_body))):
                if part == player:
                    continue
                part.rect[0] = snk_body[index-1].rect[0]
                part.rect[1] = snk_body[index-1].rect[1]
            self.rect[0] += self.x
            self.rect[1] += self.y

        def update(self):
            self.move()

    class Body(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load(
                dir_path + "\\assets\\square.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (35, 35))
            self.rect = self.image.get_rect()
            self.rect[0] = snk_body[-1].rect[0]
            self.rect[1] = snk_body[-1].rect[1]
            snk_body.append(self)
            snk_group.add(self)

    class Apple(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load(
                dir_path + "\\assets\\apple.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (35, 35))
            self.rect = self.image.get_rect()
            self.pos()

        def pos(self):
            self.rect[0] = random.randint(0, 19)*35
            self.rect[1] = random.randint(0, 19)*35
            for obj in snk_body:
                if self.rect.colliderect(obj.rect):
                    self.pos()

    def check_apple():
        if apple.rect.colliderect(player):
            apple.pos()
            Body()
            player.score += 1

    def recorde():
        if player.score > record:
            with open(f"{dir_path}\\assets\\record.txt", "w") as file:
                file.write(str(player.score))
    WIDTH = 910
    HEIGHT = 910
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    BG = pygame.surface.Surface((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    BG.fill((0, 0, 0))
    wall1 = pygame.Surface((1, HEIGHT))
    wall1.fill((255, 255, 255))
    wall1_rect = pygame.Rect(-10, 0, 1, HEIGHT)
    wall2 = pygame.Surface((1, HEIGHT))
    wall2.fill((255, 255, 255))
    wall2_rect = pygame.Rect(WIDTH+10, 0, 1, HEIGHT)
    wall3 = pygame.Surface((WIDTH, 1))
    wall3.fill((255, 255, 255))
    wall3_rect = pygame.Rect(0, -10, WIDTH, 1)
    wall4 = pygame.Surface((WIDTH, 1))
    wall4.fill((255, 255, 255))
    wall4_rect = pygame.Rect(0, HEIGHT+10, WIDTH, 1)
    walls = [wall1_rect, wall2_rect, wall3_rect, wall4_rect]
    text_rect = pygame.Rect(WIDTH/2, HEIGHT-30, 100, 100)
    font = pygame.font.SysFont("consolas", 24)
    body = pygame.Surface((35, 35))
    body.fill((255, 255, 255))
    player = Player()
    snk_body = [player]
    apple = Apple()
    head_group = pygame.sprite.Group()
    head_group.add(player)
    sprite_group = pygame.sprite.Group()
    sprite_group.add(apple)
    snk_group = pygame.sprite.Group()
    clock = pygame.time.Clock()
    with open(f"{dir_path}\\assets\\record.txt", "r") as file:
        record = int(file.read())
    while True:
        leave = 0
        clock.tick(20)
        check_apple()
        text = font.render(
            f"SCORE: {player.score}, RECORD: {record}", True, (255, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_d:
                    player.y = 0
                    player.x = 35
                    player.move()
                    check_apple()
                elif event.key == K_a:
                    player.y = 0
                    player.x = -35
                    player.move()
                    check_apple()
                elif event.key == K_w:
                    player.x = 0
                    player.y = -35
                    player.move()
                    check_apple()
                elif event.key == K_s:
                    player.x = 0
                    player.y = 35
                    player.move()
                    check_apple()
                elif event.key == K_r:
                    leave = 1
                    play_again = 1

        screen.blit(BG, (0, 0))
        screen.blit(wall1, wall1_rect)
        screen.blit(wall2, wall2_rect)
        screen.blit(wall3, wall3_rect)
        screen.blit(wall4, wall4_rect)
        sprite_group.update()
        sprite_group.draw(screen)
        head_group.update()
        head_group.draw(screen)
        snk_group.update()
        snk_group.draw(screen)
        screen.blit(text, text_rect)
        pygame.display.update()
        for obj in snk_body:
            if obj == player:
                continue
            elif player.rect.colliderect(obj.rect):
                recorde()
                main()
        for wall in walls:
            if player.rect.colliderect(wall):
                recorde()
                main()
        if leave:
            if play_again:
                main()
            else:
                pygame.quit()


main()
