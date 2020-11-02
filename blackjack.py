from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table
import random

def evaluate_round(dealer, player):
  if dealer.is_bust():
    print("Dealer bust, player WIN!")
  elif player.value > dealer.value:
    print("Player win.")
  elif player.value < dealer.value:
    print("Dealer win.")
  else:
    print("Tie.")

def main():
  """ Initialize Decks on the Table """
  decks = []
  for i in range(4):
    d = Deck()
    decks.append(d)
  table = Table(decks)
  random.shuffle(table.shoe)
    
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
    player_bust = False
    player_turn = True
    while player_turn:
      val = input("Hit (H) or Stand (S)? \n")
      val = val.lower()
      while val != "h" and val != "s":
        val = input("Please enter \"H\" for Hit and \"S\" for Stand! \n")
        val = val.lower()
      if val == "h":
        table.deal_one_card(player)
        player.print_hand()
        table.calculate_count([player.hand[len(player.hand)-1]])
        table.print_count()
        if player.is_bust():
          player_bust = True
          player_turn = False
        elif player.is_blackjack():
          player_turn = False
      elif val == "s":
        player_turn = False

    # 6. Dealer's move.
    if not player_bust:
      dealer.play(table)
      table.calculate_count(dealer.hand[1:])
      table.print_count()
      evaluate_round(dealer, player)
    else: # the player loses their bet.
      print("Bust! Lose bet of ___")
    
    play_again = input("Another round? (Y/N) \n")
    play_again = play_again.lower()
    while play_again != "y" and play_again != "n":
      play_again = input("Please enter \"Y\" to play again or \"N\" to quit.")
      play_again = play_again.lower()
    if play_again == "y":
      player.hand = []
      dealer.hand = []
      print("\n")
    elif play_again == "n":
      playing = False


if __name__ == "__main__":
   main()
