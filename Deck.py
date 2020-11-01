class Deck:
  def __init__(self):
    self.cards = [] # [['A', 2, 'A♥'], ...] 
    
    suits = ["♦", "♣", "♥", "♠"]
    for i in range(2, 11):
      for j in range(len(suits)):
        self.cards.append([i, j, str(i) + suits[j]])

    letter_cards = ["J", "Q", "K", "A"]
    for i in range(len(letter_cards)):
      for j in range(len(suits)):
        self.cards.append([letter_cards[i], j, letter_cards[i] + suits[j]])
