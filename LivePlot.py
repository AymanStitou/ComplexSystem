import pygame
from settings import SCREEN_HEIGHT


class LivePlot:
    def __init__(self, x, y, width, height, max_points=100, min_y_scale=10, screen_height=SCREEN_HEIGHT):
        """
        Initializes the live plot object.

        Args:
            x (int): The x-coordinate of the plot.
            y (int): The y-coordinate of the plot.
            width (int): The width of the plot.
            height (int): The height of the plot.
            max_points (int): Maximum number of points to display on the plot.
            min_y_scale (int): Minimum y-axis scale for readability.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_points = max_points
        self.min_y_scale = min_y_scale
        self.data = []
        self.max_speed = []
        self.font = pygame.font.Font(None, int(25*screen_height/SCREEN_HEIGHT))  # Font for labels and ticks
        self.screen_height=screen_height

    def add_data(self, avg_velocity, max_speed):
        """
        Adds a new data point to the plot.

        Args:
            avg_velocity (float): The average velocity of the boids.
            max_speed (float): The current maximum speed of the boids.
        """
        if len(self.data) >= self.max_points:
            self.data.pop(0)
            self.max_speed.pop(0)
        self.data.append(avg_velocity)
        self.max_speed.append(max_speed)

    def render(self, screen):
        """
        Renders the live plot on the given screen.

        Args:
            screen (pygame.Surface): The screen to render the plot on.
        """
        self._update_font()
        # Draw plot background
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

        if len(self.data) == 0:
            return  # No data to plot

        # Normalize data for plotting
        max_y = max(self.min_y_scale, max(self.data + self.max_speed) * 1.1)  # Dynamic scaling with a minimum threshold
        scale_x = self.width / self.max_points
        scale_y = self.height / max_y

        # Plot average velocity
        for i in range(len(self.data) - 1):
            x1 = self.x + i * scale_x
            y1 = self.y + self.height - self.data[i] * scale_y
            x2 = self.x + (i + 1) * scale_x
            y2 = self.y + self.height - self.data[i + 1] * scale_y
            pygame.draw.line(screen, (255, 0, 0), (x1, y1), (x2, y2), int(4 * self.screen_height/SCREEN_HEIGHT))

        # Plot max speed line
        for i in range(len(self.max_speed) - 1):
            x1 = self.x + i * scale_x
            y1 = self.y + self.height - self.max_speed[i] * scale_y
            x2 = self.x + (i + 1) * scale_x
            y2 = self.y + self.height - self.max_speed[i + 1] * scale_y
            pygame.draw.line(screen, (0, 0, 255), (x1, y1), (x2, y2), int(4 * self.screen_height/SCREEN_HEIGHT))

        # Add axis labels
        y_label = self.font.render("Velocity", True, (0, 0, 0))
        # screen.blit(y_label, (self.x - y_label.get_width() - 10, self.y + self.height // 2 - y_label.get_height() // 2))
        y_label_surface_rotated = pygame.transform.rotate(y_label, 90)  # Rotate text 90 degrees
        y_label_rect = y_label_surface_rotated.get_rect(center=(self.x - y_label_surface_rotated.get_height() // 2 - 15, self.y + self.height // 2))
        screen.blit(y_label_surface_rotated, y_label_rect)
        # Add legend
        avg_legend = self.font.render("Avg Velocity", True, (255, 0, 0))
        max_speed_legend = self.font.render("Max Speed", True, (0, 0, 255))
        screen.blit(avg_legend, (1.02*self.x, self.y - self.height/8))
        screen.blit(max_speed_legend, (self.x + 1*self.width/2, self.y - self.height/8))

        # Add y ticks
        num_ticks = 5
        for i in range(num_ticks + 1):
            # Y ticks
            y_tick_value = max_y / num_ticks * i
            y_tick_y = self.y + self.height - (y_tick_value * scale_y)
            y_tick_label = self.font.render(f"{y_tick_value:.1f}", True, (0, 0, 0))
            screen.blit(y_tick_label, (self.x - y_tick_label.get_width() - 5, y_tick_y - y_tick_label.get_height() // 2))
        # Print current average velocity
        if self.data:
            avg_text = f"Avg Velocity ~ {self.data[-1]:.2f}"
            avg_surface = self.font.render(avg_text, True, (0, 0, 0))
            screen.blit(avg_surface, (self.x + self.width // 2 - avg_surface.get_width() // 2, self.y + self.height + 10))

    def _update_font(self):
        """Update the font size dynamically based on screen height."""
        font_size = int(25 * self.screen_height / SCREEN_HEIGHT)
        self.font = pygame.font.Font(None, max(10, font_size))  # Ensure minimum font size of 10

    def set_screen_height(self, screen_height):
        """Update the screen height and recalculate font size."""
        self.screen_height = screen_height
        self._update_font()


import pygame

class LivePlotNeighbours:
    def __init__(self, x, y, width, height, max_points=100, min_y_scale=10, screen_height=SCREEN_HEIGHT):
        """
        Initializes the live plot object for average neighbors.

        Args:
            x (int): The x-coordinate of the plot.
            y (int): The y-coordinate of the plot.
            width (int): The width of the plot.
            height (int): The height of the plot.
            max_points (int): Maximum number of points to display on the plot.
            min_y_scale (int): Minimum y-axis scale for readability.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_points = max_points
        self.min_y_scale = min_y_scale
        self.data = []
        self.max_neighbours = []
        self.font = pygame.font.Font(None, int(25*screen_height/SCREEN_HEIGHT))  # Font for labels and ticks
        self.screen_height=screen_height

    def add_data(self, avg_neighbours, max_neighbours):
        """
        Adds a new data point to the plot.

        Args:
            avg_neighbours (float): The average number of neighbors of the boids.
            max_neighbours (int): The maximum possible neighbors (num_boids - 1).
        """
        if len(self.data) >= self.max_points:
            self.data.pop(0)
            self.max_neighbours.pop(0)
        self.data.append(avg_neighbours)
        self.max_neighbours.append(max_neighbours)

    def render(self, screen):
        """
        Renders the live plot on the given screen.

        Args:
            screen (pygame.Surface): The screen to render the plot on.
        """
        self._update_font()
        # Draw plot background
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

        if len(self.data) == 0:
            return  # No data to plot

        # Normalize data for plotting
        max_y = max(self.min_y_scale, max(self.data + self.max_neighbours) * 1.1)  # Dynamic scaling with a minimum threshold
        scale_x = self.width / self.max_points
        scale_y = self.height / max_y

        # Plot average neighbors
        for i in range(len(self.data) - 1):
            x1 = self.x + i * scale_x
            y1 = self.y + self.height - self.data[i] * scale_y
            x2 = self.x + (i + 1) * scale_x
            y2 = self.y + self.height - self.data[i + 1] * scale_y
            pygame.draw.line(screen, (0, 200, 0), (x1, y1), (x2, y2), int(4 * self.screen_height/SCREEN_HEIGHT))

        # Plot max neighbors line
        for i in range(len(self.max_neighbours) - 1):
            x1 = self.x + i * scale_x
            y1 = self.y + self.height - self.max_neighbours[i] * scale_y
            x2 = self.x + (i + 1) * scale_x
            y2 = self.y + self.height - self.max_neighbours[i + 1] * scale_y
            pygame.draw.line(screen, (0, 0, 255), (x1, y1), (x2, y2), int(4 * self.screen_height/SCREEN_HEIGHT))

        # Add axis labels
        y_label = self.font.render("Neighbors", True, (0, 0, 0))
        # screen.blit(y_label, (self.x - y_label.get_width() - 10, self.y + self.height // 2 - y_label.get_height() // 2))
        y_label_surface_rotated = pygame.transform.rotate(y_label, 90)  # Rotate text 90 degrees
        y_label_rect = y_label_surface_rotated.get_rect(center=(self.x - y_label_surface_rotated.get_height() // 2 - 15, self.y + self.height // 2))
        screen.blit(y_label_surface_rotated, y_label_rect)

        # Add legend
        avg_legend = self.font.render("Avg Neighbors", True, (0, 200, 0))
        max_neighbours_legend = self.font.render("Max Neighbors", True, (0, 0, 255))
        screen.blit(avg_legend, (1.02*self.x, self.y - self.height/8))
        screen.blit(max_neighbours_legend, (self.x + 1*self.width/2, self.y - self.height/8))

        # Add y ticks
        num_ticks = 5
        for i in range(num_ticks + 1):
            # Y ticks
            y_tick_value = max_y / num_ticks * i
            y_tick_y = self.y + self.height - (y_tick_value * scale_y)
            y_tick_label = self.font.render(f"{y_tick_value:.1f}", True, (0, 0, 0))
            screen.blit(y_tick_label, (self.x - y_tick_label.get_width() - 5, y_tick_y - y_tick_label.get_height() // 2))

        # Print current average neighbors
        if self.data:
            avg_text = f"Avg Neighbors ~ {self.data[-1]:.2f}"
            avg_surface = self.font.render(avg_text, True, (0, 0, 0))
            screen.blit(avg_surface, (self.x + self.width // 2 - avg_surface.get_width() // 2, self.y + self.height + 10))

    def _update_font(self):
        """Update the font size dynamically based on screen height."""
        font_size = int(25 * self.screen_height / SCREEN_HEIGHT)
        self.font = pygame.font.Font(None, max(10, font_size))  # Ensure minimum font size of 10

    def set_screen_height(self, screen_height):
        """Update the screen height and recalculate font size."""
        self.screen_height = screen_height
        self._update_font()