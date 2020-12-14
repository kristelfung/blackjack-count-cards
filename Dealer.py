import tkinter as tk
from Hand import Hand

class Dealer:
  """
  Dealer class

  Attributes:
    dealer_frame: tk.Frame for dealer's cards
    hand: Hand class representing dealer's hand
  """
  def __init__(self, dealer_frame, action_frame):
    """Initializes Dealer and creates "Dealer" label in player_frame."""
    self.dealer_frame = dealer_frame
    self.action_frame = action_frame
    self.hand = None
    
    dealer_label = tk.Label(self.dealer_frame, text="Dealer")
    dealer_label.grid(row=0, column=0, sticky=tk.N)

  def init_cards(self, hand, player):
    """ Receives an initial hand frmo the table. Evaluates to see if Dealer
    has natural, and if Player can buy insurance."""
    self.hand = Hand(hand)
    
    if self.hand.value == 21:
      self.hand.natural = True
    if self.hand.cards[0][0] == "A":
      player.can_insurance = True
    
    self.label_cards = tk.Label(self.dealer_frame, text=self.hand.cards[0][2] + "[Hidden]")
    self.label_cards.grid(row=1, column=0)

  def play(self, table):
    self.label_dealer_hits = tk.Label(self.action_frame)
    self.label_dealer_hits.grid(row=0, column=0, sticky="s")
    self.label_cards.config(text=self.hand)
    table.update_count([self.hand.cards[1]]) # Card overturned
    hits = 0
    while self.hand.value < 17:
      table.deal_one_card(self.hand)
      self.label_cards.config(text=self.hand)
      hits += 1
    self.label_dealer_hits.config(text="Dealer hits " + str(hits) + " times.")

  def reset(self):
    self.hand = None
