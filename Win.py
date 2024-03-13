import pygame
from Card import Card
from Player import Player
from Deck import Deck
from Hand import Hand
from Button import Button



class Win:
    def __init__(self):

        self.fps = 60
        self.objects = []
        self.width_sc, self.height_sc = 1550, 800

        self.sc = pygame.display.set_mode((self.width_sc, self.height_sc))

        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.continue_game = True

    def main_cycle(self):
        """**********ГЛАВНЫЙ ЦИКЛ ИГРЫ************"""
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.deal_initial_cards()
        pygame.init()

        while self.running:
            self.__event_system()
            self.__create_table()
            self.display_chips()

            if self.continue_game and self.player.money > 0:
                self.message(f"Ваш банк: {self.player.money} $", (0, 255, 0), 28, 300, 20, self.sc)

            btn = Button(self, 1, 300, 500, 50,50, "test")
            if btn.process(self):
                print("ccccccccc")

            self.print_hands()

            pygame.display.flip()
        pygame.display.update()
        pygame.quit()
        quit()

    def __event_system(self):
        for event in pygame.event.get():
            # проверяем закрытие окна
            if event.type == pygame.QUIT:
                self.running = False
            # проверяем нажание пробела и изменяем статус игры
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False


    def __create_table(self):
        surf = pygame.image.load("images/table2.jpg").convert_alpha()
        surf_d = pygame.image.load("images/wood1.jpg").convert_alpha()
        surf_d = pygame.transform.scale(surf_d, (1800, 50))
        pygame.Surface.blit(self.sc, surf, (0, 50))
        pygame.Surface.blit(self.sc, surf_d, (0, 0))

    def display_chips(self):
        chips = [1, 5, 10, 25, 50, 100, 500, 1000, 5000, 10000]
        chips_im = []
        for i in range(len(chips)):
            chips_im.append(
                pygame.transform.scale(pygame.image.load(f"images/chips/{chips[i]}.png").convert_alpha(), (55, 55)))
            pygame.Surface.blit(self.sc, chips_im[i], (500 + 60 * i, 500))

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

        i=0
        for card in self.player_hand.cards:
            card.display(self.sc, 100 + i * 120, 180)
            i+=1

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

            self.deck = Deck()
            self.player_hand = Hand()
            self.dealer_hand = Hand()
            self.deal_initial_cards()

            bet = self.player.make_bet(100)

            if bet > 0:

                self.step = False

                # Игрок делает свой ход
                if self.step:
                    self.print_hands()
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
