import tkinter as tk
from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table

class App(tk.Frame):
  def __init__(self, master=None):
    super(App, self).__init__(master)
    self.initGame()
  
  def initGame(self):
    """ Create Start and Quit button. """
    self.start_button = tk.Button(self, text="Start (S)", command=self.start)
    self.start_button.pack()
    self.quit_button = tk.Button(self, text="Quit (Q)", command=self.quit)
    self.quit_button.pack()
  
  def start(self):
    """ Begins game. Initializes Table with 4 decks, Player, and Dealer. """
    self.start_button.destroy()
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
