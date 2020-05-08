import random

import pygame

from games_objects import Enemy, Ship, OCEAN, COAST, BEACH, BASE, DINGHY, ROCK, PALM, Effect, Bullet


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Ships")
        self.width = 800
        self.height = 600
        self.win = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.bullets = []
        self.effects = []
        self.font = pygame.font.Font(None, 30)

        self.player = Ship(380, 420, 40, 68, 10, 'player.png')
        self.enemies = [Enemy(100, 30, 66, 113, 1, 'ship (19).png'),
                        Enemy(250, 0, 66, 113, 1, 'ship (20).png'),
                        Enemy(400, 15, 66, 113, 1, 'ship (21).png'),
                        Enemy(500, 15, 66, 113, 1, 'ship (22).png')]

    def paintBackground(self):
        for y in range(0, self.height - 100, 64):
            for x in range(0, self.width, 64):
                self.win.blit(OCEAN, (x, y))

        for x in range(0, self.width, 64):
            self.win.blit(COAST, (x, self.height - 100))
        for x in range(0, self.width, 64):
            self.win.blit(BEACH, (x, self.height - 50))

        self.win.blit(DINGHY, (680, self.height - 100))
        self.win.blit(ROCK, (700, self.height - 80))
        self.win.blit(PALM, (700, self.height - 80))

        for i in range(len(BASE)):
            self.win.blit(BASE[i], (20 + 60 * i, self.height - 70))

        text = self.font.render("Score: " + str(self.player.score), 1, (0, 0, 0))
        self.win.blit(text, (self.width - 120, 20))

    def showText(self, text):
        self.redrawGameWindow()

        font = pygame.font.Font(None, 60)
        text = font.render(text, 1, (0, 0, 0))
        x = self.width / 2 - text.get_size()[0] / 2

        self.win.blit(text, (x, 250))
        pygame.display.update()
        pygame.time.wait(2000)
        self.redrawGameWindow()

    def redrawGameWindow(self):
        self.paintBackground()
        self.player.draw(self.win)

        for enemy in self.enemies:
            enemy.draw(self.win)
        for bullet in self.bullets:
            bullet.draw(self.win)
        for effect in self.effects:
            effect.draw(self.win)

        pygame.display.update()

    def start(self):
        run = True

        self.showText("Defend your island!")
        while run:
            self.clock.tick(30)

            for event in pygame.event.get():
                run = False if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE else True

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a] or keys[pygame.K_d]:
                self.player.update(keys, self.width)
                Enemy.moveAllDown(self.enemies)

            if keys[pygame.K_SPACE]:
                now = pygame.time.get_ticks()
                if now - self.player.last >= self.player.cooldown:
                    self.player.last = now
                    g.bullets.append(Bullet(self.player.x + 15, self.player.y + 5, 10, 10, 5, 1, 'cannonBall.png'))

            if len(self.enemies) < 4:  # generate new enemies
                self.enemies.append(
                    Enemy(random.randint(0, 500), 0, 66, 108, 0.1 * (self.player.score // 10) + 1,
                          f'ship ({random.randint(19, 24)}).png'))

            for enemy in self.enemies:
                enemy.moveDown()
                if enemy.y > self.height - enemy.height - 90 or (
                        enemy.x <= self.player.x < enemy.x + enemy.width and enemy.y + enemy.height >= self.player.y):
                    self.showText(f"You lose! {self.player.score} points")  # if enemy reach island or player's ship
                    run = False

            for bullet in self.bullets:
                bullet.moveUp() if bullet.y > 0 else self.bullets.pop(self.bullets.index(bullet))

                for enemy in self.enemies:
                    if enemy.x < bullet.x < enemy.x + enemy.width and enemy.y <= bullet.y < enemy.y + enemy.height:
                        self.bullets.pop(self.bullets.index(bullet))
                        self.effects.append(Effect(enemy.x, enemy.y, 75, 75, 0, "explosion1.png"))
                        self.enemies.pop(self.enemies.index(enemy))
                        self.player.score += 1

            self.redrawGameWindow()
            self.effects = []
        pygame.quit()


Game().start()
