# Blackjack - Counting Cards

### Calculating Count

Using the Hi-Lo method:
- [2, 3, 4, 5, 6] = +1
- [7, 8, 9] = 0
- [10, J, Q, K, A] = -1

Assigning these values to all cards seen gives us the Running Count.

True Count is Running Count / Decks Remaining. For simplicity, we will always divide by 4, the total number of decks in the shoe.

When the count is high, player advantage increases.

When the count is low, dealer advantage increases.

### Basic Strategy

- When dealer's card is 7, 8, 9, 10-card, or ace, player should draw until 17 or more is reached
- When dealer's card is 4, 5, 6, player should draw until 12 or more is reached
- When dealer's card is 2, 3, player should draw until 13 or more is reached
- If player has an ace (soft hand), player should draw until 18 or more is reached

Summarized from [Bicycle Cards](https://bicyclecards.com/how-to-play/blackjack/).

### Placing Bets

- Place a bet of Betting Unit * (true count - 1)

For instance, if the betting unit is $25 and the true count is 2, we should place a bet of $25 * (2 - 1) = $25. 

Summarized from [Card Counting | WIRED](https://www.youtube.com/watch?v=G_So72lFNIU).
