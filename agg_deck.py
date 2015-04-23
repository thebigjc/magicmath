# Implmenation of Frank Karsten's 'Aggregate Deck' method
# Takes a list of Magic Workshop (MWS) deck lists and emits the Aggregate Deck

import sys
import re
from collections import Counter

reg = re.compile("(\d+) (\[...\]) (.*)")

def build_deck(f):
    deck = []
    side = []

    for l in f:
        pool = deck

        l = l.strip()
        if l.startswith("//"):
            continue

        if l.startswith("SB:"):
            pool = side
            l = l[3:].strip()

        m = reg.match(l)
        if not m:
            continue

        cnt = int(m.group(1))
        card = m.group(3)

        for i in range(cnt):
            pool.append((i, card))

    return (deck, side)


if __name__ == '__main__':
    deck = Counter()
    side = Counter()

    for fn in sys.argv[1:]:
        with open(fn, 'r') as f:
            (new_deck, new_side) = build_deck(f)
            deck.update(new_deck)
            side.update(new_side)

    for (pool, n, prefix) in ((deck, 60, ""), (side, 15, "SB: ")):
        agg = Counter()
        for c in sorted(pool.most_common(), key=lambda x: (x[1], x[0][1], x[0][0]), reverse=True)[:n]:
            agg.update([c[0][1]])

        for (card, cnt) in agg.most_common():
	  print prefix, cnt, card
