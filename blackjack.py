##from Player import Player
##from Table import Table

import random

class Deck:
  def __init__(self):
    self.cards = []
    
    suits = ["♦", "♣", "♥", "♠"]
    for i in range(2, 11):
      for j in range(len(suits)):
        self.cards.append([i, j, str(i) + suits[j]])

    letter_cards = ["J", "Q", "K", "A"]
    for i in range(len(letter_cards)):
      for j in range(len(suits)):
        self.cards.append([letter_cards[i], j, letter_cards[i] + suits[j]])


class Dealer:
  def __init__(self):
    self.value = 0
    self.hand = []

  def calculate_hand(self):
    aces = 0
    face_cards = ["J", "Q", "K"]
    for elem in self.hand:
      if elem[0] in face_cards:
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

  def receive_cards(self, hand):
    self.hand = hand
    self.calculate_hand()

  def print_one_card(self):
    print("Dealer's hand: " + self.hand[0][2] + " [Hidden] ("
          + str(self.value) + ")")
    

class Table:
  def __init__(self, decks):
    self.shoe = []
    self.count = 0
    for deck in decks:
      self.shoe += deck.cards

  def shuffle(self):
    random.shuffle(self.shoe)

  def deal(self, dealer, player):
    dealer.receive_cards([self.shoe.pop(), self.shoe.pop()])
    player.receive_cards([self.shoe.pop(), self.shoe.pop()])

  def deal_one_card(self, person):
    card = self.shoe.pop()
    person.receive_cards(card)

  def calculate_count(dealer, player):
    for card in dealer.hand:
      pass

class Player:
  def __init__(self):
    self.hand = []
    self.value = 0

  def calculate_hand(self):
    aces = 0
    for elem in self.hand:
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

  def print_hand(self):
    msg = "Your hand: "
    for card in self.hand:
      msg += card[2] + " "
    msg += "(" + str(self.value) + ")"
    print(msg)

  def receive_cards(self, hand):
    self.hand = hand
    self.calculate_hand()
    

def main():
  """ Initialize Decks on the Table """
  decks = []
  for i in range(4):
    d = Deck()
    decks.append(d)
  table = Table(decks)
  # table.shuffle()
    
  """ Initialize Player and Dealer """
  player = Player()
  dealer = Dealer()

  """ Start the game """
  playing = True
  while playing:
    # 1. Ask for bet amounts 
    # 2. Deal cards to player and dealer. Calculate hands.
    table.deal(dealer, player)
    # 3. Print hands.
    dealer.print_one_card()
    player.print_hand()
    playing = False
    # 4. Print count.
    #player.print_count()
    # 5. Ask player if they want to hit or stand.
##    val = input("Hit (H) or Stand (S)?")
##    while val != "H" or val != "S":
##      val = input("Please enter \"H\" for Hit and \"S\" for Stand!")
##    while val


if __name__ == "__main__":
   main()
