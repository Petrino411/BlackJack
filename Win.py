import pygame
from Card import Card
from Player import Player
from Deck import Deck
from Hand import Hand
from Button import Button


class Win:
    def __init__(self):

        pygame.init()
        self.continue_game = False
        self.hide_dealer_card = True
        self.running = True

        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.game_res = 0

        self.bet = 0
        self.objects = []
        self.width_sc, self.height_sc = 1550, 800
        self.chips_im = {}

        self.sc = pygame.display.set_mode((self.width_sc, self.height_sc))
        self.player = Player()

        self.btn = Button(self, 200, 700, 250, 50, "Сделать ставку", self.make_bet)
        self.btn2 = Button(self, 800, 700, 180, 50, "Взять еще", self.player_step)
        self.btn3 = Button(self, 1000, 700, 230, 50, "Воздержаться", self.dealer_step)
        self.btn4 = Button(self, 1300, 700, 200, 50, "Новая игра", self.new_game)



    def play_game(self):
        loading_message = "Загрузка..."
        self.message(loading_message, (255, 255, 255), 36, self.width_sc // 2, self.height_sc // 2, self.sc)
        pygame.display.update()

        self.deck = Deck()
        self.load_chips()
        self.deal_initial_cards()

        print(self.chips_im)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.__create_table()

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

                if player_score == 21:
                    self.game_res = 1
                    self.continue_game = False
                    self.hide_dealer_card = False

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
                self.game_result(self.game_res)
            pygame.display.update()

    def new_game(self):
        if self.game_res != 0:
            self.game_res = 0
            self.bet = 0
            self.hide_dealer_card = True
            self.deck.shuffle_cards()
            self.player_hand = Hand()
            self.dealer_hand = Hand()
            self.deal_initial_cards()
            self.continue_game = True

    def make_bet(self, value):
        print(value)
        try:
            self.bet += self.player.make_bet(value)
        except ValueError:
            self.continue_game = False
        self.continue_game = True


    def game_result(self, n):
        if n == -2:
            self.message("Сделайте ставку", (255, 255, 0), 60, 800, 250, self.sc)
        if n == -1:
            self.message("Перебор!", (255, 255, 45), 60, 800, 620, self.sc)
            self.print_hands(self.hide_dealer_card)
        elif n == 1:
            self.message("Поздравляем! Вы выиграли!", (255, 255, 45), 60, 800, 620, self.sc)
            self.print_hands(self.hide_dealer_card)

        elif n == 2:
            self.message("Вы проиграли", (255, 255, 45), 60, 800, 620, self.sc)
            self.print_hands(self.hide_dealer_card)

        elif n == 3:
            self.player.money += self.bet
            self.message("Ничья.", (255, 255, 45), 60, 800, 620, self.sc)
            self.print_hands(self.hide_dealer_card)
        elif n == 4:
            self.message("У вас закончились деньги. Игра окончена.", (255, 255, 45), 60, 800, 620, self.sc)

    def dealer_step(self):
        if self.continue_game:
            if self.bet > 0:
                if self.player_hand.calculate_score() <= 21:
                    while self.dealer_hand.calculate_score() < 17:
                        self.dealer_hand.add_card(self.deck.deal_card())
                    self.hide_dealer_card = False
                    return False

    def player_step(self):
        if self.continue_game:
            if self.bet > 0:
                self.player_hand.add_card(self.deck.deal_card())
                if self.player_hand.calculate_score() > 21:
                    self.hide_dealer_card = False
                    return False

    def __create_table(self):
        surf = pygame.image.load("images/back.jpg").convert_alpha()
        surf_d = pygame.image.load("images/doska2.jpg").convert_alpha()
        surf_d = pygame.transform.scale(surf_d, (1800, 70))
        pygame.Surface.blit(self.sc, surf, (0, 70))
        pygame.Surface.blit(self.sc, surf_d, (0, 0))

    def load_chips(self):
        chips = [5, 10, 100, 1000, 5000]
        for i in range(len(chips)):
            print(chips[i])
            btn = Button(self, 500 + 75 * i, 500, 70, 70,str(chips[i]), lambda: self.make_bet(int(chips[i])), f"images/chips/{chips[i]}.png")


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
        self.message("Ваша рука:", (255, 255, 0), 30, 300, 100, self.sc)
        i = 0
        x_threshold = 500
        x_offset = 100
        y_offset = 180
        for card in self.player_hand.cards:
            if x_offset + i * 120 >= x_threshold:
                x_offset = 100
                y_offset += 200
                i = 0
            card.display(self.sc, x_offset + i * 120, y_offset)
            i += 1

        self.message(f"Ваш счет: {self.player_hand.calculate_score()}", (255, 255, 0), 30, 550, 100, self.sc)

        self.message("Рука крупье:", (255, 255, 0), 30, 1020, 100, self.sc)
        if hide_dealer_card:
            empty_card = Card("рубашка", 0)
            empty_card.display(self.sc, 880, 180)
            self.dealer_hand.cards[1].display(self.sc, 1000, 180)
        else:
            i = 0
            x_threshold = 1300
            x_offset = 880
            y_offset = 180
            for card in self.dealer_hand.cards:
                if x_offset + i * 120 >= x_threshold:
                    x_offset = 880
                    y_offset += 200
                    i = 0
                card.display(self.sc, x_offset + i * 120, y_offset)
                i += 1
            self.message(f"Счет крупье: {self.dealer_hand.calculate_score()}", (255, 255, 0), 30, 1300, 100, self.sc)
