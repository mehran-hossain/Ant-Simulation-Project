import random
import pygame
from vector import Vector
from parameters import *
from ant import Ant

pygame.font.init()
text_color = (white)
text_font = pygame.font.SysFont("Arial", 35)


class Nest:
    def __init__(self, position, n_ants=20):
        self.position = position
        self.n_ants = n_ants
        self.stock = 0
        self.ants = self.InitializeAnts()
        self.radius = 45
        self.color = (82, 59, 51)
        self.dead = 0

    def InitializeAnts(self):
        return [Ant(self.position, self) for _ in range(self.n_ants)]

    def Update(self, food_map, pheromones, dt):
        for ant in self.ants:
            # move ants
            if ant.energy != 0:
                ant.Update(food_map, pheromones, dt)
            else:
                self.ants.remove(ant)
                print(self.dead)
                self.dead += 1
                if self.dead == self.n_ants - 1:
                    print("dead", pygame.time.get_ticks() / 1000)
            # Handling boundary movement
            if ant.position.x < 0:
                ant.position.x = 0
                Ant.Turn(ant)
            elif ant.position.x > width:
                ant.position.x = width
                Ant.Turn(ant)
            if ant.position.y < 0:
                ant.position.y = 0
                Ant.Turn(ant)
            elif ant.position.y > height:
                ant.position.y = height
                Ant.Turn(ant)

    def Show(self, screen, show_stock=True):
        pygame.draw.circle(screen, self.color, self.position.xy(), self.radius)

        if show_stock:
            text_surface = text_font.render(str(self.stock), True, text_color)
            text_rectangle = text_surface.get_rect(center=self.position.xy())
            screen.blit(text_surface, text_rectangle)
        for ant in self.ants:
            ant.Show(screen)
