import tkinter as tk
from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table

class App(tk.Frame):
  def __init__(self, master=None):
    super(App, self).__init__(master)
    self.create_window()
  
  def create_window(self):
    """ Create grid and start/quit buttons. """
    # Add padding to the entire window
    self.master['padx'] = 5
    self.master['pady'] = 5
    
    # Create [0, 0] Count Frame
    self.count_frame = tk.Frame(self, width=200, height=120)
    self.count_frame.grid(row=0, column=0, padx=5, pady=5)
    
    # Create [0, 1] Dealer Frame
    self.dealer_frame = tk.Frame(self, width=200, height=120)
    self.dealer_frame.grid(row=0, column=1, padx=5, pady=5)
    
    # Create [0, 2] Quit Frame
    self.quit_frame = tk.Frame(self, width=200, height=120)
    self.quit_frame.grid(row=0, column=2, padx=5, pady=5, sticky=tk.N + tk.E)
    
    # Create [1, 0] Money Frame
    self.money_frame = tk.Frame(self, width=200, height=120)
    self.money_frame.grid(row=1, column=0, padx=5, pady=5)
    
    # Create [1, 1] Action Frame
    self.action_frame = tk.Frame(self, width=200, height=120)
    self.start_button = tk.Button(self.action_frame, text="Start (S)", command=self.start)
    self.start_button.grid(row=0, column=0)
    self.quit_button = tk.Button(self.action_frame, text="Quit (Q)", command=self.quit)
    self.quit_button.grid(row=1, column=0)
    self.action_frame.grid(row=1, column=1, padx=5, pady=5)
    
    # Create [1, 2] Table Frame
    self.table_frame = tk.Frame(self, width=200, height=120)
    self.table_frame.grid(row=1, column=2, padx=5, pady=5)
    
    # Create a [2, 1] Player Frame
    self.player_frame = tk.Frame(self, width=200, height=120)
    self.player_frame.grid(row=2, column=1, padx=5, pady=5)
  
  def start(self):
    """ Begins game. Initializes Table with 4 decks, Player, and Dealer. """
    # Clear action frame and put quit button in quit_frame
    for widget in self.action_frame.winfo_children():
      widget.destroy()
    
    self.quit_button = tk.Button(self.quit_frame, text="Quit (Q)", command=self.quit)
    self.quit_button.grid(row=0, column=0)
    
    self.table = Table(num_decks=4)
    self.player = Player(self.master)
    self.dealer = Dealer(self.master)
    self.play_round()
  
  def play_round(self):
    """ Handles an entire round between Player and Dealer. """
    self.table.check_shoe_size()
    self.player.ask_bet()
    self.table.deal_cards(self.dealer, self.player)
    if not self.player.hand.natural:
      self.player.play(self.table)
    if not self.player.is_bust():
      self.dealer.play(self.table)
      self._evaluate_round()
    else:
      print("Player lost")
    self._play_again()
  
  def _evaluate_round(self):
    """Evaluates the round given that player has not completely busted.
    Determines winner and resolves outstanding bets. Displays result. """
    self.res = tk.Label()
    self.res.pack()
    # If naturals exist
    if self.dealer.hand.natural and self.player.hand.natural:
      self.res.config(text="Tie, both naturals. Returned $" + str(self.player.bet))
      self.player.money += self.player.bet
    elif self.dealer.hand.natural:
      if self.player.insurance:
        self.res.config(text="Dealer natural. Insurance returned $" + str(self.player.insurance*2))
        self.player.money += self.player.insurance * 3
      else:
        self.res.config(text="Dealer natural. Lost $" + str(self.player.bet))
    elif self.player.hand.natural:
      self.res.config(text="Player natural! Won $" + str(self.player.bet * 1.5))
      self.player.money += self.player.bet + self.player.bet * 1.5
    # If split hands exist
    elif self.player.split_hand:
      if self.dealer.hand.bust:
        res_string = "Dealer bust. \n"
        # Hand 1
        if self.player.hand.bust:
          res_string += "Hand 1 bust. Lost $" + str(self.player.bet) + "\n"
        else:
          res_string += "Hand 1 win! Won $" + str(self.player.bet) + "\n"
          self.player.money += 2 * self.player.bet
        # Hand 2
        if self.player.split_hand.bust:
          res_string += "Hand 2 bust. Lost $" + str(self.player.bet)
        else:
          res_string += "Hand 2 win! Won $" + str(self.player.bet)
          self.player.money += 2 * self.player.split_hand_bet
        self.res.config(text=res_string)
      else: # Dealer not busted
        res_string = ""
        # Hand 1
        if self.player.hand.value > self.dealer.hand.value:
          res_string += "Hand 1 wins! Won $" + str(self.player.bet) + "\n"
          self.player.money += self.player.bet * 2
        elif self.player.hand.value < self.dealer.hand.value:
          res_string += "Hand 1 loss. Lost $" + str(self.player.bet) + "\n"
        else:
          res_string += "Hand 1 tie. Returned $" + str(self.player.bet) + "\n"
          self.player.money += self.player.bet
        # Hand 2
        if self.player.split_hand.value > self.dealer.hand.value:
          res_string += "Hand 2 wins! Won $" + str(self.player.bet)
          self.player.money += self.player.split_hand_bet * 2
        elif self.player.split_hand.value < self.dealer.hand.value:
          res_string += "Hand 2 loss. Lost $" + str(self.player.bet)
        else:
          res_string += "Hand 2 tie. Returned $" + str(self.player.bet)
          player.money += player.split_hand_bet
        self.res.config(text=res_string)
    # Split hand does not exist
    elif self.dealer.hand.bust:
      self.res.config(text="Dealer bust, player win! Won $" + str(self.player.bet))
      self.player.money += self.player.bet * 2
    elif self.player.hand.value > self.dealer.hand.value:
      self.res.config(text="Player win! Won $" + str(self.player.bet))
      self.player.money += 2 * self.player.bet
    elif self.player.hand.value < self.dealer.hand.value:
      self.res.config(text="Dealer win. Lost $" + str(self.player.bet))
    else:
      self.res.config(text="Tie. Returned $" + str(self.player.bet))
      self.player.money += self.player.bet
    
    self.player.reset()
    self.player.update_balance_labels()
    
  def _play_again(self):
    """Asks player if they want to play again."""
    if self.player.money == 0:
      print("Out of money!")
    else:
      print("Call play round or quit.")
      # need to destroy labels if we call play round.
  
  def quit(self): # TODO: if wait_variable, doesn't quit the app
    self.master.destroy()
