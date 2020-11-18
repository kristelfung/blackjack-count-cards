class Table:
  def __init__(self, decks):
    self.shoe = []
    self.count = 0
    for deck in decks:
      self.shoe += deck.cards

  def shuffle(self):
    random.shuffle(self.shoe)

  def deal(self, dealer, player):
    dealer.init_cards([self.shoe.pop(), self.shoe.pop()])
    player.init_cards([self.shoe.pop(), self.shoe.pop()])

  def deal_one_card(self, hand):
    card_hand = [self.shoe.pop()]
    hand.receive_cards(card_hand)

  def calculate_count(self, cards):
    low = [2, 3, 4, 5, 6] # +1
    high = [10, "J", "Q", "K", "A"] # -1
    for card in cards:
      if card[0] in low:
        self.count += 1
      elif card[0] in high:
        self.count -= 1

  def print_count(self):
    print("▸ Running Count is " + str(self.count))
    print("▸ True Count is " + str(self.count / 4))
