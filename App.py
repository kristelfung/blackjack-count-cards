import tkinter as tk
import os
from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table

class App(tk.Frame):
  def __init__(self, master=None):
    super(App, self).__init__(master)
    self.create_window()
    self.init_start_buttons()
  
  def create_window(self):
    """Create a 3x3 grid for the game."""
    self.master['padx'] = 5
    self.master['pady'] = 5
    
    # [0, 0] Status Frame (Count and $$)
    self.status_frame = tk.Frame(self, width=250, height=160, bg="orange")
    self.status_frame.grid(row=0, column=0, rowspan=2, sticky="n")
    self.status_frame.grid_propagate(False)
    
    # [0, 1] Dealer Frame
    self.dealer_frame = tk.Frame(self, width=250, height=140, bg="red")
    self.dealer_frame.grid(row=0, column=1)
    self.dealer_frame.grid_propagate(False)
    
    # [0, 2] Quit Frame
    self.quit_frame = tk.Frame(self, width=250, height=140, bg="blue")
    self.quit_frame.grid(row=0, column=2)
    self.quit_frame.grid_propagate(False)
    
    # [1, 1] Action Frame
    self.action_frame = tk.Frame(self, width=250, height=140, bg="grey")
    self.action_frame.grid(row=1, column=1, sticky="nsew")
    self.action_frame.grid_propagate(False)
    
    # [1, 2] Table Frame
    self.table_frame = tk.Frame(self, width=250, height=140, bg="green")
    self.table_frame.grid(row=1, column=2)
    self.table_frame.grid_propagate(False)
    
    # [2, 1] Player Frame
    self.player_frame = tk.Frame(self, width=250, height=140, bg="purple")
    self.player_frame.grid(row=2, column=1)
    self.player_frame.grid_propagate(False)

  def init_start_buttons(self):
    """Initializes Start and Quit button, assigns each weight of 1."""
    self.action_frame.grid_columnconfigure((0, 1), weight=1)
    self.action_frame.grid_rowconfigure((0), weight=1)
    
    self.start_button = tk.Button(self.action_frame, text="Start (S)", command=self.start)
    self.start_button.grid(row=0, column=0, ipadx=10, ipady=10)
    
    self.quit_button = tk.Button(self.action_frame, text="Quit (Q)", command=self.quit)
    self.quit_button.grid(row=0, column=1, ipadx=10, ipady=10)
  
  def start(self):
    """ Begins game. Initializes Table with 4 decks, Player, and Dealer. """
    self.clear_frame(self.action_frame)
    self.action_frame.grid_columnconfigure((0, 1), weight=0)
    self.action_frame.grid_rowconfigure((0), weight=0)
    
    self.quit_frame.grid_columnconfigure((0), weight=1)
    self.quit_frame.grid_rowconfigure((0), weight=1)
    self.quit_button = tk.Button(self.quit_frame, text="Quit (Q)", command=self.quit)
    self.quit_button.grid(row=0, column=0, ipadx=5, ipady=5, sticky="ne")
    
    self.table = Table(4, self.status_frame)
    self.player = Player(self.player_frame, self.status_frame, self.action_frame)
    self.dealer = Dealer(self.dealer_frame, self.action_frame)
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
      self._player_bust_msg()
    self._play_again()
  
  def _evaluate_round(self):
    """Evaluates the round given that player has not completely busted.
    Determines winner and resolves outstanding bets. Displays result. """
    self.res = tk.Label(self.action_frame)
    self.res.grid(row=1, column=0, sticky="n")
    self.action_frame.grid_columnconfigure((0), weight=1)
    self.action_frame.grid_rowconfigure((0, 1), weight=1)
    
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
        if self.player.hand.bust:
          res_string += "Hand 1 bust! Lost $" + str(self.player.bet) + "\n"
        elif self.player.hand.value > self.dealer.hand.value:
          res_string += "Hand 1 wins! Won $" + str(self.player.bet) + "\n"
          self.player.money += self.player.bet * 2
        elif self.player.hand.value < self.dealer.hand.value:
          res_string += "Hand 1 loss. Lost $" + str(self.player.bet) + "\n"
        else:
          res_string += "Hand 1 tie. Returned $" + str(self.player.bet) + "\n"
          self.player.money += self.player.bet
        # Hand 2
        if self.player.split_hand.bust:
          res_string += "Hand 2 bust! Lost $" + str(self.player.bet)
        elif self.player.split_hand.value > self.dealer.hand.value:
          res_string += "Hand 2 wins! Won $" + str(self.player.bet)
          self.player.money += self.player.split_hand_bet * 2
        elif self.player.split_hand.value < self.dealer.hand.value:
          res_string += "Hand 2 loss. Lost $" + str(self.player.bet)
        else:
          res_string += "Hand 2 tie. Returned $" + str(self.player.bet)
          self.player.money += player.split_hand_bet
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
    
    self.player.update_balance_labels()
  
  def _player_bust_msg(self):
    """Displays message saying player busted."""
    self.res = tk.Label(self.action_frame, text="Player busted!")
    self.res.grid(row=0, column=0)
    self.action_frame.grid_columnconfigure((0), weight=1)
    self.action_frame.grid_rowconfigure((0, 1), weight=1)
    
  def _play_again(self):
    """Asks player if they want to play again."""
    self.action_frame.grid_columnconfigure((0), weight=1)
    self.action_frame.grid_rowconfigure((2), weight=1)
    
    click = tk.IntVar()
    
    if self.player.money == 0:
      self.res = tk.Label(self.action_frame, text="Out of money!")
      self.res.grid(row=2, column=0, sticky="n")
    else:
      self.play_button = tk.Button(self.action_frame, text="Play Again (P)", command=lambda: click.set(1))
      self.play_button.grid(row=2, column=0, ipadx=5, ipady=5, sticky="n")
      
      self.master.wait_variable(click)
      
      self.reset_all()
      self.play_round()
  
  def reset_all(self):
    self.clear_frame(self.action_frame)
    
    self.player.reset()
    self.dealer.reset()
    
    self.action_frame.grid_columnconfigure((0), weight=0)
    self.action_frame.grid_rowconfigure((0, 1, 2), weight=0)
    
  def clear_frame(self, frame):
    """Destroys all widgets in a frame."""
    for widget in frame.winfo_children():
      widget.destroy()
  
  def quit(self):
    os._exit(1) # Dirty way to terminate despite wait_variables
