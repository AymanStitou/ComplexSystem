import random
import pygame
import numpy as np
from settings import SCREEN_HEIGHT

class Boid:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position = pygame.math.Vector2(random.uniform(0, self.screen_width), random.uniform(0, self.screen_height))
        angle = random.uniform(0, 360)
        self.velocity = pygame.math.Vector2(1, 0).rotate(angle) * random.uniform(1.5, 4)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.max_speed = 4
        self.max_force = 0.1

        # Load and scale the sprite image
        self.image = pygame.image.load("bird.png")
        self.image = pygame.transform.scale(self.image, (20* self.screen_height/SCREEN_HEIGHT, 20* self.screen_height/SCREEN_HEIGHT))  # Resize the image
        self.original_image = self.image  # Keep an unrotated copy

    def limits(self):
        """Ensure the boid wraps around the screen edges."""
        self.position.x %= self.screen_width
        self.position.y %= self.screen_height

    def get_neighbours(self, flock, radius):
        """Find neighboring boids within a given radius."""
        neighbours = [other for other in flock if other != self and self.position.distance_to(other.position) < radius]
        return neighbours

    def separation(self, neighbours, max_speed):
        """Calculate the separation force to avoid crowding."""
        steering = pygame.math.Vector2(0, 0)
        for other in neighbours:
            diff = self.position - other.position
            distance = diff.length()
            if distance > 0:  # Avoid division by zero
                diff.scale_to_length(1 / distance)  # Weight inversely to distance
                steering += diff
        if len(neighbours) > 0:
            steering /= len(neighbours)
            steering = self._steer_towards(steering, max_speed)
        return steering

    def alignment(self, neighbours, max_speed):
        """Calculate the alignment force to align velocity with neighbors."""
        steering = pygame.math.Vector2(0, 0)
        for other in neighbours:
            steering += other.velocity
        if len(neighbours) > 0:
            steering /= len(neighbours)
            steering = self._steer_towards(steering, max_speed)
        return steering

    def cohesion(self, neighbours, max_speed):
        """Calculate the cohesion force to steer towards the center of mass."""
        steering = pygame.math.Vector2(0, 0)
        for other in neighbours:
            steering += other.position
        if len(neighbours) > 0:
            steering /= len(neighbours)
            steering -= self.position
            steering = self._steer_towards(steering, max_speed)
        return steering

    def _steer_towards(self, vector, max_speed):
        """Calculate a steering force towards a given vector."""
        if max_speed <= 0:
            max_speed = 0.1  # Ensure max_speed is not zero or negative

        if vector.length() > 0:
            vector.scale_to_length(max_speed)
        steering = vector - self.velocity
        if steering.length() > self.max_force:
            steering.scale_to_length(self.max_force)
        return steering

    def behaviour(self, flock, separation_weight, alignment_weight, cohesion_weight, radius, maxspeed):
        """Combine separation, alignment, and cohesion forces."""
        neighbours = self.get_neighbours(flock, radius)
        self.acceleration = pygame.math.Vector2(0, 0)

        separation_force = self.separation(neighbours, maxspeed) * separation_weight
        alignment_force = self.alignment(neighbours, maxspeed) * alignment_weight
        cohesion_force = self.cohesion(neighbours, maxspeed) * cohesion_weight

        self.acceleration += separation_force
        self.acceleration += alignment_force
        self.acceleration += cohesion_force

    def update(self, max_speed):
        """Update the boid's position, velocity, and wrap around the screen."""
        if max_speed <= 0:
            max_speed = 0.1  # Ensure max_speed is not zero or negative

        self.velocity += self.acceleration
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)
        self.position += self.velocity
        self.limits()

    def draw(self, screen):
        # Calculate the angle of the boid's velocity vector
        angle = np.degrees(np.arctan2(self.velocity[1], self.velocity[0]))
        rotated_image = pygame.transform.rotate(self.original_image, 320-angle)  # Rotate the image
        rect = rotated_image.get_rect(center=(self.position[0], self.position[1]))
        screen.blit(rotated_image, rect.topleft)

    def draw_perception_radius(self, screen, radius):
        """Draw the perception radius of the boid."""
        pygame.draw.circle(screen, (255, 0, 0), (self.position.x, self.position.y), radius, int(4* self.screen_height/SCREEN_HEIGHT))  
