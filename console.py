import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} из {self.suit}"

    def __repr__(self):
        return f"{self.value} из {self.suit}"


class Deck:
    def __init__(self):
        suits = ['Черви', 'Бубны', 'Трефы', 'Пики']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']
        self.cards = [Card(suit, value) for suit in suits for value in values]
        random.shuffle(self.cards)

    def deal_card(self):
        print(len(self.cards))
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_score(self):
        total = sum(
            11 if card.value == 'Туз' else 10 if card.value in ['Валет', 'Дама', 'Король'] else int(card.value) for card
            in self.cards)
        num_aces = sum(1 for card in self.cards if card.value == 'Туз')
        while total > 21 and num_aces:
            total -= 10
            num_aces -= 1
        return total


class Player:
    def __init__(self, money=5000):
        self.money = money

    def make_bet(self):
        while True:
            try:
                bet = int(input(f"Сделайте ставку (не больше {self.money}): "))
                self.money -= bet
                if bet > self.money:
                    print("У вас недостаточно денег.")
                else:
                    return bet
            except ValueError:
                print("Пожалуйста, введите целое число.")


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.player = Player()
        self.continue_game = True

    def deal_initial_cards(self):
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())

    def print_hands(self, hide_dealer_card=True):
        print("\nВаша рука:")
        for card in self.player_hand.cards:
            print(card)
        print("Ваш счет:", self.player_hand.calculate_score())

        print("\nРука крупье:")
        if hide_dealer_card:
            print("Скрытая карта")
            print(*self.dealer_hand.cards[1:])
        else:
            for card in self.dealer_hand.cards:
                print(card)
            print("Счет крупье:", self.dealer_hand.calculate_score())

    def play_game(self):
        while self.continue_game and self.player.money > 0:
            print("\nУ вас", self.player.money, "долларов в банке.")

            # Создаем колоду карт и раздаем карты игроку и крупье
            self.deck = Deck()
            self.player_hand = Hand()
            self.dealer_hand = Hand()
            self.deal_initial_cards()

            # Ставка игрока
            bet = self.player.make_bet()

            # Игрок делает свой ход
            while True:
                self.print_hands()
                choice = input("\nХотите взять еще карту? (да/нет): ").lower()
                if choice == 'да':
                    self.player_hand.add_card(self.deck.deal_card())
                    if self.player_hand.calculate_score() > 21:
                        self.print_hands()
                        print("У вас перебор! Вы проиграли.")
                        break
                else:
                    break

            if self.player_hand.calculate_score() <= 21:
                while self.dealer_hand.calculate_score() < 17:
                    self.dealer_hand.add_card(self.deck.deal_card())
                self.print_hands(hide_dealer_card=False)

                player_score = self.player_hand.calculate_score()
                dealer_score = self.dealer_hand.calculate_score()

                if dealer_score > 21 or player_score > dealer_score:
                    print("Поздравляем! Вы выиграли.")
                    self.player.money += 2 * bet
                elif player_score < dealer_score:
                    print("Вы проиграли.")
                else:
                    print("Ничья.")
                    self.player.money += bet

            if self.player.money == 0:
                print("У вас закончились деньги. Игра окончена.")

            self.continue_game = input("Хотите сыграть еще раз? (да/нет): ").lower() == 'да'


# Запуск игры
game = BlackjackGame()
game.play_game()
