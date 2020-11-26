from Hand import Hand

class Player:
  """
  Player class

  Attributes:
    hand: Hand class representing player's hand
    split_hand: Hand class if player decides to split
    money: int representing how much money player has remaining
    bet: int representing bet amount for the round
    insurance: int representing insurance amount (always 1/2 of bet)
    can_double_down: boolean if player can double down, set right after hand
        dealt
    can_insurance: boolean if player can insurance, set right after hand dealt
    can_split_pairs: boolean if player can split pairs, set right after hand
        dealt
  """
  def __init__(self):
    self.hand = None
    self.split_hand = None
    self.money = 1000
    self.bet = 0
    self.insurance = 0
    self.can_double_down = False
    self.can_insurance = False
    self.can_split_pairs = False

  def init_cards(self, hand): # hand is an array of cards
    self.hand = Hand(hand)
    if self.hand.value == 21:
      self.hand.natural = True

  def print_hand(self):
    print("Your hand: ")
    print(self.hand)

  def ask_bet(self):
    print("Currently have: $" + str(self.money))
    valid_bet = False
    bet = None
    while not valid_bet:
      bet = input("Place a bet: ")
      try:
        bet = float(bet)
        while bet > self.money:
          bet = input("Not enough money, place a smaller bet: ")
          bet = float(bet)
        valid_bet = True
      except:
        print("Please enter a valid number.")
    self.money = self.money - bet
    self.bet = bet

  def ask_insurance(self):
    valid_ins = False
    ins = None
    while not valid_ins:
      ins = input("Buy insurance up to half the original bet: ")
      try:
        ins = float(ins)
        while ins > self.bet / 2:
          ins = input("Can only place up to half the original: ")
          ins = float(ins)
        valid_ins = True
      except:
        print("Please enter a valid number.")
    self.money -= ins
    self.insurance = ins

  def play_hand(self, table, hand, split=None): # hand = Hand class, passed in
    if split:
      print("Hand " + str(split) + ":")
      print(hand)
    while True:
      val = input("Hit (H) or Stand (S)? \n")
      val = val.lower()
      while val != "h" and val != "s":
        val = input("Please enter \"H\" for Hit and \"S\" for Stand! \n")
        val = val.lower()
      if val == "h":
        table.deal_one_card(hand)
        print(hand)
        table.calculate_count([hand.cards[len(hand.cards)-1]])
        #table.print_count()
        if hand.bust:
          return
        elif hand.blackjack:
          return
      elif val == "s":
        return

  def split_pairs(self):
    c = self.hand.cards
    self.hand = Hand([c[0]])
    self.split_hand = Hand([c[1]])
  
  def reset(self):
    self.hand = None
    self.split_hand = None
    self.bet = 0
    self.insurance = 0
    self.can_double_down = False
    self.can_insurance = False
    self.can_split_pairs = False
        
