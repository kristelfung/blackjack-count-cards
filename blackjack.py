from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table
import random

def deal_cards(table, dealer, player):
  table.deal(dealer, player)
  dealer.print_one_card()
  player.print_hand()
  if player.hand.value == 21:
    player.hand.natural = True
  if dealer.hand.value == 21:
    dealer.hand.natural = True
  if player.hand.value == 9 or player.hand.value == 10 or player.hand.value == 11:
    player.can_double_down = True
  if player.hand.cards[0][0] == player.hand.cards[1][0]:
    player.can_split_pairs = True
  if dealer.hand.cards[0][0] == "A":
    player.can_insurance = True
  table.calculate_count(player.hand.cards)
  table.calculate_count([dealer.hand.cards[0]])
  table.print_count()

def player_turn(table, player):
  if not player.hand.natural:
    # ASK: Double Down / Insurance / Split pairs
    dd = None
    ins = None
    sp = None
    if player.can_double_down:
      dd = input("Total of " + str(player.hand.value) + ". Double down? (Y/N) \n")
      dd = dd.lower()
      while dd != "y" and dd != "n":
        dd = input("Please enter \"Y\" to double down or \"N\" to play as is. \n")
        dd = dd.lower()
    if player.can_insurance and (dd == "n" or dd == None):
      ins = input("Dealer showing an Ace. Buy insurance? (Y/N) \n")
      ins = ins.lower()
      while ins != "y" and ins != "n":
        ins = input("Please enter \"Y\" to buy insurance or \"N\" to play as is. \n")
        ins = ins.lower()
    if player.can_split_pairs and (dd == "n" or dd == None):
      sp = input("You have two of the same kind. Split pairs? (Y/N) \n")
      sp = sp.lower()
      while sp != "y" and sp != "n":
        sp = input("Please enter \"Y\" to split pairs or \"N\" to play as is. \n")
        sp = sp.lower()
    
    # HANDLE: Double Down / Insurance / Split pairs
    if dd == "y":
      print("Bet additional " + str(player.bet))
      player.money -= player.bet
      player.bet *= 2
      table.deal_one_card(player.hand)
      player.print_hand()
      return
    if ins == "y":
      player.ask_insurance()
    elif sp == "y":
      player.split_pairs()
      player.play_hand(table, player.split_hand, split=1)
      player.play_hand(table, player.hand, split=2)
      return
    
    # Regular Round
    player.play_hand(table, player.hand)

def player_bust(player): # -> returns bool of whether dealer should continue or not
  if player.split_hand:
    if player.split_hand.bust and player.hand.bust:
      return True
  elif player.hand.bust:
    return True
  return False

def dealer_turn(table, dealer, player):
  dealer.play(table)
  table.calculate_count(dealer.hand.cards[1:])
  #table.print_count()

def evaluate_round(dealer, player):
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
  elif dealer.hand.bust:
    print("Dealer bust, player win! Won $" + str(player.bet))
    player.money += player.bet * 2
  elif player.split_hand:
    # hand 1
    if player.hand.value > dealer.hand.value:
      print("Hand 1 wins! Won $" + str(player.bet))
      player.money += player.bet * 2
    elif player.hand.value < dealer.hand.value:
      print("Hand 1 loss. Lost $" + str(player.bet))
    else:
      print("Hand 1 tie. Returned $" + str(player.bet))
      player.money += player.bet
    # hand 2
    if player.split_hand.value > dealer.hand.value:
      print("Hand 2 wins! Won $" + str(player.bet))
      player.money += player.bet * 2
    elif player.split_hand.value < dealer.hand.value:
      print("Hand 2 loss. Lost $" + str(player.bet))
    else:
      print("Hand 2 tie. Returned $" + str(player.bet))
      player.money += player.bet
  elif player.hand.value > dealer.hand.value:
    print("Player win! Won $" + str(player.bet))
    player.money += 2 * player.bet
  elif player.hand.value < dealer.hand.value:
    print("Dealer win. Lost $" + str(player.bet))
  else:
    print("Tie. Returned $" + str(player.bet))
    player.money += player.bet

def play_again(dealer, player, playing):
  if player.money == 0:
    print("Out of money!")
    playing = False
  play_again = input("Another round? (Y/N) \n")
  play_again = play_again.lower()
  while play_again != "y" and play_again != "n":
    play_again = input("Please enter \"Y\" to play again or \"N\" to quit. \n")
    play_again = play_again.lower()
  if play_again == "y":
    player.reset()
    dealer.reset()
    print("")
  elif play_again == "n":
    playing = False

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
    # 1. Ask for bet amounts and print count
    table.print_count()
    player.ask_bet()
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
    play_again(dealer, player, playing)

if __name__ == "__main__":
   main()
