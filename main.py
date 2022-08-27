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
    cardv = dict(sorted(cardv.items(), key=lambda item: item[1]))
    cardf = Counter([card.f for card in hand])

    # print(cardv, cardf)

    isflush = True if len(cardf) == 1 else False
    isstraight = True if (len(cardv) == 4 and havejoker) or len(cardv) == 5 else False
    isfiveofakind = True if (len(cardv) == 1) and havejoker else False
    isfourofakind = True if (list(cardv.values())[-1] == 3 and havejoker) or list(cardv.values())[-1] == 4 else False
    isthreeofakind = True if (list(cardv.values())[-1] == 2 and havejoker) or list(cardv.values())[-1] == 3 else False
    isfullhouse = True if (isthreeofakind and len(cardv) == 2) else False
    istwopair = True if (list(cardv.values())[-1] == 2 and list(cardv.values())[-2] == 2 and not havejoker) else False

    combo_number = 10
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

    return combos[combo_number], maxv


def createDeck() -> list:
    deck = []
    for v, f in product(value, flower):
        deck.append(Card(v, f))

    deck.append(Card('K', '♠', joker=True))
    return deck


# s for simulate, one game where two players have a hand
def s_OneGame():

    # create a random deck consist of 17 cards
    deck = createDeck()

    # shuffle the deck
    shuffle(deck)

    # pop a random hand for the player from the top of the deck
    hand1 = [deck.pop(0) for _ in range(5)]
    hand2 = [deck.pop(0) for _ in range(5)]

    # combo is a tuple (combo value, combo name), maxv is int of highest card value
    hand1v = handValue(hand1)
    hand2v = handValue(hand2)

    print(f'hand1: {hand1} \t - {hand1v[0][1]} \nhand2: {hand2} \t - {hand2v[0][1]}')
    if hand1v[0][0] > hand2v[0][0]:
        print('hand1 wins')
    elif hand1v[0][0] < hand2v[0][0]:
        print('hand2 wins')
    else:
        if hand1v[1] > hand2v[1]:
            print('same combo, hand 1 has highest value card and wins')
        else:
            print('same combo, hand 2 has highest value card and wins')

def s_ProbOneHand():

    result = []
    iterations = 5000000

    for _ in range(iterations):
        deck = createDeck()
        shuffle(deck)
        hand = [deck.pop(0) for _ in range(5)]

        # k = handValue(hand)[0]
        # if k[0] == 8:
        #     print(hand)

        result.append(handValue(hand)[0])


    result = dict(Counter(result))
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    for k, v in result.items():
        print(f'{k} \t\t {v/iterations*100:.2f}%')

if __name__ == '__main__':
    s_ProbOneHand()

