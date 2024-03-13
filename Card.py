import pygame


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.im_card = pygame.image.load(f"images/cards/{self.value}_{self.suit}.png").convert_alpha()
        self.im_card = pygame.transform.scale(self.im_card, (self.im_card.get_width() // 12, self.im_card.get_height() // 12))

    def __str__(self):
        return f"{self.value} из {self.suit}"

    def __repr__(self):
        return f"{self.value} из {self.suit}"

    def display(self, sc, x, y):
        pygame.Surface.blit(sc, self.im_card, (x, y))
