import pygame
from Card import Card
from Player import Player
from Deck import Deck
from Hand import Hand
from Button import Button

from icecream import ic


class Win:
    def __init__(self):

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
        print(self.chips_im)

    def main_cycle(self):
        """**********ГЛАВНЫЙ ЦИКЛ ИГРЫ************"""
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.deal_initial_cards()
        pygame.init()

        continue_game = False

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

            player_score = 0
            dealer_score = 0

            self.message(f"Ваш банк: {self.player.money} $", (0, 255, 0), 28, 300, 20, self.sc)

            btn = Button(self, 1, 300, 700, 150, 50, "ставка")
            btn.process(self)

            btn2 = Button(self, 1, 800, 700, 150, 50, "карта")
            btn2.process(self)

            btn3 = Button(self, 1, 1000, 700, 150, 50, "пропустить")
            btn3.process(self)

            game_res = 0

            if btn.process(self):
                self.bet += self.player.make_bet(100)
                continue_game = True


            if continue_game:
                if self.player.money == 0:
                    game_res = 4
                    continue_game = False

                self.print_hands(self.hide_dealer_card)

                if self.bet > 0:
                    if btn2.process(self):
                        self.player_step()

                    if self.player_hand.calculate_score() <= 21 and btn3.process(self):
                        self.dealer_step()

                player_score = self.player_hand.calculate_score()
                dealer_score = self.dealer_hand.calculate_score()

                if not self.hide_dealer_card:
                    ic(player_score, dealer_score)

                    if player_score > 21:
                        # self.message("Перебор", (255, 0, 45), 58, 1000, 400, self.sc)
                        game_res = -1
                        continue_game = False

                    elif dealer_score > 21 or player_score > dealer_score:
                        # self.message("Поздравляем! Вы выиграли!", (255, 0, 45), 58, 1000, 400, self.sc)
                        # if not game_over:
                        #
                        #     game_over = True
                        self.player.money += self.bet * 2
                        game_res = 1
                        continue_game = False

                    elif player_score < dealer_score:
                        # self.message("Вы проиграли =(", (255, 0, 45), 58, 1000, 400, self.sc)
                        game_res = 2
                        continue_game = False

                    else:
                        # if not game_over:
                        #     self.player.money += self.bet
                        #     game_over = True
                        # self.message("Ничья.", (255, 0, 45), 58, 1000, 400, self.sc)
                        self.player.money += self.bet
                        game_res = 3
                        continue_game = False

            else:
                self.message("Сделайте ставку", (255, 0, 45), 58, 800, 650, self.sc)
                self.over(game_res)

            pygame.display.flip()

        pygame.display.update()
        pygame.quit()
        quit()

    def over(self, n):
        print("over", n)
        self.print_hands(self.hide_dealer_card)
        if n == -1:
            self.message("Перебор", (255, 0, 45), 58, 800, 650, self.sc)
        elif n == 1:
            self.message("Поздравляем! Вы выиграли!", (255, 0, 45), 58, 800, 650, self.sc)

        elif n == 2:
            self.message("Вы проиграли", (255, 0, 45), 58, 800, 650, self.sc)

        elif n == 3:
            self.player.money += self.bet
            self.message("Ничья.", (255, 0, 45), 58, 800, 650, self.sc)
        elif n == 4:
            self.message("У вас закончились деньги. Игра окончена.", (255, 0, 45), 58, 800, 650, self.sc)

    def dealer_step(self):
        while self.dealer_hand.calculate_score() < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
        self.hide_dealer_card = False
        return False

    def player_step(self):
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

    def play_game(self):
        if self.continue_game and self.player.money > 0:
            print("\nУ вас", self.player.money, "долларов в банке.")

            self.deck.shuffle_cards()
            self.player_hand = Hand()
            self.dealer_hand = Hand()
            self.deal_initial_cards()

            bet = self.player.make_bet(100)

            if bet > 0:

                self.step = False

                # Игрок делает свой ход
                if self.step:
                    choice = False
                    # choice = input("\nХотите взять еще карту? (да/нет): ").lower()
                    if choice:
                        self.player_hand.add_card(self.deck.deal_card())
                        if self.player_hand.calculate_score() > 21:
                            self.print_hands()
                            print("У вас перебор! Вы проиграли.")
                            self.step = False
                    else:
                        self.step = False

                if self.player_hand.calculate_score() <= 21:
                    while self.dealer_hand.calculate_score() < 17:
                        self.dealer_hand.add_card(self.deck.deal_card())
                    self.print_hands(hide_dealer_card=False)

                    player_score = self.player_hand.calculate_score()
                    dealer_score = self.dealer_hand.calculate_score()

                    if dealer_score > 21 or player_score > dealer_score:
                        print("Поздравляем! Вы выиграли.")
                        self.message("Поздравляем! Вы выиграли!", (255, 0, 45), 58, 1000, 400, self.sc)
                        self.player.money += 2 * bet
                    elif player_score < dealer_score:
                        print("Вы проиграли.")
                        self.message("Вы проиграли =(", (255, 0, 45), 58, 1000, 400, self.sc)
                    else:
                        print("Ничья.")
                        self.player.money += bet
                        self.message("Ничья.", (255, 0, 45), 58, 1000, 400, self.sc)

                if self.player.money == 0:
                    print("У вас закончились деньги. Игра окончена.")
                    self.message("У вас закончились деньги. Игра окончена.", (255, 0, 45), 58, 1000, 400, self.sc)

                self.continue_game = True
