import pygame


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # Gets mouse position
        pos = pygame.mouse.get_pos()

        # Checks mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

class SwitchButton():
    off_button: Button
    on_button: Button
    cooldown: int
    max_cooldown: int
    toggled: bool
    ready: bool
    pressed: bool

    def __init__(self, x, y, off_img, on_img, scale, default = False):
        self.off_button = Button(x, y, off_img, scale)
        self.on_button = Button(x, y, on_img, scale)
        self.toggled = default
        self.pressed = False
        self.ready = False
        self.cooldown = 0
        self.max_cooldown = 20
    
    def draw(self, screen):

        if not pygame.mouse.get_pressed()[0]: self.ready = True

        if self.toggled:
            if self.on_button.draw(screen) and self.ready:
                self.toggled = False
                self.ready = False
                return True
        else:
            if self.off_button.draw(screen) and self.ready:
                self.toggled = True
                self.ready = False
                return True
        return False