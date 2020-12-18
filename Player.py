import tkinter as tk
from Hand import Hand

class Player:
  """
  Player class

  Attributes:
    parent: the parent App class
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
  def __init__(self, parent):
    """Initializes Player and creates "Player" label in player_frame."""
    self.parent = parent
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
    """Create "Player" tk.Label in player_frame. Create bets and balances
    tk.Label in status_frame."""
    # Player Frame: "Player" label.
    self.parent.player_frame.grid_columnconfigure((0), weight=1)
    self.parent.player_frame.grid_rowconfigure((0, 1), weight=1)
    
    self.player_label = tk.Label(self.parent.player_frame, text="Player")
    self.player_label.grid(row=1, column=0, sticky="s")
    
    # Status Frame: Rows 2, 3, 4 for Balance, Bet, Insurance
    self.parent.status_frame.grid_columnconfigure((0), weight=1)
    self.parent.status_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
    
    self.label_wallet = tk.Label(self.parent.status_frame, text="Balance: $" + str(self.money))
    self.label_wallet.grid(row=2, column=0)
    
    self.label_bet = tk.Label(self.parent.status_frame)
    self.label_bet.grid(row=3, column=0)
    
    self.label_insurance = tk.Label(self.parent.status_frame)
    self.label_insurance.grid(row=4, column=0)

  def init_cards(self, hand): # hand is an array of cards
    """Receives an initial hand from the Table. Creates tk.Label to display
    cards. Evaluates to see if hand is a natural or if we can split pairs /
    double down."""
    self.label_hand = tk.Label(self.parent.player_frame)
    self.label_hand.grid(row=0, column=0, columnspan=2, sticky="s")
    
    self.hand = Hand(self, hand, self.label_hand)
    
    if self.hand.value == 21:
      self.hand.natural = True
    if (self.hand.value == 9 or self.hand.value == 10 or
        self.hand.value == 11) and self.money >= self.bet:
      self.can_double_down = True
    if self.hand.cards[0][0] == self.hand.cards[1][0]:
      self.can_split_pairs = True
    
    self.hand.update_display()
  
  def update_balance_labels(self):
    """Updates balance, bet (if it exists), and insurance (if it exists)."""
    self.label_wallet.config(text="Balance: $" + str(self.money))
    if self.bet:
      self.label_bet.config(text="Bet: $" + str(self.bet))
    if self.insurance:
      self.label_insurance.config(text="Insurance: $" + str(self.insurance))
  
  def validate_bet(self, val):
    """Validates and sets self.bet."""
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
    """Prompts Player to ask for a bet."""
    self.parent.action_frame.grid_columnconfigure((0, 1), weight=1)
    self.parent.action_frame.grid_rowconfigure((0, 1), weight=1)
    
    self.bet_prompt = tk.Label(self.parent.action_frame, text="Place a bet:")
    self.bet_prompt.grid(row=0, column=0, columnspan=2, pady=5, sticky="s")
    
    vcmd = self.parent.player_frame.register(self.validate_bet)
    
    self.entry_bet = tk.Entry(self.parent.action_frame, validate="key", validatecommand=(vcmd, '%P'))
    self.entry_bet.grid(row=1, column=0, ipadx=2, ipady=2, sticky="n")
    self.entry_bet.focus_set()
    
    var = tk.IntVar()
    
    self.button_enter = tk.Button(self.parent.action_frame, text="Enter (↵)", command=lambda: var.set(1))
    self.button_enter.grid(row=1, column=1, pady=0, ipadx=10, ipady=5, sticky="n")
    i = self.parent.master.bind("<Return>", lambda event: var.set(1))
    self.parent.bindings.append(["<Return>", i])
    
    self.button_enter.wait_variable(var)
    
    self.money -= self.bet
    self.update_balance_labels()
    
    # Clear frame and set weights to 0
    self.parent.clear_frame()
    self.parent.action_frame.grid_columnconfigure((0, 1), weight=0)
    self.parent.action_frame.grid_rowconfigure((0, 1), weight=0)
  
  def double_down(self, table):
    """Double down: Table deals one more card to Player and Player doubles
    bet."""
    self.money -= self.bet
    self.bet *= 2
    self.update_balance_labels()
    table.deal_one_card(self.hand)
    
  def validate_insurance(self, val):
    """Validates and sets self.insurance."""
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
    """Asks Player for insurance bet."""
    self.parent.action_frame.grid_columnconfigure((0, 1), weight=1)
    self.parent.action_frame.grid_rowconfigure((0, 1), weight=1)
    
    self.insurance_prompt = tk.Label(self.parent.action_frame, text="Insurance up to half of\nthe original bet:")
    self.insurance_prompt.grid(row=0, column=0, columnspan=2, pady=5, sticky="s")
    
    vcmd = self.parent.player_frame.register(self.validate_insurance)
    
    self.entry_insurance = tk.Entry(self.parent.action_frame, validate="key", validatecommand=(vcmd, '%P'))
    self.entry_insurance.grid(row=1, column=0, ipadx=2, ipady=2, sticky="n")
    self.entry_insurance.focus_set()
    
    var = tk.IntVar()
    
    self.button_enter = tk.Button(self.parent.action_frame, text="Enter (↵)", command=lambda: var.set(1))
    self.button_enter.grid(row=1, column=1, pady=0, ipadx=10, ipady=5, sticky="n")
    i = self.parent.master.bind("<Return>", lambda event: var.set(1))
    self.parent.bindings.append(["<Return>", i])
    
    self.button_enter.wait_variable(var)
    
    self.money -= self.insurance
    self.update_balance_labels()
    
    self.parent.clear_frame()
    self.parent.action_frame.grid_columnconfigure((0, 1), weight=0)
    self.parent.action_frame.grid_rowconfigure((0, 1), weight=0)

    self.play_hand(table, self.hand)

  def split_pairs(self, table):
    """Splits pairs and plays both hands."""
    # Destroy the previous label for our singular hand.
    self.label_hand.destroy()
    
    # Recreate our hand label and create split hand label.
    self.label_hand = tk.Label(self.parent.player_frame)
    self.label_hand.grid(row=0, column=0, sticky="s")
    
    self.label_split_hand = tk.Label(self.parent.player_frame)
    self.label_split_hand.grid(row=0, column=1, sticky="s")
    
    # Make sure columns are equal weight
    self.parent.player_frame.grid_columnconfigure((0, 1), weight=1)
    
    # Center "Player" label.
    self.player_label.grid(columnspan=2)
    
    c = self.hand.cards
    self.hand = Hand(self, [c[0]], self.label_hand)
    self.split_hand = Hand(self, [c[1]], self.label_split_hand)
    self.split_hand_bet = self.bet
    self.money -= self.bet
    
    # Update text for split hand
    self.split_hand.update_display()
    
    # Update Label for original hand
    self.hand.update_display()
    
    self.play_hand(table, self.hand, self.label_hand)
    self.play_hand(table, self.split_hand, self.label_split_hand)

  def play_hand(self, table, hand, label_curr_hand=None):
    """Takes in Table, Hand, and optional parameter of Label class
    (label for hand being played)."""
    # Set action frame grid weights
    self.parent.action_frame.grid_columnconfigure((0, 1), weight=1)
    self.parent.action_frame.grid_rowconfigure((0), weight=1)
    
    stand = tk.IntVar() # To indicate whether player has stood
    
    def hit():
      """Player hits and receives one card from Table."""
      table.deal_one_card(hand)

      if hand.bust or hand.blackjack:
        stand.set(1)
      
    # If we're in a split hand play
    if label_curr_hand:
      label_curr_hand.config(borderwidth=3, relief="solid")
    
    self.button_hit = tk.Button(self.parent.action_frame, text="Hit (H)", command=hit)
    self.button_hit.grid(row=0, column=0, ipadx=5, ipady=5)
    i = self.parent.master.bind("<h>", lambda event: hit())
    self.parent.bindings.append(["<h>", i])
    
    self.button_stand = tk.Button(self.parent.action_frame, text="Stand (S)", command=lambda: stand.set(1))
    self.button_stand.grid(row=0, column=1, ipadx=5, ipady=5)
    i = self.parent.master.bind("<s>", lambda event: stand.set(1))
    self.parent.bindings.append(["<s>", i])
    
    # Wait for stand to be pressed (or forcefully stand due to 21 or bust)
    self.parent.player_frame.wait_variable(stand)
    
    # Clear frame
    self.parent.clear_frame()
    
    # If we're in a split hand play, remove border
    if label_curr_hand:
      label_curr_hand.config(borderwidth=0)
    
    # Reset action frame grid weights
    self.parent.action_frame.grid_columnconfigure((0, 1), weight=0)
    self.parent.action_frame.grid_rowconfigure((0), weight=0)
  
  def play(self, table):
    """First checks double down / split pairs / insurance if applicable. Plays
    round accordingly."""
    
    action = tk.IntVar() # To indicate whether action has been pressed
    
    def double_down_wrapper(table):
      """Clears buttons, calls double_down, and triggers wait variable."""
      self.parent.clear_frame()
      self.double_down(table)
      action.set(1)
    
    def insurance_wrapper(table):
      """Clears buttons, calls ask_insurance, and triggers wait variable."""
      self.parent.clear_frame()
      self.ask_insurance(table)
      action.set(1)
    
    def split_pairs_wrapper(table):
      """Clears buttons, calls split_pairs, and triggers wait variable."""
      self.parent.clear_frame()
      self.split_pairs(table)
      action.set(1)
    
    def play_hand_wrapper(table, hand):
      """Clears buttons, calls play_hand, and triggers wait variable."""
      self.parent.clear_frame()
      self.play_hand(table, hand)
      action.set(1)
    
    self.parent.action_frame.grid_columnconfigure((0), weight=1)
    self.parent.action_frame.grid_rowconfigure((0, 1, 2, 3), weight=0)
    
    if self.can_double_down or self.can_insurance or self.can_split_pairs:
      if self.can_double_down:
        dd_button = tk.Button(self.parent.action_frame, text="Double Down (D)", command= lambda: double_down_wrapper(table))
        dd_button.grid(row=0, column=0, padx=3, pady=3, ipadx=3, ipady=3)
        i = self.parent.master.bind("<d>", lambda event: double_down_wrapper(table))
        self.parent.bindings.append(["<d>", i])
      if self.can_insurance:
        button_ins = tk.Button(self.parent.action_frame, text="Insurance (I)", command= lambda: insurance_wrapper(table))
        button_ins.grid(row=1, column=0, padx=3, pady=3, ipadx=3, ipady=3)
        i = self.parent.master.bind("<i>", lambda event: insurance_wrapper(table))
        self.parent.bindings.append(["<i>", i])
      if self.can_split_pairs:
        button_sp = tk.Button(self.parent.action_frame, text="Split Pairs (S)", command= lambda: split_pairs_wrapper(table))
        button_sp.grid(row=2, column=0, padx=3, pady=3, ipadx=3, ipady=3)
        i = self.parent.master.bind("<s>", lambda event: split_pairs_wrapper(table))
        self.parent.bindings.append(["<s>", i])
      button_normal = tk.Button(self.parent.action_frame, text="Normal Round (N)", command= lambda: play_hand_wrapper(table, self.hand))
      button_normal.grid(row=3, column=0, padx=3, pady=3, ipadx=3, ipady=3)
      i = self.parent.master.bind("<n>", lambda event: play_hand_wrapper(table, self.hand))
      self.parent.bindings.append(["<n>", i])
      
      # Wait for user to choose
      self.parent.player_frame.wait_variable(action)
    else:
      self.play_hand(table, self.hand)
  
  def is_bust(self):
    """Returns whether Player has totally bust, taking into account split
    hands."""
    if self.split_hand:
      if self.split_hand.bust and self.hand.bust:
        return True
    elif self.hand.bust:
      return True
    return False
  
  def reset(self):
    """Resets Player for the next round."""
    self.hand = None
    self.split_hand = None
    self.bet = 0
    self.split_hand_bet = 0
    self.insurance = 0
    self.can_double_down = False
    self.can_insurance = False
    self.can_split_pairs = False
    
    self.label_hand.destroy()
    
    try:
      if self.label_split_hand:
        self.label_split_hand.destroy()
    except:
      pass
    
    self.label_bet.config(text="")
    self.label_insurance.config(text="")
    
    self.update_balance_labels()
