import tkinter as tk
from Hand import Hand

class Player:
  """
  Player class

  Attributes:
    player_frame: tk.Frame for player's cards
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
  def __init__(self, player_frame, status_frame, action_frame):
    """Initializes Player and creates "Player" label in player_frame."""
    self.player_frame = player_frame
    self.status_frame = status_frame
    self.action_frame = action_frame
    self.hand = None
    self.split_hand = None
    self.money = 1000
    self.bet = 0
    self.split_hand_bet = 0
    self.insurance = 0
    self.can_double_down = False
    self.can_insurance = False
    self.can_split_pairs = False
    
    self.create_frame()
  
  def create_frame(self):
    """Initialize Player Frame for cards, and Status Frame for bets and balances."""
    player_label = tk.Label(self.player_frame, text="Player")
    player_label.grid(row=2, column=0)
    
    # Status Frame: Rows 2, 3, 4 for Balance, Bet, Insurance
    self.status_frame.grid_columnconfigure((0), weight=1)
    self.status_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
    
    self.label_wallet = tk.Label(self.status_frame, text="Balance: $" + str(self.money))
    self.label_wallet.grid(row=2, column=0)
    
    self.label_bet = tk.Label(self.status_frame)
    self.label_bet.grid(row=3, column=0)
    
    self.label_insurance = tk.Label(self.status_frame)
    self.label_insurance.grid(row=4, column=0)

  def init_cards(self, hand): # hand is an array of cards
    """ Receives an initial hand from the Table. Evaluates to see if hand is
    a natural or if we can split pairs / double down. """
    self.hand = Hand(hand)
    
    if self.hand.value == 21:
      self.hand.natural = True
    if (self.hand.value == 9 or self.hand.value == 10 or
        self.hand.value == 11):
      self.can_double_down = True
    if self.hand.cards[0][0] == self.hand.cards[1][0]:
      self.can_split_pairs = True
    
    self.label_hand = tk.Label(self.player_frame, text=self.hand)
    self.label_hand.grid(row=1, column=0)
  
  def update_balance_labels(self):
    """ Updates balance, bet (if it exists), and insurance (if it exists). """
    self.label_wallet.config(text="Balance: $" + str(self.money))
    if self.bet:
      self.label_bet.config(text="Bet: $" + str(self.bet))
    if self.insurance:
      self.label_insurance.config(text="Insurance: $" + str(self.insurance))
  
  def validate_bet(self, val):
    """ Validates and sets self.bet """
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
    """ Prompts Player to ask for a bet. """
    self.action_frame.grid_columnconfigure((0, 1), weight=1)
    self.action_frame.grid_rowconfigure((0, 1), weight=1)
    
    self.bet_prompt = tk.Label(self.action_frame, text="Place a bet:")
    self.bet_prompt.grid(row=0, column=0, columnspan=2, pady=5, sticky="s")
    vcmd = self.player_frame.register(self.validate_bet)
    self.entry_bet = tk.Entry(self.action_frame, validate="key", validatecommand=(vcmd, '%P'))
    self.entry_bet.grid(row=1, column=0, ipadx=2, ipady=2, sticky="n")
    var = tk.IntVar()
    self.button_enter = tk.Button(self.action_frame, text="Enter (↵)", command=lambda: var.set(1))
    self.button_enter.grid(row=1, column=1, pady=0, ipadx=5, ipady=5, sticky="n")
    
    self.button_enter.wait_variable(var)
    
    self.money -= self.bet
    self.update_balance_labels()
    
    # Clear frame and set weights to 0
    self.clear_frame(self.action_frame)
    self.action_frame.grid_columnconfigure((0, 1), weight=0)
    self.action_frame.grid_rowconfigure((0, 1), weight=0)
  
  def double_down(self, table):
    """ Double down: Table deals one more card to Player and Player doubles
    bet. """
    self.money -= self.bet
    self.bet *= 2
    self.update_balance_labels()
    table.deal_one_card(self.hand)
    self.label_hand.config(text=self.hand)
    
  def validate_insurance(self, val):
    """ Validates and sets self.insurance """
    if not val:
      self.insurance = 0
      return True
    try:
      self.insurance = int(val)
      if self.insurance > self.bet / 2:
        return False
      return True
    except ValueError:
      return False

  def ask_insurance(self, table):
    """ Asks Player for insurance bet. """
    self.action_frame.grid_columnconfigure((0, 1), weight=1)
    self.action_frame.grid_rowconfigure((0, 1), weight=1)
    
    self.insurance_prompt = tk.Label(self.action_frame, text="Insurance up to half of\nthe original bet:")
    self.insurance_prompt.grid(row=0, column=0, columnspan=2, pady=5, sticky="s")
    
    vcmd = self.player_frame.register(self.validate_insurance)
    self.entry_insurance = tk.Entry(self.action_frame, validate="key", validatecommand=(vcmd, '%P'))
    self.entry_insurance.grid(row=1, column=0, ipadx=2, ipady=2, sticky="n")
    var = tk.IntVar()
    self.button_enter = tk.Button(self.action_frame, text="Enter (↵)", command=lambda: var.set(1))
    self.button_enter.grid(row=1, column=1, pady=0, ipadx=5, ipady=5, sticky="n")
    
    self.button_enter.wait_variable(var)
    
    self.money -= self.insurance
    self.update_balance_labels()
    
    self.clear_frame(self.action_frame)
    self.action_frame.grid_columnconfigure((0, 1), weight=0)
    self.action_frame.grid_rowconfigure((0, 1), weight=0)

    self.play_hand(table, self.hand)

  def split_pairs(self, table):
    """ Splits pairs and plays both hands. """
    c = self.hand.cards
    self.hand = Hand([c[0]])
    self.split_hand = Hand([c[1]])
    self.split_hand_bet = self.bet
    self.money -= self.bet
    
    # Create Label for split hand
    self.label_split_hand = tk.Label(self.player_frame, text=self.split_hand)
    self.label_split_hand.grid(row=0, column=0)
    
    # Update Label for original hand
    self.label_hand.config(text=self.hand)
    
    self.play_hand(table, self.split_hand, self.label_hand)
    self.play_hand(table, self.hand, self.label_split_hand)

  def play_hand(self, table, hand, label_curr_hand=None):
    """ Takes in Table, Hand, and optional parameter of Label class
    (label for hand being played) """
    self.action_frame.grid_columnconfigure((0, 1), weight=1)
    self.action_frame.grid_rowconfigure((0), weight=1)
    
    stand = tk.IntVar() # To indicate whether player has stood
    
    def hit():
      """ Player hits and receives one card from Table """
      table.deal_one_card(hand)
      # Update our hand's label of cards AND the table's count
      label_curr_hand.config(text=hand)

      if hand.bust or hand.blackjack:
        stand.set(1)
      
    if not label_curr_hand:
      label_curr_hand = self.label_hand
    # TODO: highlight label (indicate it's the hand's turn)
    
    self.button_hit = tk.Button(self.action_frame, text="Hit (H)", command=hit)
    self.button_hit.grid(row=0, column=0, ipadx=5, ipady=5)
    self.button_stand = tk.Button(self.action_frame, text="Stand (S)", command=lambda: stand.set(1))
    self.button_stand.grid(row=0, column=1, ipadx=5, ipady=5)
    
    # Wait for stand to be pressed (or forcefully stand due to 21 or bust)
    self.player_frame.wait_variable(stand)
    
    self.clear_frame(self.action_frame)
    self.action_frame.grid_columnconfigure((0, 1), weight=0)
    self.action_frame.grid_rowconfigure((0), weight=0)
  
  def play(self, table):
    """ First checks double down / split pairs / insurance if applicable. Plays
    round accordingly. """
    
    action = tk.IntVar() # To indicate whether action has been pressed
    
    def double_down_wrapper(table):
      """ Calls double_down, clears buttons and triggers wait variable. """
      self.clear_frame(self.action_frame)
      self.double_down(table)
      action.set(1)
    
    def insurance_wrapper(table):
      """ Calls ask_insurance, clears buttons and triggers wait variable. """
      self.clear_frame(self.action_frame)
      self.ask_insurance(table)
      action.set(1)
    
    def split_pairs_wrapper(table):
      """ Calls split_pairs, clears buttons and triggers wait variable. """
      self.clear_frame(self.action_frame)
      self.split_pairs(table)
      action.set(1)
    
    def play_hand_wrapper(table, hand):
      """ Calls play_hand, clears buttons and triggers wait variable. """
      self.clear_frame(self.action_frame)
      self.play_hand(table, hand)
      action.set(1)
    
    self.action_frame.grid_columnconfigure((0), weight=1)
    self.action_frame.grid_rowconfigure((0, 1, 2, 3), weight=0)
    
    if self.can_double_down or self.can_insurance or self.can_split_pairs:
      if self.can_double_down:
        dd_button = tk.Button(self.action_frame, text="Double Down (D)", command= lambda: double_down_wrapper(table))
        dd_button.grid(row=0, column=0, padx=3, pady=3, ipadx=3, ipady=3)
      if self.can_insurance:
        button_ins = tk.Button(self.action_frame, text="Insurance (I)", command= lambda: insurance_wrapper(table))
        button_ins.grid(row=1, column=0, padx=3, pady=3, ipadx=3, ipady=3)
      if self.can_split_pairs:
        button_sp = tk.Button(self.action_frame, text="Split Pairs (S)", command= lambda: split_pairs_wrapper(table))
        button_sp.grid(row=2, column=0, padx=3, pady=3, ipadx=3, ipady=3)
      button_normal = tk.Button(self.action_frame, text="Normal Round (N)", command= lambda: play_hand_wrapper(table, self.hand))
      button_normal.grid(row=3, column=0, padx=3, pady=3, ipadx=3, ipady=3)
      
      # Wait for user to choose
      self.player_frame.wait_variable(action)
    else:
      self.play_hand(table, self.hand)
  
  def is_bust(self):
    """ Returns whether Player has bust, taking into account split hands. """
    if self.split_hand:
      if self.split_hand.bust and self.hand.bust:
        return True
    elif self.hand.bust:
      return True
    return False
  
  def reset(self):
    """ Resets Player for the next round. """
    self.hand = None
    self.split_hand = None
    self.bet = 0
    self.split_hand_bet = 0
    self.insurance = 0
    self.can_double_down = False
    self.can_insurance = False
    self.can_split_pairs = False
  
  def clear_frame(self, frame):
    """Destroys all widgets in a frame."""
    for widget in frame.winfo_children():
      widget.destroy()
        
