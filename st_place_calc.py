def place_odds(nag):
    if nag.place_chance == 0:
        return 0
    else:
        return ((1 - nag.place_chance) / (nag.place_chance + 1)) - 1

def sp_placechancebasis(nag):
    return (1 / (1 + nag.sp)) if nag.sp else 0

def rp_forecast_placechancebasis(nag):
    return (1 / (1 + nag.rp_forecast)) if nag.rp_forecast else 0


"""
HRRacePlaceCalc>>addPPPlaceValueFor: anArray chance: aChance

	| cum favs favVal |
	self allPlaceChances addLast: (anArray -> aChance).
	cum := anArray inject: 0 into: [ :sum :each | sum + each ppPercIncFav ].
	cum isZero ifFalse: [anArray do: [ :each |
		each ppPlaceValue: each ppPlaceValue + (((1 / cum) - 1) * aChance) ]].
"""
def all_placechances(race):
    return {}

def add_pp_placevalue_for_chance(nags, chance):
    cum = 0
    for nag in nags:
        cum += nag.pp_perc
    if cum:
        for nag in nags:
            nag.pp_placevalue += ((1 / cum) - 1) * chance

def sp_all_runners_basis(nags):
    basis = 0
    for nag in nags:
        basis += nag.sp_placechancebasis()
    return basis

def rp_forecast_all_runners_basis(nags):
    basis = 0
    for nag in nags:
        basis += nag.rp_forecast_placechancebasis()
    return basis


def sp_calculate_first_placechance(nags, places):
    basis = sp_all_runners_basis(nags)
    for nag_1 in nags:
        nag_1.sp_placechance = (nag_1.sp_placechancebasis / basis)
        if places == 1:
            add_pp_placevalue_for_chance([nag_1], nag_1.sp_placechance)
    if places > 1:
        sp_calculate_second_placechance(nags, places)

"""
calculateSecondPlaceChance

	| final basis |
	final := self places = 2.
	basis := self allRunnersBasis.
	basis isZero ifTrue: [basis := 1].
	self allRunners do: [ :first |
		self allRunners do: [ :second |
			second == first ifFalse: [ | chance |
				chance := [(first placeChanceBasis * second placeChanceBasis / 
					basis /
					(basis - first placeChanceBasis)) roundTo: 0.000001] on: ZeroDivide do: [ :i | 0 ].
				second placeChance: (second placeChance + chance).
				final ifTrue: [self addPPPlaceValueFor: (Array with: first with: second) chance: chance].
				]
			]
		].
	final ifFalse: [ self calculateThirdPlaceChance ].
"""
def sp_calculate_second_placechance(nags, places):
    basis = sp_all_runners_basis(nags)
    for nag_1 in nags:
        nags_2 = nags.copy()
        nags_2.remove(nag_1)
        for nag_2 in nags_2:
            chance = nag_1.sp_placechancebasis * nag_2.sp_placechancebasis / basis / (basis - nag_1.sp_placechancebasis)
        nag.sp_placechance = (nag.sp_placechancebasis / basis)
        if places == 2:
            add_pp_placevalue_for_chance([nag], nag.sp_placechance)
    if places > 2:
        sp_calculate_third_placechance(nags, places)


"""
calculateFourthPlaceChance

	| basis myNags |
	myNags := self allRunners.
	basis := self allRunnersBasis.
	basis isZero ifTrue: [basis := 1].
	myNags size > 25 ifTrue: [
		myNags := self mainRunners.
		basis := self mainRunnersBasis ].
	myNags do: [ :first |
		myNags do: [ :second |
			second == first ifFalse: [
				myNags do: [ :third |
					((third ~~ second) and: [third ~~ first]) ifTrue: [
						myNags do: [ :fourth |
							((fourth ~~ third) and: [(fourth ~~ second) and: 
								[fourth ~~ first]]) 
							ifTrue: [ | chance |
	chance := [(first placeChanceBasis * second placeChanceBasis * 
		third placeChanceBasis * fourth placeChanceBasis / 
		basis /
		(basis - first placeChanceBasis) / 
		(basis - first placeChanceBasis - second placeChanceBasis) /
		(basis - first placeChanceBasis - second placeChanceBasis - third placeChanceBasis)
		) roundTo: 0.000001] on: ZeroDivide do: [ :i | 0 ].
	fourth placeChance: (fourth placeChance + chance).
	self addPPPlaceValueFor: 
			(Array with: first with: second with: third with: fourth) chance: chance.
								]
							]
						]
					]
				]
			]
		].
"""

