import itertools
import collections

SYMBOLS = '23456789TJQKA'
BLACK_SUITS = 'CS'
RED_SUITS = 'HD'



def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    ranks = [SYMBOLS.index(i[0]) for i in hand]
    ranks.sort()
    ranks.reverse()
    return ranks




def flush(hand):
    """Возвращает True, если все карты одной масти"""
    return len(set([suit for rank, suit in hand])) == 1




def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""

    c = collections.Counter(ranks)
    for k, v in c.items():
        if v == n:
            return k
        else:
            None




def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    return set(map(lambda a,b: a-b, ranks, ranks[1:])) == {1}



def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    c = collections.Counter(ranks)
    a = []
    for k, v in c.items():
        if v == 2:
            a.append(k)
    if len(a) < 2:
        return None
    else:
        return a[0], a[1]



def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    five_card_hands = itertools.combinations(hand, 5)
    result = max(five_card_hands, key=hand_rank)
    return result



def variants(hand):
    for card in hand:
        if not card.startswith('?'):
            yield [card]
        else:
            color = card[1]
            suits = black_suits if color == 'B' else red_suits
            yield set(r + s for r in symbols for s in suits) - set(hand)


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    hands = list(itertools.product(*variants(hand)))
    bests = set([best_hand(el) for el in hands])
    return max(bests, key=hand_rank)



def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')

if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
