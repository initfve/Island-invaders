import pygame

OCEAN = pygame.image.load("assets/Tiles/tile_73.png")
COAST = pygame.image.load("assets/Tiles/tile_02.png")
BEACH = pygame.image.load("assets/Tiles/tile_18.png")
DINGHY = pygame.image.load("assets/Ships/dinghyLarge3.png")
ROCK = pygame.image.load("assets/Tiles/tile_66.png")
PALM = pygame.image.load("assets/Tiles/tile_72.png")
BASE = [pygame.image.load("assets/Tiles/tile_46.png"), pygame.image.load("assets/Tiles/tile_47.png"),
        pygame.image.load("assets/Tiles/tile_47.png"), pygame.image.load("assets/Tiles/tile_62.png")]


class GameObject:
    def __init__(self, x, y, width, height, velocity, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = velocity
        self.image = "assets/" + image

    def draw(self, window):
        image = pygame.image.load(self.image)
        window.blit(image, (self.x, self.y))

    def moveLeft(self):
        self.x -= self.vel

    def moveRight(self):
        self.x += self.vel

    def moveUp(self):
        self.y -= self.vel

    def moveDown(self):
        self.y += self.vel


class Ship(GameObject):
    def __init__(self, x, y, width, height, velocity, image):
        self.image = image
        self.last = pygame.time.get_ticks()
        self.cooldown = 300
        self.score = 0
        image = "Ships/" + str(image)
        super().__init__(x, y, width, height, velocity, image)

    def update(self, pressed_key, width_of_screen):
        if pressed_key[pygame.K_a] and self.x > self.vel:
            self.moveLeft()

        elif pressed_key[pygame.K_d] and self.x < width_of_screen - self.width - self.vel:
            self.moveRight()


class Enemy(Ship):
    def __init__(self, x, y, width, height, velocity, image):
        image = str(image)
        super().__init__(x, y, width, height, velocity, image)

    def move(self):
        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            self.moveDown()

    @staticmethod
    def moveAllDown(enemies):
        for enemy in enemies:
            enemy.moveDown()


class Effect(GameObject):
    def __init__(self, x, y, width, height, velocity, image):
        image = "Effects/" + image
        super().__init__(x, y, width, height, velocity, image)


class Bullet(GameObject):
    def __init__(self, x, y, width, height, velocity, force, image):
        image = "Ship parts/" + str(image)
        self.force = force
        super().__init__(x, y, width, height, velocity, image)
