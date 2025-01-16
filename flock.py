import numpy as np
from boid import Boid

class Flock:
    def __init__(self, num_boids, screen_width, screen_height):
        self.boids = [Boid(screen_width, screen_height) for _ in range(num_boids)]

    def apply_rules(self, separation_weight, alignment_weight, cohesion_weight, perception_radius, maxspeed):
        for boid in self.boids:
            boid.behaviour(
                self.boids,
                separation_weight=separation_weight,
                alignment_weight=alignment_weight,
                cohesion_weight=cohesion_weight,
                radius=perception_radius,
                maxspeed=maxspeed
            )

    def update(self, max_speed):
        for boid in self.boids:
            boid.update(max_speed)

    def draw(self, screen):
        for boid in self.boids:
            boid.draw(screen)