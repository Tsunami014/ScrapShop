import requests
import json
import os
import re

CACHE = "cache.json" # str file path or None
COIN = "⧖"

_reg = re.compile("\033\\[[0-9;]+.")
def stripAnsi(txt):
    return re.sub(_reg, "", txt)
def strlen(txt):
    return len(re.sub(_reg, "", txt))

class Item:
    def __init__(self, dat):
        self.name = dat['name'].capitalize()
        self._desc = dat['description'].capitalize()
        self.heart = dat['heartCount']
        self.category = dat['category']
        self.count = dat['count']
        self.upgrCost = dat['nextUpgradeCost']
        self.upgrProb = dat['boostAmount']

        self.data = dat
        self.title() # Also updates self.score

        self.upgrades = 0
        self.want = False

    def title(self):
        if self.soldout:
            self.score = 0
            return f"\033[90m{self.name}\n\033[90mSold out"

        # cols - 0 good, 1 warn, 2 bad
        def convColour(col):
            return \
                "92" if col < 1 else \
                "93" if col < 2 else \
                "91"
        countnorm = max((20-self.count)/5, 0)
        probnorm = (100-self.probability)/30
        heartnorm = self.heart/7
        costnorm = self.cost/12
        upgrprobnorm = (20-self.upgrProb)/7
        upgrcostnorm = self.upgrCost/6
        allcols = [countnorm, probnorm, heartnorm, costnorm, upgrprobnorm, upgrcostnorm]
        self.score = sum(min(i, 3) for i in allcols)/len(allcols) - 0.3
        return (
            f"\033[{convColour(self.score)}m{self.name}"
            "\033[39m "
            f"\033[1;{convColour(countnorm)}mx{self.count}\n"

            f"\033[1;{convColour(probnorm)}m{self.probability}%"
            "\033[39m "
            f"\033[1;{convColour(heartnorm)}m{self.heart}♥"
            "\033[39m "
            f"\033[1;{convColour(costnorm)}m{COIN}{self.cost}"
            "\033[39m(↑"
                f"\033[1;{convColour(upgrprobnorm)}m{self.upgrProb}% "
                f"\033[1;{convColour(upgrcostnorm)}m{COIN}{self.upgrCost}"
            "\033[39m)"
        )

    @property
    def probability(self):
        return self.data['effectiveProbability']
    @property
    def cost(self):
        return max(1, round(self.data['price'] * (self.data['baseProbability'] / 100)))
    @property
    def soldout(self):
        return self.count == 0

    def sort(self):
        return (self.soldout, self.score, -self.probability)

    def __repr__(self): return self.name
    def __str__(self): return self.name

    def desc(self):
        if self.soldout:
            return "Sold out\n\n"+\
                f"{self._desc}"
        return f"{self.name} ({self.category})\n"+\
            f"Only {self.count} left, {self.heart} ppl hearted\n"+\
            f"Next upgrade: {COIN}{self.upgrCost} (+{self.upgrProb}%)\n"+\
            "\n"+\
            f"{self._desc}"


def get_shop():
    print("Loading the shop...")
    if CACHE and os.path.exists(CACHE):
        with open(CACHE) as f:
            dat = json.load(f)
    else:
        req = requests.get("https://api.scraps.hackclub.com/shop/items")
        req.raise_for_status()
        dat = req.json()
        if CACHE:
            with open(CACHE, "w+") as f:
                json.dump(dat, f)
    li = [Item(d) for d in dat]
    li.sort(key=lambda it: it.sort())
    return li
