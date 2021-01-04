
"""
Meeting>>cumOdds

	| accum cumOdds |
	self meeting races size < 6 ifTrue: [^0].
	accum := ((self meeting races first: 6) reject: [ :each | each hasResults ]) inject: 1 into: 
		[ :cum :race | cum * race myPlaceOdds ].
	accum isZero ifTrue: [cumOdds := 0] ifFalse: [cumOdds := ((1-accum)/accum) asFloat].
	^(cumOdds roundTo: 0.1) displayString, ' / ', (self meeting myPlaceOdds roundTo: 0.1) displayString.
"""

"""
BlokeSystemMeeting>>findWinningBSLines
	| score lines |
	score := self findAllPlacedNags.
	lines := Bag new.
	(score at: 1) do: 
		[:a | (score at: 2) do: 
			[:b | (score at: 3) do: 
				[:c | (score at: 4) do: 
					[:d | (score at: 5) do: 
						[:e | (score at: 6) do: 
							[:f | | line |
								line := Array new: 6.
								line
										at: 1 put: a;
										at: 2 put: b;
										at: 3 put: c;
										at: 4 put: d;
										at: 5 put: e;
										at: 6 put: f.
								lines add: line]]]]]].
	^lines select: 
			[:each | 
			(each occurrencesOf: 1) = 3 
				and: [(each occurrencesOf: 2) = 2 and: [(each occurrencesOf: 3) = 1]]]
"""


"""
Nag>>estRatio

	| oddsFactor ffFactor bfBackedFactor result |
	self rpForecast isZero ifTrue: [^0]. 
	oddsFactor := 1/((self rpForecast + self bfOdds + 0.0000001) raisedTo: 2).
	ffFactor := 1 + (self formPoints * 0.05).
	bfBackedFactor := 1.
	(self rpForecast isZero not and: [self bfOdds isZero not]) ifTrue: 
		[bfBackedFactor := 1 - (((self bfOdds - self rpForecast) / self bfOdds) * 0.3)].
	result := oddsFactor * ffFactor * bfBackedFactor.
	self nonRunner ifTrue: [^0 "result/2"].
	^result
"""

"""
Nag>>formPoints

	|points last oneBut result formThisSeason|
	points := #(5 3 2 1).
	last := 0. oneBut := 0. result := 0.
	formThisSeason := self form reverse readStream upTo: $/.
	formThisSeason := formThisSeason readStream upTo: $-.
	formThisSeason isEmpty ifFalse: [formThisSeason first isDigit ifTrue: [last := formThisSeason first asString asNumber]].
	formThisSeason size > 1 ifTrue: [
		oneBut := formThisSeason at: 2.
		oneBut isDigit ifTrue: [oneBut := oneBut asString asNumber] ifFalse: [oneBut := 0]].
	((last < 5) and: [last isZero not]) ifTrue: [result := result + (points at: last)].
	((oneBut < 5) and: [oneBut isZero not]) ifTrue: [result := result + (points at: oneBut)].
"	self courseWinner ifTrue: [result := result + 1].
	self distanceWinner ifTrue: [result := result + 2].
"	^result
"""

"""
Nag>>placeOdds
	self placeChance isZero ifTrue: [^0].
	^(((1 - self placeChance) / self placeChance + 1) - 1) asScaledDecimal: 2
"""

def place_odds(nag):
    if nag.place_chance == 0:
        return 0
    else:
        return ((1 - nag.place_chance) / (nag.place_chance + 1)) - 1


"""
Nag>>ppEstIncFav
	self isPreRaceFav ifTrue: [^self ppEst + self race ppFavEst].
	^self ppEst
"""

"""
BlokeSystemNag>>setPlaceChanceBasis

	self race hasFinalOdds 
		ifTrue: [
			self slFinalOdds isZero ifTrue: [^self placeChanceBasis: 0].
			^self placeChanceBasis: ((1/(1 + self slFinalOdds)) asFloat roundTo: 0.000001)].
	self race hasLiveShows
		ifTrue: [
			self preRaceShow isEmpty ifTrue: [^self placeChanceBasis: 0].
			^self placeChanceBasis: ((1/(1 + self preRaceShow last)) asFloat 
				roundTo: 0.000001)].
	self race hasBFOdds
		ifTrue: [
			self bfOdds isZero ifTrue: [^self placeChanceBasis: 0].
			^self placeChanceBasis: ((1/(1 + self bfOdds)) asFloat roundTo: 0.000001)].
	self rpForecast isZero ifTrue: [^self placeChanceBasis: 0].
	self placeChanceBasis: ((1/(1 + self rpForecast)) asFloat roundTo: 0.000001)
"""

def sp_placechancebasis(nag):
    return (1 / (1 + nag.sp)) if nag.sp else 0

def rp_forecast_placechancebasis(nag):
    return (1 / (1 + nag.rp_forecast)) if nag.rp_forecast else 0

"""
Rac>>calculateBookiesPercentage
	"return the difference of 100% and the sum of rp forecast odds"

	self nags isEmpty ifTrue: [^self bookiesPercentage: 0].
	^self bookiesPercentage: (self nags inject: -1 into: [ :sum :nag | sum + nag rpGrossChance])
"""


"""
BlokeSystemRace>>setBlokeSystemFavs
	| sorted skip |
	self leg = 1 
		ifTrue: [sorted := self nags asSortedCollection: [:a :b | a compareSlFinalOddsWith: b].
			skip := (sorted first slFinalOdds - 3) ceiling min: sorted size - 3] 
		ifFalse: [sorted := self nags asSortedCollection: [:a :b | a compareRpForecastWith: b].
			skip := (sorted first rpForecast - 3) ceiling min: sorted size - 3].
	skip negative ifTrue: [skip := 0].
	1 to: (3 min: sorted size) do: [:i | (sorted at: skip + i) fav: i]
"""

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

"""
HRRacePlaceCalc>>allRunnersBasis

	allRunnersBasis ifNil: [allRunnersBasis := self sumOfPlaceChanceBasisFor: self allRunners].
	^allRunnersBasis
	
sumOfPlaceChanceBasisFor: aCollection

	^aCollection inject: 0 into: [ :sum :each | sum + each placeChanceBasis ]
"""

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


"""
calculateFirstPlaceChance

	| final basis |
	final := self places < 2.
	basis := self allRunnersBasis.
	basis isZero ifTrue: [^self].
	self allRunners do: [ :each |
		each placeChance: ((each placeChanceBasis / basis) roundTo: 0.000001).
		final ifTrue: [self addPPPlaceValueFor: (Array with: each) chance: each placeChance ]].
	final ifFalse: [ self calculateSecondPlaceChance ].
"""

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
