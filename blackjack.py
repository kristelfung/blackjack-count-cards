from tkinter import *

from App import App
from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table

def evaluate_round(dealer, player):
  """
    <Purpose>
      Evaluates the round given that player has not completely busted.
      Determines winner and resolves outstanding bets.

    <Arguments>
      dealer: instance of Dealer class
      player: instance of Player class

    <Effect>
      Adds/removes money from Player accordingly.
  """
  # Deal with naturals
  if dealer.hand.natural and player.hand.natural:
    print("Tie, both naturals. Returned $" + str(player.bet))
    player.money += player.bet
  elif dealer.hand.natural:
    if player.insurance:
      print("Dealer natural. Insurance returned $" + str(player.insurance*2))
      player.money += player.insurance * 2 + player.insurance
    else:
      print("Dealer natural. Lost $" + str(player.bet))
  elif player.hand.natural:
    print("Player natural! Won $" + str(player.bet * 1.5))
    player.money += player.bet + player.bet * 1.5
  # If a split hand exists
  elif player.split_hand:
    if dealer.hand.bust:
      print("Dealer bust.")
      # Hand 1
      if player.hand.bust:
        print("Hand 1 bust. Lost $" + str(player.bet))
      else:
        print("Hand 1 win! Won $" + str(player.bet))
        player.money += 2 * player.bet
      # Hand 2
      if player.split_hand.bust:
        print("Hand 2 bust. Lost $" + str(player.bet))
      else:
        print("Hand 2 win! Won $" + str(player.bet))
        player.money += 2 * player.split_hand_bet
    else: # Dealer not busted
      # Hand 1
      if player.hand.value > dealer.hand.value:
        print("Hand 1 wins! Won $" + str(player.bet))
        player.money += player.bet * 2
      elif player.hand.value < dealer.hand.value:
        print("Hand 1 loss. Lost $" + str(player.bet))
      else:
        print("Hand 1 tie. Returned $" + str(player.bet))
        player.money += player.bet
      # Hand 2
      if player.split_hand.value > dealer.hand.value:
        print("Hand 2 wins! Won $" + str(player.bet))
        player.money += player.split_hand_bet * 2
      elif player.split_hand.value < dealer.hand.value:
        print("Hand 2 loss. Lost $" + str(player.bet))
      else:
        print("Hand 2 tie. Returned $" + str(player.bet))
        player.money += player.split_hand_bet
  # Split hand does not exist
  elif dealer.hand.bust:
    print("Dealer bust, player win! Won $" + str(player.bet))
    player.money += player.bet * 2
  elif player.hand.value > dealer.hand.value:
    print("Player win! Won $" + str(player.bet))
    player.money += 2 * player.bet
  elif player.hand.value < dealer.hand.value:
    print("Dealer win. Lost $" + str(player.bet))
  else: 
    print("Tie. Returned $" + str(player.bet))
    player.money += player.bet

def play_again(dealer, player):
  """
    <Purpose>
      Asks player if they want to play again.

    <Arguments>
      dealer: instance of Dealer class
      player: instance of Player class

    <Effect>
      Continues or halts game.
      Resets Player and Dealer.
  """
  if player.money == 0:
    print("Out of money!")
    return False
  play_again = input("Another round? (Y/N) \n")
  play_again = play_again.lower()
  while play_again != "y" and play_again != "n":
    play_again = input("Please enter \"Y\" to play again or \"N\" to quit. \n")
    play_again = play_again.lower()
  if play_again == "y":
    player.reset()
    dealer.reset()
    print("")
    return True
  elif play_again == "n":
    return False

def main():
  root = Tk()
  app = App(root)
  app.pack()
  app.mainloop()
  
  '''
  # Initialize Table with 4 Decks
  table = Table(num_decks=4)
    
  # Initialize Player and Dealer
  player = Player()
  dealer = Dealer()
  
  # Start the game
  playing = True
  while playing:
    # 1. Ask for bet amounts and print count
    table.check_shoe_size() √
    table.print_count() √
    player.ask_bet() √
    # 2. Deal hands + print hands + print count
    deal_cards(table, dealer, player)
    # 3. Player move
    player_turn(table, player)
    # 4. Evaluate player
    if not player_bust(player):
      # 5a. Dealer's move & evaluate round
      dealer_turn(table, dealer, player)
      evaluate_round(dealer, player)
    else:
      # 5b. Player busted
      print("Bust! Lost $" + str(player.bet))
    # 6. Ask to play again.
    playing = play_again(dealer, player)
  '''

if __name__ == "__main__":
   main()
