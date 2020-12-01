from Hand import Hand
from tkinter import *

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
  def __init__(self, master=None):
    self.master = master
    self.hand = None
    self.split_hand = None
    self.money = 1000
    self.bet = 0
    self.split_hand_bet = 0
    self.insurance = 0
    self.can_double_down = False
    self.can_insurance = False
    self.can_split_pairs = False

  def init_cards(self, hand): # hand is an array of cards
    self.hand = Hand(hand)
    if self.hand.value == 21:
      self.hand.natural = True

#  def print_hand(self):
#    print("Your hand: ")
#    print(self.hand)
  
  def validate_bet(self, val):
    if not val:
        self.bet = 0
        return True
    try:
        self.bet = int(val)
        if self.bet > self.money:
          return False
        return True
    except ValueError:
        return False

  def ask_bet(self):
    self.label_wallet = Label(text="Currently have: $" + str(self.money))
    self.label_wallet.pack()
    self.bet_prompt = Label(text="Place a bet:")
    self.bet_prompt.pack()
    
    vcmd = self.master.register(self.validate_bet)
    self.entry_bet = Entry(self.master, validate="key", validatecommand=(vcmd, '%P'))
    self.entry_bet.pack()
    var = IntVar()
    self.button_enter = Button(text="Enter (E)", command=lambda: var.set(1))
    self.button_enter.pack()
    
    self.button_enter.wait_variable(var)
    
    self.money -= self.bet
    self.label_wallet.config(text="Currently have: $" + str(self.money))
    self.bet_prompt.destroy()
    self.entry_bet.destroy()
    self.button_enter.destroy()
  
  def double_down(self, table):
    self.money -= self.bet
    self.label_wallet.config(text="Currently have: $" + str(self.money))
    self.bet *= 2
    table.deal_one_card(player.hand)
  
  def validate_insurance(self):
    pass

  def ask_insurance(self, table):
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
    self.play_hand(self, table, self.hand)
  
  def split_pairs(self, table):
    c = self.hand.cards
    self.hand = Hand([c[0]])
    self.split_hand = Hand([c[1]])
    self.split_hand_bet = self.bet
    self.money -= self.bet
  
    self.play_hand(table, self.split_hand, hand_num=1)
    self.play_hand(table, self.hand, hand_num=2)

  def play_hand(self, table, hand, hand_num=None): # hand = Hand class, passed in
    if hand_num:
      print("Hand " + str(hand_num) + ":")
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
  
  def reset(self):
    self.hand = None
    self.split_hand = None
    self.bet = 0
    self.split_hand_bet = 0
    self.insurance = 0
    self.can_double_down = False
    self.can_insurance = False
    self.can_split_pairs = False
        
