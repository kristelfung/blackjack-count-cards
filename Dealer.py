class Dealer:
  def __init__(self):
    self.value = 0
    self.hand = []

  def calculate_hand(self):
    self.value = 0
    aces = 0
    face_cards = ["J", "Q", "K"]
    for elem in self.hand:
      if elem[0] in face_cards:
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

  def receive_cards(self, hand):
    self.hand = hand
    self.calculate_hand()

  def print_one_card(self):
    print("Dealer's hand: " + self.hand[0][2] + " [Hidden] ("
          + str(self.value) + ")")
