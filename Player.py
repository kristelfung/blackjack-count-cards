from tkinter import *
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
    """ Receives an initial hand from the table. Evaluates to see if hand is
    a natural or if we can split pairs / double down. """
    self.hand = Hand(hand)
    
    if self.hand.value == 21:
      self.hand.natural = True
    if (self.hand.value == 9 or self.hand.value == 10 or
        self.hand.value == 11):
      self.can_double_down = True
    if self.hand.cards[0][0] == self.hand.cards[1][0]:
      self.can_split_pairs = True
    
    self.label_hand = Label(text=self.hand)
    self.label_hand.pack()

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
    table.deal_one_card(self.hand)
    
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
    
    # Create Label for split hand
    self.label_split_hand = Label(text=self.split_hand)
    self.label_split_hand.pack()
    
    # Update Label for original hand
    self.label_hand.config(text=self.hand)
    
    self.play_hand(table, self.split_hand, self.label_hand)
    self.play_hand(table, self.hand, self.label_split_hand)

  def play_hand(self, table, hand, label_curr_hand=None): # NEED TO WAIT.
    """ Takes in Table, Hand, and optional parameter of Label class
    (label for hand being played) """
    
    stand = IntVar() # To indicate whether player has stood
    
    def hit():
      table.deal_one_card(hand)
      table.calculate_count([hand.cards[len(hand.cards)-1]])
      # Update our hand's label of cards AND the table's count
      label_curr_hand.config(text=hand)
      table.label_rc.config(text="Running Count is " + str(table.count))
      table.label_tc.config(text="True Count is " + str(table.count / 4))
      
      if hand.bust or hand.blackjack:
        stand.set(1)
      
    if not label_curr_hand:
      label_curr_hand = self.label_hand
    # TODO: highlight label (indicate it's the hand's turn)
    
    self.button_hit = Button(self.master, text="Hit (H)", command=hit)
    self.button_hit.pack()
    self.button_stand = Button(self.master, text="Stand (S)", command=lambda: stand.set(1))
    self.button_stand.pack()
    
    # Wait for stand to be pressed (or forcefully stand due to 21 or bust)
    self.master.wait_variable(stand)
    
    self.button_hit.destroy()
    self.button_stand.destroy()
  
  def play(self, table):
    """ First checks double down / split pairs / insurance if applicable. Plays
    round accordingly. """
    
    action = IntVar() # To indicate whether action has been pressed
    
    def double_down_wrapper(buttons, table):
      for btn in buttons:
        btn.destroy()
      self.double_down(table)
      action.set(1)
    
    def insurance_wrapper(buttons, table):
      for btn in buttons:
        btn.destroy()
      self.ask_insurance(table)
      action.set(1)
    
    def split_pairs_wrapper(buttons, table):
      for btn in buttons:
        btn.destroy()
      self.split_pairs(table)
      action.set(1)
    
    def play_hand_wrapper(buttons, table, hand):
      for btn in buttons:
        btn.destroy()
      self.play_hand(table, hand)
      action.set(1)
    
    if self.can_double_down or self.can_insurance or self.can_split_pairs:
      buttons = []
      if self.can_double_down:
        dd_button = Button(self.master, text="Double Down (D)", command= lambda: double_down_wrapper(buttons, table))
        buttons.append(dd_button)
        dd_button.pack()
      if self.can_insurance:
        button_ins = Button(self.master, text="Insurance (I)", command= lambda: insurance_wrapper(buttons, table))
        buttons.append(button_ins)
        button_ins.pack()
      if self.can_split_pairs:
        button_sp = Button(self.master, text="Split Pairs (S)", command= lambda: split_pairs_wrapper(buttons, table))
        buttons.append(button_sp)
        button_sp.pack()
      button_normal = Button(self.master, text="Normal Round (N)", command= lambda: play_hand_wrapper(buttons, table, self.hand))
      buttons.append(button_normal)
      button_normal.pack()
      
      # Wait for user to choose
      self.master.wait_variable(action)
    else:
      self.play_hand(table, self.hand)
  
  def is_bust(self):
    if self.split_hand:
      if self.split_hand.bust and self.hand.bust:
        return True
    elif self.hand.bust:
      return True
    return False
  
  def reset(self):
    self.hand = None
    self.split_hand = None
    self.bet = 0
    self.split_hand_bet = 0
    self.insurance = 0
    self.can_double_down = False
    self.can_insurance = False
    self.can_split_pairs = False
        
