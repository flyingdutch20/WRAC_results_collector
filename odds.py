from fractions import Fraction


class nag(odds):
    odds = ""
    fraction = Fraction(0)
    float_odds = 0
    normalised = 0
    chance = 0
    def __init__(self, odds):
        self.odds = odds
        self.set_fraction(odds)
        self.set_inverse()

    def set_fraction(self, odds):
        if odds == "Fav":
            self.fraction = Fraction(1)
        try:
            self.fraction = Fraction(odds)
        except ValueError:
            self.fraction = 0

    def set_inverse(self):
        self.float_odds = float(1/(1+self.fraction))

class race(odds_list):
    places = 0
    nags = []
    normalised_odds = []
    def __init__(self, odds_list):
        for odds in odds_list:
            self.nags.append(nag(odds))
        self.set_places()
        self.normalise_odds()
        self.calculate_place_chance()

    def set_places(self):
        num = len(self.nags)
        if num < 5:
            self.places = 1
        elif num < 8:
            self.places = 2
        elif num < 16:
            self.places = 3
        else:
            self.places = 4
        # note officially if > 15 and not handicap or nursery then places is 3 but not sure how often that happens

    def normalise_odds(self):
        sum_odds = sum([nag.float_odds for nag in self.nags])
        for nag in self.nags:
            normalised = nag.float_odds / sum_odds
            nag.normalised = normalised
            self.normalised_odds.append(normalised)

    def calculate_place_chance(self):
        place_chance_dict = {}
        for odds in set(self.normalised_odds):
            # chance of placing 1st
            place_chance_dict[odds] = odds
            # chance of placing 2nd
            place_chance_dict[odds] += self.calculate_2nd(odds)
            # chance of placing 3rd
            place_chance_dict[odds] += self.calculate_3rd(odds)
            # chance of placing 4th
            place_chance_dict[odds] += self.calculate_4th(odds)

    def calculate_2nd(self, odds):
        return 0

    def calculate_3rd(self, odds):
        return 0

    def calculate_4th(self, odds):
        return 0

"""
Je krijgt een list of odds
Je wil een dict returnen
odds -> chance
Dus voor elke odds in de orig series wil je een chance teruggeven

if places = 1



"""