"""
calculateMyRacePlaceOdds

	| myPicks myChances fav |
	fav := self nags detect: [ :nag | nag baseNag == self bestOddsFav ].
	myPicks := self nags select: [ :nag | nag mySelect ].
	self myUnnamedFav ifTrue: [myPicks addLast: fav].
	myPicks isEmpty ifTrue: [^0].
	((myPicks anySatisfy: [ :each | each nonRunner ]) and: [self myUnnamedFav not]) ifTrue: [myPicks addLast: fav].
	myChances := self allPlaceChances select: [ :each | each key includesAnyOf: myPicks ].
	^myChances inject: 0 into: [ :sum :mine | sum + mine value ]
"""

"""
calculatePlaceChance
	"first set to zero"
"	self nags do: [ :each | each placeChance: 0; placeChanceBasis: nil; ppPlaceValue: 0.].
	self setPreRaceFavs.
	self calculateFirstPlaceChance.
	self subtractNonPlaceValue."
	self calculatePPValue
"""

"""
calculateThirdPlaceChance

	| final basis myNags |
	final := self places = 3.
	myNags := self allRunners.
	basis := self allRunnersBasis.
	basis isZero ifTrue: [basis := 1].
	myNags do: [ :first |
		myNags do: [ :second |
			second == first ifFalse: [
				myNags do: [ :third |
					((third ~~ second) and: [third ~~ first]) ifTrue: [ | chance |
		chance := [(first placeChanceBasis * second placeChanceBasis * 
			third placeChanceBasis / 
			basis /
			(basis - first placeChanceBasis) / 
			(basis - first placeChanceBasis - second placeChanceBasis)) 
			roundTo: 0.000001] on: ZeroDivide do: [ :i | 0 ].
		third placeChance: (third placeChance + chance).
		final ifTrue: [self addPPPlaceValueFor: (Array with: first with: second with: third) chance: chance].
						]
					]
				]
			]
		].
	final ifFalse: [ self calculateFourthPlaceChance ].
"""

"""
findNagsUpTo: aPercentage

	| basis sortedOdds sum index |
	basis := self allRunnersBasis.
	sortedOdds := (self allRunners collect: [ :each | (each placeChanceBasis / basis) 
		roundTo: 0.000001 ]) asSortedCollection: [ :a :b | a > b ].
	sum := 0.
	sortedOdds := sortedOdds collect: [ :each | sum := each + sum ].
	index := sortedOdds findFirst: [ :each | each >= aPercentage ].
	^self allRunnersSorted first: index
"""

"""
mainRunners

	mainRunners ifNil: [mainRunners := self findNagsUpTo: 0.97].
	^mainRunners
"""

"""
spreadLeg1PP: cf between: tmpNags

"	| denom |
	denom := tmpNags inject: 0 into: [ :sum :each | 
		sum + ((1/(each rpForecast + each slFinalOdds + 0.0000001)) raisedTo: 2) ].
	tmpNags do: [ :each | 
		each ppLeg1Est: (cf * ((1/(each rpForecast + each slFinalOdds + 0.0000001)) raisedTo: 2) / denom) asFloat. 
		each ppValue: (each ppLeg1Est roundTo: 0.01)].
"
	| denom |
	denom := tmpNags inject: 0 into: [ :sum :each | 
		sum + each ppEstIncFav ].
	denom isZero ifTrue: [^self spreadLeg1PPOnOdds: cf between: tmpNags].
	tmpNags do: [ :each | 
		each ppLeg1Est: (cf * each ppEstIncFav / denom) asFloat. 
		each ppValue: (each ppLeg1Est roundTo: 0.01)].
"""

"""
spreadLeg1PPOnOdds: cf between: tmpNags

	| denom |
	denom := tmpNags inject: 0 into: [ :sum :each | 
		sum + ((1/(each rpForecast + each slFinalOdds + 0.0000001)) raisedTo: 2) ].
	tmpNags do: [ :each | 
		each ppLeg1Est: (cf * ((1/(each rpForecast + each slFinalOdds + 0.0000001)) raisedTo: 2) / denom) asFloat. 
		each ppValue: (each ppLeg1Est roundTo: 0.01)].

"""
