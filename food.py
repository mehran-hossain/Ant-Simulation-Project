import sys

import pygame
from parameters import *
from random import randint
from vector import Vector

screen_offset = 30
pygame.font.init()
text_color = white


class Food:
    def __init__(self, position):
        self.position = position
        self.stock = 20
        self.bite_size = 1
        self.color = (220, 130, 30)
        self.pheromones = []

    def AppendFoodPheromone(self, pher):
        # print(len(self.pheromones))
        self.pheromones.append(pher)

    def Bite(self):
        self.stock -= self.bite_size

    def Update(self):
        if self.stock < 0:
            pass
            # self.position.x = randint(screen_offset, width-screen_offset)
            # self.position.y = randint(screen_offset,height-screen_offset)
            # self.stock = 25

    def Show(self, screen, show_remaining=True):
        if self.stock > 0:
            # print("ye", self.stock)
            pygame.draw.circle(screen, self.color, self.position.xy(), self.stock + 5)

        if show_remaining:
            text_font = pygame.font.SysFont("Arial", self.stock)
            text_surface = text_font.render(str(self.stock), True, text_color)
            text_rectangle = text_surface.get_rect(center=self.position.xy())
            screen.blit(text_surface, text_rectangle)


class FoodMap:
    def __init__(self, food_stock):
        # food_stock -> food_stock_count
        self.size = food_stock
        self.foods = self.InitializeFood()

    def InitializeFood(self):
        # return [
        #     Food(Vector(randint(screen_offset, width - screen_offset), randint(screen_offset, height - screen_offset)))
        #     for _ in range(self.size)]
        return [Food(Vector(100, 300)), Food(Vector(500, 300)), Food(Vector(700, 600)), Food(Vector(800, 800)), Food(Vector(1200, 100)), Food(Vector(1400, 800))]

    def Update(self):
        for food in self.foods:
            food.Update()
            if food.stock <= 0:
                self.foods.remove(food)

    def GetClosestFood(self, position):
        # finds closest food source from a given position
        if len(self.foods) == 0:
            print("finish", pygame.time.get_ticks() / 1000)
            pygame.quit()
            sys.exit()
        closest_food = self.foods[0]
        closest_distance = Vector.GetDistanceSQ(position, closest_food.position)
        temp_distance = closest_distance

        for x in range(1, len(self.foods)):
            temp_distance = Vector.GetDistanceSQ(position, self.foods[x].position)
            if temp_distance < closest_distance:
                closest_food = self.foods[x]
                closest_distance = temp_distance

        return closest_food

    def Show(self, screen):
        for food in self.foods:
            food.Show(screen)
