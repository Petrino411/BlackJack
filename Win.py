import pygame
from Card import Card
from Player import Player
from Deck import Deck
from Hand import Hand
from Button import Button

from icecream import ic


class Win:
    def __init__(self):
        pygame.init()
        self.continue_game = False

        self.dealer_hand = None
        self.player_hand = None
        self.game_res = None
        self.hide_dealer_card = None
        self.bet = 0
        self.fps = 60
        self.objects = []
        self.width_sc, self.height_sc = 1550, 800

        self.sc = pygame.display.set_mode((self.width_sc, self.height_sc))

        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()

        self.chips_im = {}
        self.load_chips()
        self.deck = Deck()

        self.btn = Button(self, 300, 700, 150, 50, "ставка", self.make_bet)

        self.btn2 = Button(self, 800, 700, 150, 50, "карта", self.player_step)

        self.btn3 = Button(self, 1000, 700, 150, 50, "пропустить",  self.dealer_step)

        self.btn4 = Button(self, 1200, 700, 150, 50, "новая игра", self.restart)

    def main_cycle(self):
        """**********ГЛАВНЫЙ ЦИКЛ ИГРЫ************"""

        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.deal_initial_cards()


        self.continue_game = False

        self.hide_dealer_card = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.__create_table()
            self.display_chips()

            for object in self.objects:
                object.process()

            self.message(f"Ваш банк: {self.player.money} $", (0, 255, 0), 28, 300, 20, self.sc)

            if self.bet == 0:
                self.game_res = -2
                self.continue_game = False

            if self.continue_game:
                self.game_res = 0
                if self.player.money < 0:
                    self.game_res = 4
                    self.continue_game = False

                self.print_hands(self.hide_dealer_card)

                player_score = self.player_hand.calculate_score()
                dealer_score = self.dealer_hand.calculate_score()

                if not self.hide_dealer_card:

                    if player_score > 21:
                        self.game_res = -1
                        self.continue_game = False

                    elif dealer_score > 21 or player_score > dealer_score:
                        self.player.money += self.bet * 2
                        self.game_res = 1
                        self.continue_game = False

                    elif player_score < dealer_score:
                        self.game_res = 2
                        self.continue_game = False

                    else:
                        self.player.money += self.bet
                        self.game_res = 3
                        self.continue_game = False


            else:
                self.over(self.game_res)

            pygame.display.flip()

    def restart(self):
        if self.game_res != 0:
            self.game_res = 0
            self.bet = 0
            self.hide_dealer_card = True
            self.deck.shuffle_cards()
            self.player_hand = Hand()
            self.dealer_hand = Hand()
            self.deal_initial_cards()
            self.continue_game = True

    def make_bet(self):
        self.bet += self.player.make_bet(100)
        self.continue_game = True

    def over(self, n):
        if n == -2:
            self.message("Сделайте ставку", (255, 0, 45), 58, 800, 650, self.sc)
        if n == -1:
            self.message("Перебор", (255, 0, 45), 58, 800, 650, self.sc)
            self.print_hands(self.hide_dealer_card)
        elif n == 1:
            self.message("Поздравляем! Вы выиграли!", (255, 0, 45), 58, 800, 650, self.sc)
            self.print_hands(self.hide_dealer_card)

        elif n == 2:
            self.message("Вы проиграли", (255, 0, 45), 58, 800, 650, self.sc)
            self.print_hands(self.hide_dealer_card)

        elif n == 3:
            self.player.money += self.bet
            self.message("Ничья.", (255, 0, 45), 58, 800, 650, self.sc)
            self.print_hands(self.hide_dealer_card)
        elif n == 4:
            self.message("У вас закончились деньги. Игра окончена.", (255, 0, 45), 58, 800, 650, self.sc)

    def dealer_step(self):
        if self.bet > 0:
            if self.player_hand.calculate_score() <= 21:
                while self.dealer_hand.calculate_score() < 17:
                    self.dealer_hand.add_card(self.deck.deal_card())
                self.hide_dealer_card = False
                return False


    def player_step(self):
        if self.bet > 0:
            self.player_hand.add_card(self.deck.deal_card())
            if self.player_hand.calculate_score() > 21:
                self.hide_dealer_card = False
                return False

    def __create_table(self):
        surf = pygame.image.load("images/table2.jpg").convert_alpha()
        surf_d = pygame.image.load("images/wood1.jpg").convert_alpha()
        surf_d = pygame.transform.scale(surf_d, (1800, 50))
        pygame.Surface.blit(self.sc, surf, (0, 50))
        pygame.Surface.blit(self.sc, surf_d, (0, 0))

    def load_chips(self):
        chips = [1, 5, 10, 25, 50, 100, 500, 1000, 5000, 10000]
        for i in range(len(chips)):
            self.chips_im[chips[i]] = pygame.transform.scale(
                pygame.image.load(f"images/chips/{chips[i]}.png").convert_alpha(), (55, 55))

    def display_chips(self):
        if self.chips_im is not {}:
            i = 0
            for key, value in self.chips_im.items():
                pygame.Surface.blit(self.sc, value, (500 + 60 * i, 500))
                i += 1

    def message(self, msg, color, size, x, y, sc):
        """Функция будет показывать сообщение в окне"""
        font_style = pygame.font.SysFont('arial', size)
        text = font_style.render(msg, True, color)  # оформление
        text_rect = text.get_rect(center=(x, y))
        sc.blit(text, text_rect)

    def deal_initial_cards(self):
        self.player_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())

        self.dealer_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())

    def print_hands(self, hide_dealer_card=True):
        self.message("Ваша рука:", (255, 255, 0), 28, 300, 100, self.sc)

        i = 0
        for card in self.player_hand.cards:
            card.display(self.sc, 100 + i * 120, 180)
            i += 1

        self.message(f"Ваш счет: {self.player_hand.calculate_score()}", (255, 255, 0), 28, 300, 400, self.sc)

        self.message("Рука крупье:", (255, 255, 0), 28, 1000, 100, self.sc)
        if hide_dealer_card:
            empty_card = Card("рубашка", 0)
            empty_card.display(self.sc, 880, 180)

            self.dealer_hand.cards[1].display(self.sc, 1000, 180)
        else:
            i = 0
            for card in self.dealer_hand.cards:
                card.display(self.sc, 880 + i * 120, 180)
                i += 1
            self.message(f"Счет крупье: {self.dealer_hand.calculate_score()}", (255, 255, 0), 28, 1000, 400, self.sc)


def test():
    print("asdfgasdgasfdg")
