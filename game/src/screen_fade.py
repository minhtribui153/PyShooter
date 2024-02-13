import pygame

class ScreenFade():
    def __init__(self, direction, colour, speed, screen_width, screen_height):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def fade(self, screen):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, self.screen_width // 2, self.screen_height))
            pygame.draw.rect(screen, self.colour, (self.screen_width // 2 + self.fade_counter, 0, self.screen_width, self.screen_height))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, self.screen_width, self.screen_height // 2))
            pygame.draw.rect(screen, self.colour, (0, self.screen_height // 2 + self.fade_counter, self.screen_width, self.screen_height // 2))
        if self.direction == 2: pygame.draw.rect(screen, self.colour, (0, 0, self.screen_width, 0 + self.fade_counter))
        if self.fade_counter >= self.screen_width: fade_complete = True

        return fade_complete