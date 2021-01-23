import re
from fractions import Fraction

"""
['2/1', '9/4', '7/2', '5/1', '14/1', '20/1']
 
['8/13', '5/1', '7/1', '10/1', '12/1', '20/1', '33/1', '50/1', '50/1', '100/1']

['4/1', '4/1', '6/1', '8/1', '8/1', '8/1', '10/1', '14/1', '14/1', 
'16/1', '16/1', '20/1', '33/1', '50/1', '50/1', '66/1', '66/1']

"""



def get_place_chances_for(list_of_odds, places):
    my_race = race(list_of_odds, places)
    result = my_race.place_chance_dict.copy()
    my_race = None
    return result

class nag:
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
        odds = re.sub(r'[JF]$', '', odds)
        if odds[0:2] == "Ev":
            self.fraction = Fraction(1)
        else:
            try:
                self.fraction = Fraction(odds)
            except ValueError:
                self.fraction = 0

    def set_inverse(self):
        if self.fraction > 0:
            self.float_odds = float(1/(1+self.fraction))
        else:
            self.float_odds = 0

#        self.float_odds = float(1/(1+self.fraction)) if self.fraction > 0 else 0

class race:
    places = 0
    nags = []
    normalised_odds = []
    place_chance_dict = {}
    def __init__(self, odds_list, places):
        self.nags = []
        self.normalised_odds = []
        self.place_chance_dict = {}
        self.places = places
        for odds in odds_list:
            if odds:
                my_nag = nag(odds)
                self.nags.append(my_nag)
        self.normalise_odds()
        self.calculate_place_chance()

    def normalise_odds(self):
        sum_odds = sum([nag.float_odds for nag in self.nags])
        for nag in self.nags:
            normalised = nag.float_odds / sum_odds
            nag.normalised = normalised # = win chance
            self.normalised_odds.append(normalised)

    def calculate_place_chance(self):
        mydict = {}
        for odds in set(self.normalised_odds):
            # chance of placing 1st
            mydict[odds] = odds
            # chance of placing 2nd
            if self.places > 1:
                mydict[odds] += self.calculate_2nd(odds)
            # chance of placing 3rd
            if self.places > 2:
                mydict[odds] += self.calculate_3rd(odds)
            # chance of placing 4th
            if self.places > 3:
                mydict[odds] += self.calculate_4th(odds)
        for nag in self.nags:
            nag.chance = mydict[nag.normalised]
            self.place_chance_dict[nag.odds] = [nag.normalised, nag.chance]

    def calculate_2nd(self, odds):
        odds_list_first = self.normalised_odds.copy()
        odds_list_first.remove(odds)
        chance = 0
        for first in odds_list_first:
            chance += first * odds / (1 - first)
        return chance

    def calculate_3rd(self, odds):
        odds_list_first = self.normalised_odds.copy()
        odds_list_first.remove(odds)
        chance = 0
        for first in odds_list_first:
            odds_list_second = odds_list_first.copy()
            odds_list_second.remove(first)
            for second in odds_list_second:
                chance += first * second / (1 - first) * odds / (1 - first - second)
        return chance

    def calculate_4th(self, odds):
        odds_list_first = self.normalised_odds.copy()
        odds_list_first.remove(odds)
        chance = 0
        for first in odds_list_first:
            odds_list_second = odds_list_first.copy()
            odds_list_second.remove(first)
            for second in odds_list_second:
                odds_list_third = odds_list_second.copy()
                odds_list_third.remove(second)
                for third in odds_list_third:
                    chance += first * second / (1 - first) * third / (1 - first - second) * odds / (1 - first - second - third)
        return chance




"""
Je krijgt een list of odds
Je wil een dict returnen
odds -> chance
Dus voor elke odds in de orig series wil je een chance teruggeven

"""