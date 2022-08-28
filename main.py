from itertools import product
from random import shuffle
from collections import Counter


flower = {'♠': 3,
          '♥': 2,
          '♣': 1,
          '♦': 0}
value = {'A': 3,
         'K': 2,
         'Q': 1,
         'J': 0}

class Card:
    def __init__(self, v, f, joker=False):
        self.v = v
        self.f = f
        self.joker = joker
        # joker has a value of 100 (basically if it comes down to highest v card joker always wins)
        self.score = value[v] * 4 + flower[f] if not joker else 100

    def __repr__(self):
        return str(self.v) + str(self.f) if not self.joker else str('Joker')

# find the value of a hand
def handValue(hand) -> tuple:
    combos = [
        (9, 'five-of-a-kind'),
        (8, 'straight-flush'),  # (same flower but flush)
        (7, 'four-of-a-kind'),
        (6, 'full-house'),  # (fu lo)
        (5, 'flush'),  # (fa)
        (4, 'straight'),
        (3, 'three-of-a-kind'),
        (2, 'two-pair'),
        (1, 'one-pair')]

    # check if joker is in hand, if it does remove it from 'hand'
    # also find the highest value card
    maxv = 0
    havejoker = False
    for i, card in enumerate(hand):
        maxv = max(maxv, card.score)
        if str(card) == 'Joker':
            havejoker = True
            hand = hand.copy()
            hand.pop(i)

    # count the number of value and flowers in a hand, sort by value
    cardv = Counter([card.v for card in hand])
    cardv = dict(sorted(cardv.items(), key=lambda item: (item[1], value[item[0]])))
    cardf = Counter([card.f for card in hand])

    isflush = True if len(cardf) == 1 else False
    isstraight = True if (len(cardv) == 4 and havejoker) or len(cardv) == 5 else False
    isfiveofakind = True if (len(cardv) == 1) and havejoker else False
    isfourofakind = True if (list(cardv.values())[-1] == 3 and havejoker) or list(cardv.values())[-1] == 4 else False
    isthreeofakind = True if (list(cardv.values())[-1] == 2 and havejoker) or list(cardv.values())[-1] == 3 else False
    isfullhouse = True if (isthreeofakind and len(cardv) == 2) else False
    istwopair = True if (list(cardv.values())[-1] == 2 and list(cardv.values())[-2] == 2 and not havejoker) else False

    if isfiveofakind:
        combo_number = 0
    elif isflush and isstraight:
        combo_number = 1
    elif isfourofakind:
        combo_number = 2
    elif isfullhouse:
        combo_number = 3
    elif isflush:
        combo_number = 4
    elif isstraight:
        combo_number = 5
    elif isthreeofakind:
        combo_number = 6
    elif istwopair:
        combo_number = 7
    else:
        combo_number = 8




    return (combos[combo_number][0] + (value[list(cardv.keys())[-1]] * 0.1), combos[combo_number][1]), maxv


def createDeck() -> list:
    deck = []
    for v, f in product(value, flower):
        deck.append(Card(v, f))

    deck.append(Card('K', '♠', joker=True))
    return deck

def compareHands(hand1, hand2) -> int:

    # combo is a tuple (combo value, combo name), maxv is int of highest card value
    hand1v = handValue(hand1)
    hand2v = handValue(hand2)

    # print(f'hand1: {hand1} \t - {hand1v[0][1]} \nhand2: {hand2} \t - {hand2v[0][1]}')
    if hand1v[0][0] > hand2v[0][0]:
        # print('hand1 wins')
        return 0
    elif hand1v[0][0] < hand2v[0][0]:
        # print('hand2 wins')
        return 1
    else:
        if hand1v[1] > hand2v[1]:
            # print('same combo, hand 1 has highest value card and wins')
            return 0
        else:
            # print('same combo, hand 2 has highest value card and wins')
            return 1

# s for simulate, one game where two players have a hand
def s_OneGame():

    # create a random deck consist of 17 cards
    deck = createDeck()

    # shuffle the deck
    shuffle(deck)

    # pop a random hand for the player from the top of the deck
    hand1 = [deck.pop(0) for _ in range(5)]
    hand2 = [deck.pop(0) for _ in range(5)]

    compareHands(hand1, hand2)

# the probability of getting each type of combo in a hand in the first round
def s_ProbOneHand():

    result = []
    iterations = 1_000_000

    for _ in range(iterations):
        deck = createDeck()
        shuffle(deck)
        hand = [deck.pop(0) for _ in range(5)]

        result.append(handValue(hand)[0])

    result = dict(Counter(result))
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    for k, v in result.items():
        print(f'{k} \t\t {v/iterations*100:.2f}%')

