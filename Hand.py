class Hand:
  def __init__(self, hand):
    self.cards = hand
    self.value = None
    self.bust = False
    self.blackjack = False
    self.natural = False
    self.calculate_hand()

  def __repr__(self):
    msg = ""
    for card in self.cards:
      msg += card[2] + " "
    msg += "(" + str(self.value) + ")"
    return msg

  def print_one(self):
    face_cards = ["J", "Q", "K"]
    val = self.cards[0][0]
    if self.cards[0][0] in face_cards:
      val = 10
    elif self.cards[0][0] == "A":
      val = 11
    print(self.cards[0][2] + " [Hidden] ("
          + str(val) + ")")

  def calculate_hand(self):
    self.value = 0
    aces = 0
    for elem in self.cards:
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

    if self.value > 21:
      self.bust = True

    if self.value == 21:
      self.blackjack = True

  def receive_cards(self, cards):
    self.cards += cards
    self.calculate_hand()
