from Hand import Hand

class Dealer:
  def __init__(self):
    self.hand = None

  def init_cards(self, hand):
    self.hand = Hand(hand)

  def print_one_card(self):
    print("Dealer's hand: ")
    self.hand.print_one()

  def print_hand(self):
    print("Dealer's hand: ")
    print(self.hand)

  def play(self, table):
    self.print_hand()
    while self.hand.value < 17:
      print("Dealer hits.")
      table.deal_one_card(self.hand)
      self.print_hand()

  def reset(self):
    self.hand = None
