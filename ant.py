import pygame
from parameters import *
from vector import Vector
from math import pi, degrees, radians
import random


class Ant:
    def __init__(self, position=Vector(), nest=None):
        self.position = position
        self.velocity = Vector()
        self.max_speed = 3
        self.trigger_radius = 10
        self.smell_radius = 90
        self.scavenger = Scavenger()
        self.nest = nest
        # angle in radiant
        self.angle = -self.velocity.Heading()
        self.has_food = False
        self.isFollowingTrail = False
        self.food_source = None
        self.energy = 500
        self.color = (0, 0, 0)
        self.has_memory = False

    def ReturnToNest(self, pheromone, closest_food):
        # if it reached the nest
        if Vector.WithinRange(self.position, self.nest.position, self.nest.radius):
            self.has_food = False
            self.nest.stock += 1
            self.color = (255 - self.energy, 0, 0)
            self.angle = -self.velocity.Heading()
            self.velocity = self.velocity.Negate()
            self.position += self.velocity
            self.isFollowingTrail = False
            return
        # doesn't try to go home without this line
        self.velocity = self.scavenger.Seek(self.position, self.nest.position, self.velocity, self.max_speed)
        # add some randomness to have some more realistic movement
        wander_force = self.scavenger.Wander(self.velocity)
        self.velocity += (wander_force * 0.5)
        # changes x,y of velocity to -x,-y
        pher_direction = self.velocity.Negate()

        pheromone.AppendPheromone(self.position, pher_direction, "food", self.food_source)

    def SearchForFood(self, food_map, closest_food, pheromones):
        dist = Vector.GetDistance(self.position, closest_food.position)

        if dist < self.trigger_radius:
            self.TakeFood(closest_food)

        elif dist < self.smell_radius:
            # steps towards food source if smell is found
            self.Step(closest_food, pheromones)
        # --> Remove 57 - 60 to disable memory functionality
        elif self.has_memory:
            self.MemoryCheck(pheromones)
            wander_force = self.scavenger.Wander(self.velocity)
            self.velocity += (wander_force * 0.3)

        else:
            self.FollowPheromoneOrWander(pheromones, food_map)
            # --> Remove 63 and uncomment 65 to disable pheromone functionality
            # self.Wander()
        pheromones.AppendPheromone(self.position, self.velocity, "home")

    # 2
    def UpdateVelocity(self, foods, closest_food, pheromones):
        if self.has_food:
            self.ReturnToNest(pheromones, closest_food)
        else:
            self.SearchForFood(foods, closest_food, pheromones)

    def TakeFood(self, closest_food):
        self.has_food = True
        self.isFollowingTrail = False
        self.energy += 50
        self.UpdateColour()
        closest_food.Bite()
        self.food_source = closest_food
        if self.food_source.stock != 0:
            self.has_memory = True
        else:
            self.has_memory = False

    def Step(self, closest_food, pheromone):
        self.velocity = self.scavenger.Seek(self.position, closest_food.position, self.velocity, self.max_speed)

    def FollowPheromoneOrWander(self, pheromones, food_map):
        pheromone = self.NearPheromone(pheromones)
        desirability = 0
        if pheromone:
            # rough calculation to make nearer food sources with stronger pheromones desirable
            desirability = (pheromone.strength) * (1 / Vector.GetDistance(pheromone.position, self.position))
        if pheromone and desirability >= 0.2:
            for food in food_map.foods:
                if pheromone in food.pheromones:
                    # self.Step(food, pheromones)
                    self.isFollowingTrail = True
                    self.velocity = self.scavenger.Seek(self.position, food.position, self.velocity,
                                                        self.max_speed)
                    wander_force = self.scavenger.Wander(self.velocity)
                    self.velocity += (wander_force * 0.3)
        # only keep this to remove pheromone following
        else:
            self.velocity += self.scavenger.Wander(self.velocity)
        # pheromone.AppendPheromone(self.position, self.velocity, "home")

    def Wander(self):
        self.velocity += self.scavenger.Wander(self.velocity)

    def NearPheromone(self, pheromone_map):
        # pheromone_direction = pheromone.PheromoneDirection(self.position, self.smell_radius, "food")
        food_pheromones = pheromone_map.food_pheromones
        for pheromone in food_pheromones:
            if Vector.WithinRange(self.position, pheromone.position, 40):
                self.isFollowingTrail = True
                return pheromone
        return False

    # 1, gets pheromone from call in nest
    def Update(self, foods, pheromones, dt):
        closest_food = foods.GetClosestFood(self.position)
        self.UpdateVelocity(foods, closest_food, pheromones)
        self.velocity = self.velocity.Scale(self.max_speed)
        # self.position += self.velocity.Normalize()  * dt * self.max_speed
        self.position += self.velocity  # changing position
        self.angle = self.velocity.Heading()
        self.energy -= 0.5
        self.UpdateColour()

    def Show(self, screen):
        # initialize triangle point
        # rotate point based on the angle
        triangle = [
            (self.position + Vector(ant_size // 2, 0).Rotate(self.angle)).xy(),
            (self.position - Vector(ant_size // 2, - ant_size / 3).Rotate(self.angle)).xy(),
            (self.position - Vector(ant_size // 2, + ant_size / 3).Rotate(self.angle)).xy()
        ]
        if self.has_food:
            pygame.draw.circle(screen, (220, 130, 30),
                               (self.position + Vector(ant_size / 1.5, 0).Rotate(self.angle)).xy(), 2)

        pygame.draw.polygon(screen, self.color, triangle)

    def Turn(self):
        if random.randint(0, 15) == 1:
            self.velocity = self.velocity.Negate()
            self.position += self.velocity

    def UpdateColour(self):
        if self.energy > 255:
            self.color = (0, 0, 0)
        else:
            self.color = (255 - self.energy, 0, 0)

    def MemoryCheck(self, pheromones):
        if self.food_source.stock != 0:
            self.Step(self.food_source, pheromones)
        else:
            self.has_memory = False


class Scavenger:
    def __init__(self):
        self.wander_distance = 20
        self.wander_radius = 10
        self.wander_angle = 0.5
        self.wander_delta_angle = pi / 4

    def Seek(self, position, target, velocity, max_speed):
        diff = target - position
        diff = diff.Scale(max_speed)
        return diff

    def Wander(self, velocity):
        pos = velocity.Copy()
        pos = pos.Scale(self.wander_distance)
        displacement = Vector(-1, 1).Scale(self.wander_radius)
        # prevent ants from moving in a straight line
        displacement = displacement.SetAngle(self.wander_angle)
        self.wander_angle += random.uniform(0, 1) * self.wander_delta_angle - self.wander_delta_angle * 0.5
        return pos + displacement
