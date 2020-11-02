from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table
import random

def deal_cards(table, dealer, player):
  table.deal(dealer, player)
  dealer.print_one_card()
  player.print_hand()
  if player.value == 21:
    player.natural = True
  if dealer.value == 21:
    dealer.natural = True
  table.calculate_count(player.hand)
  table.calculate_count([dealer.hand[0]])
  table.print_count()

def player_turn(table, player):
  player.bust = False
  turn = True
  while turn:
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
        player.bust = True
        turn = False
      elif player.is_blackjack():
        turn = False
    elif val == "s":
      turn = False

def dealer_turn(table, dealer, player):
  if not player.bust:
    dealer.play(table)
    table.calculate_count(dealer.hand[1:])
    table.print_count()
    evaluate_round(dealer, player)
  else: # the player loses their bet.
    print("Bust! Lost $" + str(player.bet))

def evaluate_round(dealer, player):
  if dealer.natural and player.natural:
    print("Tie, both naturals.")
    player.money += player.bet
  elif dealer.natural:
    print("Dealer natural. Lost $" + str(player.bet))
  elif player.natural:
    print("Player natural! Won $" + str(player.bet * 1.5))
    player.money += player.bet + player.bet * 1.5
  elif dealer.is_bust():
    print("Dealer bust, player win! Won $" + str(player.bet))
    player.money += 2 * player.bet
  elif player.value > dealer.value:
    print("Player win! Won $" + player.bet)
    player.money += 2 * player.bet
  elif player.value < dealer.value:
    print("Dealer win. Lost $" + player.bet)
  else:
    print("Tie. Returned $" + str(player.bet))
    player.money += player.bet

def main():
  """ Initialize Decks on the Table """
  decks = []
  for i in range(6):
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
    player.ask_bet()
    # 2. Deal hands + print hands + print count
    deal_cards(table, dealer, player)
    # 3. Player move
    player_turn(table, player)
    # 4. Dealer's move.
    dealer_turn(table, dealer, player)
    # 5. Ask to play again.
    play_again = input("Another round? (Y/N) \n")
    play_again = play_again.lower()
    while play_again != "y" and play_again != "n":
      play_again = input("Please enter \"Y\" to play again or \"N\" to quit.")
      play_again = play_again.lower()
    if play_again == "y":
      player.hand = []
      dealer.hand = []
      print("")
    elif play_again == "n":
      playing = False

if __name__ == "__main__":
   main()
