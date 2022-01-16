from parameters import *
from vector import *
from nest import *
from pheromone import *
from food import *


class Colony:
    def __init__(self):
        self.nest = Nest(Vector(width // 2, height // 2), ant_count)
        self.food = FoodMap(food_stock_count)
        self.pheromones = PheromoneMap()

    def Update(self, screen, showFoodTrail, showHomeTrail, delta_time):
        self.nest.Update(self.food, self.pheromones, delta_time)
        self.food.Update()
        self.pheromones.Update(screen, showFoodTrail, showHomeTrail, self.food.foods)

    def Show(self, screen):
        self.nest.Show(screen)
        self.food.Show(screen)
