import pygame
import random
import os
pygame.mixer.init()

class Partical:
    def __init__(self, pos : list, vel : list, radius: int, color = 0, explode: bool = False, rocket : bool = True):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.explode = explode
        self.rocket = rocket
        self.color = color
    
    def update(self):
        if self.explode:
            self.radius -= 0.09
            self.vel[1] += 0.04
        if self.rocket:
            self.vel[1] += 0.13 
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def get_surf(self, radius, color):
        surf = pygame.Surface((int(radius * 2), int(radius * 2)))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])),  int(self.radius))
        screen.blit(self.get_surf(self.radius * 2, (20, 20, 20)), (int(self.pos[0] - self.radius * 2), int(self.pos[1] - self.radius * 2)),  special_flags=pygame.BLEND_RGB_ADD)

class Firework:
    def __init__(self):
        self.width : int = 500
        self.height : int = 850
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("FireWork")
        self.fly = pygame.mixer.Sound(os.path.join("assects", "whistel.mp3"))
        self.boom = pygame.mixer.Sound(os.path.join("assects", "boom.mp3"))
        self.fly.set_volume(0.1)
        self.particals = []
        self.temp_partical = []

    def blast(self, pos, color):
        for _ in range(100):
            self.temp_partical.append(
                Partical([pos[0], pos[1]],
                        [random.randint(-20, 20)/10 , random.randint(-20, 20)/10],
                        (random.randrange(2, 8)),
                        color,
                        True,
                        False)
                        )

    def get_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))



    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.screen.fill((0, 0, 0))

            if random.random() < 0.02:
                self.particals.append(
                    Partical(
                        [random.randrange(self.width), self.height],
                        [0, random.randint(-14, -9)], 2,
                        self.get_random_color())
                        )
                self.fly.play()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.temp_partical = self.particals.copy()
            for partical in self.particals:
                partical.draw(self.screen)
                partical.update()

                if partical.vel[1] > 0 and partical.rocket:
                    self.blast(partical.pos, partical.color)
                    self.boom.play()
                    self.temp_partical.remove(partical)

                if partical.radius <= 0:
                    self.temp_partical.remove(partical)
            self.particals = self.temp_partical
            pygame.display.update()
            clock.tick(60)

Firework().run()