# when playing with another player, the chance of winning by combo type
def s_TwoHandWinChanceByType():
    result = []
    iterations = 1_000_000

    for _ in range(iterations):
        deck = createDeck()
        shuffle(deck)
        hand1 = [deck.pop(0) for _ in range(5)]
        hand2 = [deck.pop(0) for _ in range(5)]

        win = True if compareHands(hand1, hand2) == 0 else False
        result.append((handValue(hand1)[0], win))

    result = dict(Counter(result))
    result = dict(sorted(result.items(), key=lambda item: item[0][1], reverse=True))

    chances = {}
    for k, v in result.items():
        if k[1]:
            if result.get((k[0], False)):
                chances[k[0]] = v / (v + result.get((k[0], False))) * 100
            else:
                chances[k[0]] = 100

    chances = dict(sorted(chances.items(), key=lambda item: (item[1], item[0][0]), reverse=True))
    for k, v in chances.items():
        print(f'{k} \t\t {v:.2f}%')

# winning chance with or without drawing the Joker
def s_JokerWinChance():
    result = []
    iterations = 1_000_000

    for _ in range(iterations):
        deck = createDeck()
        shuffle(deck)
        hand1 = [deck.pop(0) for _ in range(5)]
        hand2 = [deck.pop(0) for _ in range(5)]

        havejoker = True if 'Joker' in str(hand1) else False
        win = True if compareHands(hand1, hand2) == 0 else False

        result.append((havejoker, win))

    chances = dict(Counter(result))
    chances = dict(sorted(chances.items(), key=lambda item: (item[0][0], item[0][1])))

    print(chances)
    lis_chances = list(chances.values())
    print(f'When no joker:\n\tWin:\t{lis_chances[1]}\t{lis_chances[1]/(lis_chances[0]+lis_chances[1])*100:.2f}\t%\n',
          f'\tLoss:\t{lis_chances[0]}\t{lis_chances[0]/(lis_chances[0]+lis_chances[1])*100:.2f}\t%\n',
          f'When have joker:\n\tWin:\t{lis_chances[3]}\t{lis_chances[3]/(lis_chances[2]+lis_chances[3])*100:.2f}\t%\n',
          f'\tLoss:\t{lis_chances[2]}\t{lis_chances[2] / (lis_chances[2] + lis_chances[3]) * 100:.2f}\t%\n')

# in a given hand, what's the win rate after swapping 1-5 cards
def s_WhenToSwap():

    iteration = 2_000

    deck = createDeck()
    print(deck)
    hand1ids = [1, 2, 3, 6, 16]
    discardids = [0, 1, 2, 3]

    hand1 = [deck[i] for i in hand1ids]
    deck = [deck[i] for i in range(len(deck)) if i not in hand1ids]

    discards = [hand1[i] for i in discardids]
    print('deck:\t', deck)
    print(f'hand:\t', hand1)
    print('discard:', discards)
    print()

    # calculate the original winrate for later comparison

    result = []
    for _ in range(iteration):
        newdeck = deck.copy()
        shuffle(newdeck)

        hand2 = [newdeck.pop(0) for _ in range(5)]
        win = True if compareHands(hand1, hand2) == 0 else False
        result.append(win)

    result = dict(Counter(result))

    print(f'Before:\n\tWin:\t{result[True]}\t{result[True]/iteration*100:.2f} %')
    print(f'\tLoss:\t{result[False]}\t{result[False]/iteration*100:.2f} %' if result.get(False) else '', end='')

    # discard and redraw
    discards = len(discardids)
    hand1 = [hand1[i] for i in range(len(hand1)) if i not in discardids]


    print()


    result = []
    for _ in range(iteration):
        newdeck = deck.copy()
        shuffle(newdeck)

        newhand1 = hand1.copy()
        newhand1 += [newdeck.pop(0) for _ in range(discards)]

        hand2 = [newdeck.pop(0) for _ in range(5)]
        win = True if compareHands(newhand1, hand2) == 0 else False
        result.append(win)

    result = dict(Counter(result))
    print(f'After:\n\tWin:\t{result[True]}\t{result[True] / iteration * 100:.2f} %')
    print(f'\tLoss:\t{result[False]}\t{result[False]/iteration*100:.2f} %' if result.get(False) else '', end='')


if __name__ == '__main__':
    s_WhenToSwap()
    