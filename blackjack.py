from Dealer import Dealer
from Player import Player
from Deck import Deck
from Table import Table

def deal_cards(table, dealer, player):
  """
  <Purpose>
    Deals cards to dealer and player.

  <Arguments>
    table: instance of Table class
    dealer: instance of Dealer class
    player: instance of Player class

  <Effect>
    Deals cards to dealer and player.
    Prints hands.
    Checks for naturals / double down / split pairs.
    Prints the count of the table.
  """
  
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
  """
  <Purpose>
    Analyse player's turn.

  <Arguments>
    table: instance of Table class
    player: instance of Player class

  <Effect>
    Checks for natural, double down, insurance, split pairs.
    Call player methods (e.g. insurance, play hand) based on input.
  """
  
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
    if (player.can_split_pairs and (dd == "n" or dd == None) and
        (ins == "n" or ins == None)):
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
    elif ins == "y":
      player.ask_insurance()
    elif sp == "y":
      player.split_pairs()
      player.play_hand(table, player.split_hand, hand_num=1)
      player.play_hand(table, player.hand, hand_num=2)
      return
    
    # Regular Round
    player.play_hand(table, player.hand)

def player_bust(player):
  """
    <Purpose>
      Checks if all player hand(s) busted.
      
    <Arguments>
      player: instance of Player class
    
    <Effect>
      Checks the bust attribute of each Hand
    
    <Returns>
      Boolean True if player busts, False if did not bust.
  """
  
  if player.split_hand:
    if player.split_hand.bust and player.hand.bust:
      return True
  elif player.hand.bust:
    return True
  return False

def dealer_turn(table, dealer, player):
  """
    <Purpose>
      Calls the dealer's turn.

    <Arguments>
      table: instance of Table class
      dealer: instance of Dealer class
      player: instance of Player class

    <Effect>
      Calls play method for Dealer
  """
  
  dealer.play(table)
  table.calculate_count(dealer.hand.cards[1:])

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
  # Initialize Table with 4 Decks
  table = Table(num_decks=4)
    
  # Initialize Player and Dealer
  player = Player()
  dealer = Dealer()

  # Start the game
  playing = True
  while playing:
    # 1. Ask for bet amounts and print count
    table.check_shoe_size()
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
    playing = play_again(dealer, player)

if __name__ == "__main__":
   main()
