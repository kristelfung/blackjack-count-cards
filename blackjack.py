from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table
import random

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
    # 4. Print count.
    table.calculate_count(player.hand)
    table.calculate_count([dealer.hand[0]])
    table.print_count()
    # 5. Ask player if they want to hit or stand.
    turn = True
    while turn:
      val = input("Hit (H) or Stand (S)? \n")
      val = val.lower()
      while val != "h" and val != "s":
        val = input("Please enter \"H\" for Hit and \"S\" for Stand! \n")
        print(val)
      if val == "h":
        table.deal_one_card(player)
        player.calculate_hand()
        player.print_hand()
      elif val == "s":
        turn = False
    print("dealer does stuff now")
    playing = False


if __name__ == "__main__":
   main()
