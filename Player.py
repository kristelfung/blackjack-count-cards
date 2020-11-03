class Player:
  def __init__(self):
    self.hand = []
    self.money = 1000
    self.bet = 0
    self.value = None
    self.bust = False
    self.natural = False
    self.double_down = False

  def calculate_hand(self):
    self.value = 0
    aces = 0
    for elem in self.hand:
      if elem[0] == "J" or elem[0] == "Q" or elem[0] == "K":
        self.value += 10
      elif elem[0] == "A":
        aces += 1
      else:
        self.value += elem[0]

    if aces > 0:
      if self.value <= 10 and aces == 1:
        self.value += 11
      elif self.value <= 9 and aces == 2:
        self.value += 12
      elif self.value <= 8 and aces == 3:
        self.value += 13
      elif self.value <= 7 and aces == 4:
        self.value += 14
      else:
        self.value += aces

  def is_bust(self):
    return self.value > 21

  def is_blackjack(self):
    return self.value == 21

  def print_hand(self):
    msg = "Your hand: "
    for card in self.hand:
      msg += card[2] + " "
    msg += "(" + str(self.value) + ")"
    print(msg)

  def ask_bet(self):
    print("Currently have: $" + str(self.money))
    valid_bet = False
    while not valid_bet:
      bet = input("Place a bet: ")
      try:
        bet = float(bet)
        valid_bet = True
      except:
        print("Please enter a valid number.")
    bet = float(bet)
    while bet > self.money:
      bet = input("Not enough money, place a smaller bet: ")
    self.money = self.money - bet
    self.bet = bet

  def receive_cards(self, hand): # hand is an array of cards
    self.hand += hand
    self.calculate_hand()
