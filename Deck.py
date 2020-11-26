class Deck:
  """
  Deck class

  Attributes:
    cards: list of cards in the form [['A', 1, 'A♠'], ['A', 2, 'A♥'], ...]
  """
  
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
