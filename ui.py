import pygame
import numpy as np
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, NUM_BOIDS
import time
class Panel:
    def __init__(self, x, y, width, height, color=(0, 0, 150), border_color=(255, 0, 0), border_width=6):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.height = height
        self.width = width
        self.x=x
        self.y=y

    def Render(self, screen):
        # Draw the panel with border
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)



class DigitInputBox:
    def __init__(self, x, y, width, height, initial_value=1.00, min_value=0.00, max_value=9.99, step=0.5, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        self.rect = pygame.Rect(x, y, width, height)
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.value = initial_value
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.font = pygame.font.Font('freesansbold.ttf', int(20*screen_height/SCREEN_HEIGHT))
        self.color = (170, 170, 170)
        self.text_color = (0, 0, 0)
        self.active = False

        
        self.text = f"{initial_value:.2f}"
        self.cursor_visible = True
        self.last_blink_time = time.time()
        self.cursor_blink_interval = 0.5  # Cursor blinks every 0.5 seconds
    
        # Arrow buttons
        self.up_arrow = pygame.Rect(x + width + 5, y, height, height // 2)
        self.down_arrow = pygame.Rect(x + width + 5, y + height // 2, height, height // 2)

        # Tooltip
        self.show_tooltip = False
        self.tooltip_font = pygame.font.Font('freesansbold.ttf', int(18* screen_height/SCREEN_HEIGHT))
        self.tooltip_text = f"Click to type values between {min_value} and {max_value}"

        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        # Show tooltip when hovering over the input box
        self.show_tooltip = self.rect.collidepoint(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            elif self.up_arrow.collidepoint(event.pos):
                self.value = min(self.max_value, self.value + self.step)
                self.text = f"{self.value:.2f}"
            elif self.down_arrow.collidepoint(event.pos):
                self.value = max(self.min_value, self.value - self.step)
                self.text = f"{self.value:.2f}"
            else:
                self.active = False
            
            if len(self.text) > 5:
                self.text = self.text[1:]

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Remove last character
                if not self.text:  # If empty, reset to "0.00"
                    # self.text = "00.00"
                    self.value=self.min_value
                else:
                    self.value = float(self.text)
            elif event.unicode.isdigit() or (event.unicode == "." and "." not in self.text):
                # Append valid digit or decimal point
                if len(self.text) < 5:  # Limit to 5 characters (e.g., "09.99")
                    self.text += event.unicode
                try:
                    new_value = float(self.text)
                    if self.min_value <= new_value <= self.max_value:
                        self.value = new_value
                    else:
                        self.text = f"{self.value:.2f}"  # Revert to last valid value
                except ValueError:
                    pass
                if len(self.text) > 5:
                    self.text = self.text[1:]
            # elif event.key == pygame.K_RETURN:
            #     self.active=False

    def render(self, screen):
        # Draw the input box
        border_color = (255, 0, 0) if self.active else self.color
        
        pygame.draw.rect(screen, border_color, self.rect)
        # pygame.draw.rect(screen, self.color, self.rect)

        # Manage cursor blinking
        current_time = time.time()
        if self.active and current_time - self.last_blink_time > self.cursor_blink_interval:
            self.cursor_visible = not self.cursor_visible
            self.last_blink_time = current_time

        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        # Render the blinking cursor if active
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right
            cursor_y = text_rect.top 
            cursor_height = text_rect.height - 3 * self.screen_height/SCREEN_HEIGHT
            pygame.draw.line(screen, self.text_color, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

        # Draw up arrow
        pygame.draw.polygon(screen, (0, 0, 0), [
            (self.up_arrow.centerx, self.up_arrow.top + 5*self.screen_height/SCREEN_HEIGHT),
            (self.up_arrow.left + 5*self.screen_height/SCREEN_HEIGHT, self.up_arrow.bottom - 5*self.screen_height/SCREEN_HEIGHT),
            (self.up_arrow.right - 5*self.screen_height/SCREEN_HEIGHT, self.up_arrow.bottom - 5*self.screen_height/SCREEN_HEIGHT)
        ])
        # Draw down arrow
        pygame.draw.polygon(screen, (0, 0, 0), [
            (self.down_arrow.centerx, self.down_arrow.bottom - 5*self.screen_height/SCREEN_HEIGHT),
            (self.down_arrow.left + 5*self.screen_height/SCREEN_HEIGHT, self.down_arrow.top + 5*self.screen_height/SCREEN_HEIGHT),
            (self.down_arrow.right - 5*self.screen_height/SCREEN_HEIGHT, self.down_arrow.top + 5*self.screen_height/SCREEN_HEIGHT)
        ])

        # Render tooltip if hovering
        if self.show_tooltip:
            tooltip_surface = self.tooltip_font.render(self.tooltip_text, True, (0, 0, 0))
            tooltip_bg = tooltip_surface.get_rect(topleft=(3.3*self.screen_width/5, 0.15*self.screen_height))
            pygame.draw.rect(screen, (255, 255, 255), tooltip_bg.inflate(10, 5))  # Background with padding
            screen.blit(tooltip_surface, tooltip_bg)

    def get_value(self):
        return self.value

class TextUI:
    def __init__(self, text, x, y, font_size=30, color=(0, 0, 0), font_name='freesansbold.ttf'):
        """
        Initialize a text label.

        Args:
            text (str): The text to display.
            x (int): X-coordinate of the text position.
            y (int): Y-coordinate of the text position.
            font_size (int): Font size of the text.
            color (tuple): RGB color of the text.
            font_name (str): Font name (use a system font or a .ttf file).
        """
        self.text = text
        self.position = (x, y)
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(font_name, font_size)

    def set_text(self, text):
        """
        Update the text to display.

        Args:
            text (str): The new text to display.
        """
        self.text = text

    def render(self, screen):
        """
        Render the text on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the text on.
        """
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.position)


class SemiCirclePanel:
    def __init__(self, x, y, radius, color=(0, 0, 0), text="Menu", subtext="Click or press space", text_color=(255, 255, 255), screen_height=SCREEN_HEIGHT):
        """
        Initialize a semicircular panel.

        Args:
            x (int): X-coordinate of the semicircle's center.
            y (int): Y-coordinate of the semicircle's center.
            radius (int): Radius of the semicircle.
            color (tuple): RGB color of the semicircle.
            text (str): Main label text displayed on the semicircle.
            subtext (str): Subtext displayed below the main text.
            text_color (tuple): RGB color of the text.
        """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.text = text
        self.subtext = subtext
        self.text_color = text_color
        self.screen_height=screen_height

    def render(self, screen):
        """Draw the semicircle panel and its labels."""
        # Draw the semicircle
        rect = pygame.Rect(self.x - self.radius, self.y, 2 * self.radius, self.radius)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)  

        # Fonts
        font_main = pygame.font.Font('freesansbold.ttf', int(30* self.screen_height/SCREEN_HEIGHT))
        font_subtext = pygame.font.Font('freesansbold.ttf', int(16* self.screen_height/SCREEN_HEIGHT))

        # Render main text
        text_surface = font_main.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x, self.y + self.radius // 3))
        screen.blit(text_surface, text_rect)

        # Render subtext
        subtext_surface = font_subtext.render(self.subtext, True, self.text_color)
        subtext_rect = subtext_surface.get_rect(center=(self.x, self.y + self.radius // 2))
        screen.blit(subtext_surface, subtext_rect)

    def is_clicked(self, mouse_pos):
        """
        Check if the semicircle is clicked.

        Args:
            mouse_pos (tuple): (x, y) position of the mouse click.

        Returns:
            bool: True if the click is inside the semicircle, False otherwise.
        """
        dx, dy = mouse_pos[0] - self.x, mouse_pos[1] - self.y
        return dx**2 + dy**2 <= self.radius**2 and dy >= 0  # Ensure within the semicircle bounds

class Button:
    def __init__(self, x, y, width, height, text, font_size=20, color=(200, 200, 200), text_color=(0, 0, 0), screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, tooltip_text = "Text"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.text_color = text_color

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tooltip_text = tooltip_text

        # Tooltip
        self.show_tooltip = False
        self.tooltip_font = pygame.font.Font('freesansbold.ttf', int(18* screen_height/SCREEN_HEIGHT))

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        # Render tooltip if hovering
        if self.show_tooltip:
            tooltip_surface = self.tooltip_font.render(self.tooltip_text, True, (0, 0, 0))
            tooltip_bg = tooltip_surface.get_rect(topleft=(3.3*self.screen_width/5, 0.15*self.screen_height))
            pygame.draw.rect(screen, (255, 255, 255), tooltip_bg.inflate(10, 5))  # Background with padding
            screen.blit(tooltip_surface, tooltip_bg)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        # Show tooltip when hovering over the button
        self.show_tooltip = self.rect.collidepoint(mouse_pos)
    

import pygame
import time


class IntegerInputBox:
    def __init__(self, x, y, width, height, initial_value=100, min_value=1, max_value=300, step=1, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = initial_value
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.font = pygame.font.Font('freesansbold.ttf', int(20* screen_height/SCREEN_HEIGHT))
        self.color = (170, 170, 170)
        self.text_color = (0, 0, 0)
        self.active = False

        self.text = str(initial_value)  # Initial text representation of the value
        self.cursor_visible = True
        self.last_blink_time = time.time()
        self.cursor_blink_interval = 0.5  # Cursor blinks every 0.5 seconds

        # Arrow buttons
        self.up_arrow = pygame.Rect(x + width + 5, y, height, height // 2)
        self.down_arrow = pygame.Rect(x + width + 5, y + height // 2, height, height // 2)

        # Tooltip
        self.show_tooltip = False
        self.tooltip_font = pygame.font.Font('freesansbold.ttf', int(18*screen_height/SCREEN_HEIGHT))
        self.tooltip_text = f"Enter an integer between {min_value} and {max_value}"

        self.screen_width = screen_width
        self.screen_height=screen_height

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        # Show tooltip when hovering over the input box
        self.show_tooltip = self.rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            elif self.up_arrow.collidepoint(event.pos):
                self.value = min(self.max_value, self.value + self.step)
                self.text = str(self.value)
            elif self.down_arrow.collidepoint(event.pos):
                self.value = max(self.min_value, self.value - self.step)
                self.text = str(self.value)
            else:
                self.active = False

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Remove last character
                self.value = int(self.text) if self.text.isdigit() else self.min_value
            elif event.unicode.isdigit():
                new_text = self.text + event.unicode
                if self.min_value <= int(new_text) <= self.max_value:
                    self.text = new_text
                    self.value = int(new_text)
            elif event.key == pygame.K_RETURN:
                self.active = False

    def render(self, screen):
        # Draw the input box
        border_color = (255, 0, 0) if self.active else self.color
        pygame.draw.rect(screen, border_color, self.rect)


        # Manage cursor blinking
        current_time = time.time()
        if self.active and current_time - self.last_blink_time > self.cursor_blink_interval:
            self.cursor_visible = not self.cursor_visible
            self.last_blink_time = current_time

        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

        # Render the blinking cursor if active
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2 * self.screen_height/SCREEN_HEIGHT
            cursor_y = text_rect.top
            pygame.draw.line(screen, self.text_color, (cursor_x, cursor_y), (cursor_x, cursor_y + text_rect.height), 2)

        # Draw up arrow
        pygame.draw.polygon(screen, (0, 0, 0), [
            (self.up_arrow.centerx, self.up_arrow.top + 5* self.screen_height/SCREEN_HEIGHT),
            (self.up_arrow.left + 5* self.screen_height/SCREEN_HEIGHT, self.up_arrow.bottom - 5* self.screen_height/SCREEN_HEIGHT),
            (self.up_arrow.right - 5* self.screen_height/SCREEN_HEIGHT, self.up_arrow.bottom - 5* self.screen_height/SCREEN_HEIGHT)
        ])
        # Draw down arrow
        pygame.draw.polygon(screen, (0, 0, 0), [
            (self.down_arrow.centerx, self.down_arrow.bottom - 5* self.screen_height/SCREEN_HEIGHT),
            (self.down_arrow.left + 5* self.screen_height/SCREEN_HEIGHT, self.down_arrow.top + 5* self.screen_height/SCREEN_HEIGHT),
            (self.down_arrow.right - 5* self.screen_height/SCREEN_HEIGHT, self.down_arrow.top + 5* self.screen_height/SCREEN_HEIGHT)
        ])

        # Render tooltip if hovering
        if self.show_tooltip:
            tooltip_surface = self.tooltip_font.render(self.tooltip_text, True, (0, 0, 0))
            tooltip_bg = tooltip_surface.get_rect(topleft=(3.3*self.screen_width/5, 0.15*self.screen_height))
            pygame.draw.rect(screen, (255, 255, 255), tooltip_bg.inflate(10, 5))  # Background with padding
            screen.blit(tooltip_surface, tooltip_bg)

    def get_value(self):
        return self.value