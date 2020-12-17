import tkinter as tk
from PIL import ImageTk, Image

class Hand:
  """
  Hand class

  Attributes:
    parent: the parent Player or Dealer class
    cards: a list of cards in the form [['A', 3, 'AS'], ['A', 2, 'AH'], ...]
    value: int representing the value of the hand
    bust: boolean indicating whether hand is bust or not
    blackjack: boolean indicating whether hand is blackjack or not
    natural: boolean indicating whether hand is a natural or not
  """
  def __init__(self, parent, hand):
    """Initializes a Hand and calculates the value."""
    self.parent = parent
    self.cards = hand
    self.value = None
    self.bust = False
    self.blackjack = False
    self.natural = False
    
    self.calculate_hand()
    self.create_window()
  
  def create_window(self):
    """Creates label for hand's value."""
    self.label_count = tk.Label(self.parent.label_hand)
  
  def display_one_card(self):
    """Displays first card face up, second card face down (needed for
    Dealer)."""
    filename = "images/" + self.cards[0][2] + ".jpg"
    image = Image.open(filename)
    image.thumbnail((70, 105), Image.ANTIALIAS)
    image.save(filename, quality=95)
    img = ImageTk.PhotoImage(image)
    label_card = tk.Label(self.parent.label_hand, image=img)
    label_card.photo = img
    label_card.grid(row=0, column=0)
    
    filename = "images/back.jpg"
    image = Image.open(filename)
    image.thumbnail((70, 105), Image.ANTIALIAS)
    image.save(filename, quality=95)
    img = ImageTk.PhotoImage(image)
    label_card = tk.Label(self.parent.label_hand, image=img)
    label_card.photo = img
    label_card.grid(row=0, column=1)
    
    self.label_count.config(text="(" + str(self.card_value(self.cards[0])) + ")")
    self.label_count.grid(row=1, column=0, columnspan=len(self.cards))

  def update_display(self):
    """Calculates value of hand. Displays cards and hand value."""
    for i in range(len(self.cards)):
      filename = "images/" + self.cards[i][2] + ".jpg"
      image = Image.open(filename)
      image.thumbnail((70, 105), Image.ANTIALIAS)
      image.save(filename, quality=95)
      img = ImageTk.PhotoImage(image)
      label_card = tk.Label(self.parent.label_hand, image=img)
      label_card.photo = img
      label_card.grid(row=0, column=i)
  
    self.label_count.config(text="(" + str(self.value) + ")")
    self.label_count.grid(row=1, column=0, columnspan=len(self.cards))

  def calculate_hand(self):
    """Calculates value of all cards in hand."""
    self.value = 0
    aces = 0
    for elem in self.cards:
      if elem[0] == "J" or elem[0] == "Q" or elem[0] == "K":
        self.value += 10
      elif elem[0] == "A":
        aces += 1
      else:
        self.value += elem[0]

    if aces > 0:
      if self.value <= 10 and aces == 1:
        self.value += 11
      elif self.value <= 9 and aces == 2:
        self.value += 12
      elif self.value <= 8 and aces == 3:
        self.value += 13
      elif self.value <= 7 and aces == 4:
        self.value += 14
      else:
        self.value += aces

    if self.value > 21:
      self.bust = True

    if self.value == 21:
      self.blackjack = True
  
  def card_value(self, card):
    """Calculates and returns value of a singular card (needed for Dealer)."""
    card = card[0]
    if card == "A":
      return 11
    elif card == "J" or card == "Q" or card == "K":
      return 10
    return int(card)

  def receive_cards(self, cards):
    """Receives a list of cards to add to hand. Called by Table's
    deal_one_card()."""
    self.cards += cards
    self.calculate_hand()
    self.update_display()
