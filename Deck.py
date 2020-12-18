class Deck:
  """
  Deck class

  Attributes:
    cards: list of cards in the form [['A', 'AS'], ['A', 'AH'], ...]
  """
  
  def __init__(self):
    self.cards = [] 
    
    suits = ["D", "C", "H", "S"] # Diamond, Club, Heart, Spade
    for i in range(2, 11):
      for j in range(len(suits)):
        self.cards.append([i, str(i) + suits[j]])

    letter_cards = ["J", "Q", "K", "A"]
    for i in range(len(letter_cards)):
      for j in range(len(suits)):
        self.cards.append([letter_cards[i], letter_cards[i] + suits[j]])
