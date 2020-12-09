from tkinter import *

from App import App
from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table

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
