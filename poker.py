from enum import Enum

usedCards = []


class Card:

    def __init__(self, card):
        self.setValue(card[0])
        self.setSuit(card[1])

    # Turns the first element of a card into a number
    def setValue(self, value):
        validValueLetter = ['T', 'J', 'Q', 'K', 'A']

        # Raise an exception is the value is not from the valid list above or a digit
        if value not in validValueLetter and not value.isdigit():
            raise Exception("Input Error: One of your value has an invalid letter")

        if value == "T":
            self.value = 10
        elif value == "J":
            self.value = 11
        elif value == "Q":
            self.value = 12
        elif value == "K":
            self.value = 13
        elif value == "A":
            self.value = 14
        else:
            self.value = int(value)

        # Raise an exception if the final value is not between 2 and 14 (ace)
        if self.value not in range(2, 15):
            raise Exception("Input Error: One of your cards had an invalid value: " + str(self.value))

        return self

    def setSuit(self, suit):
        validSuit = ['s', 'h', 'd', 'c']

        # Raise an exception if the final suit is not part of the valid suits
        if suit not in validSuit:
            raise Exception("One or several of your cards had an unknown suit.")
        self.suit = suit
        return self

    def getValue(self):
        return self.value

    def getSuit(self):
        return self.suit


class Hand:

    class Ranking(Enum):
        WIN = 1
        LOSS = 2
        TIE = 3

    class Score(Enum):
        ROYAL_FLUSH = 9
        STRAIGHT_FLUSH = 8
        FOUR_OF_A_KIND = 7
        FULL_HOUSE = 6
        FLUSH = 5
        STRAIGHT = 4
        THREE_OF_A_KIND = 3
        TWO_PAIRS = 2
        PAIR = 1
        NONE = 0

    # Receive a string of all 5 cards, parse the hand: split the string in card, create object card
    def __init__(self, stringOfCards):
        # Hand = list of Card objects that are passed below
        self.hand = []

        # valueAllCards = list of all the values of the hand
        self.valueAllCards = []

        # suitAllCards = list of all the suits of the hand
        self.suitAllCards = []

        # score = when assign a ranking (flush, pair..), implicit score defined above
        self.score = 0

        # highest = in case of tie,have to keep track of the highest cards (or array in descending order) for comparison
        self.highest = []

        # status = win, loss, tie hand
        self.status = 0

        # If no error, parse the given string into a list of Card objects
        try:
            self.parseHand(stringOfCards)

        # Catch other exception that happened while parsing the hand
        except Exception as e:
            print("Error: " + str(e))

        # If no error, get all the values and all the suits of the hand
        try:
            self.translateValueAndSuit()

        # Catch any exception that happened while turning a card into value and suit
        except Exception as e:
            print("Error: " + str(e))

    def parseHand(self, stringOfCards):
        # listOfCards = list of cards as substring of the string of all the cards
        listOfCards = stringOfCards.split()  # split by the space by default

        # Raise an exception if splits the string into more than 5 substrings
        if len(listOfCards) != 5:
            raise Exception("Error input: There are too many cards in your input")

        for i in range(len(listOfCards)):
            card = listOfCards[i]

            # Raise an exception if the cards substring are not made of 2 elements
            if len(card) != 2:
                raise Exception("Error Format: Your cards should be only 2 letters. Card entered: ", card)

            usedCards.append(card)  # List of used card to verify that cards are only used once
            newCard = Card(card)
            self.hand.append(newCard)

    def translateValueAndSuit(self):
        # for each Card object, call the Card method to get all the value and all the suits in 2 distinct lists
        for i in range(len(self.hand)):
            card = self.hand[i]
            self.valueAllCards.append(card.getValue())
            self.suitAllCards.append(card.getSuit())

        # sort the values in descending orders to facilitate future comparisons
##        sorted(self.valueAllCards, key=int, reverse=True)
        self.valueAllCards.sort(reverse=True)

    # Compare the number of distinct cards, check the possible score and assign it to the hand
    # set highest card directly or as a side effect of hasSimilar() method
    def setScore(self):

        # The number of distinct cards is a first selection of the potential ranking (see readme)
        distinctCards = len(set(self.valueAllCards))

        # 5 distinct cards=> Royal/ Straight Flush / Straight / Flush / none
        if distinctCards == 5:
            if self.isStraight() and self.sameSuit() and self.valueAllCards[0] == 14:
                self.score = self.Score.ROYAL_FLUSH
                self.highest = self.valueAllCards[0]
            elif (self.isStraight() or self.isStraightWithAce()) and self.sameSuit():
                self.score = self.Score.STRAIGHT_FLUSH
                self.highest = self.valueAllCards[0]
            elif self.isStraight() or self.isStraightWithAce():
                self.score = self.Score.STRAIGHT
                self.highest = self.valueAllCards[0]
            elif self.sameSuit():
                self.score = self.Score.FLUSH
                self.highest = self.valueAllCards
            else:
                self.score = self.Score.NONE
                self.highest = self.valueAllCards

        else:
            similarCards = self.hasSimilar()   # In that case the highest are set in the hasSimilar() method

            # 4 distinct cards => pair
            if distinctCards == 4:
                if similarCards == 2:                   # this is just a double check as it should not be otherwise
                    self.score = self.Score.PAIR

            # 3 distinct cards => 3 of a kind / 2 pairs
            elif distinctCards == 3:
                if similarCards == 3:
                    self.score = self.Score.THREE_OF_A_KIND
                elif similarCards == 22:                # this is just a double check as it should not be otherwise
                    self.score = self.Score.TWO_PAIRS

            # 2 distinct cards =>  4 of a kind / full house
            elif distinctCards == 2:
                if similarCards == 4:
                    self.score = self.Score.FOUR_OF_A_KIND
                elif similarCards == 5:                 # this is just a double check as it should not be otherwise
                    self.score = self.Score.FULL_HOUSE

            else:
                raise Exception("Not able to give a score to this hand")

        return self

    # check if all the suits are similar by comparing the first element to the other element of the list
    def sameSuit(self):
        suits = self.suitAllCards
        for i in range(1, len(suits)):
            if suits[0] != suits[i]:
                return False                    # Return False as soon as it finds a difference
            else:
                return True

    # Check how many times a card appears in a hand (with built-in function `count`)
    def hasSimilar(self):

        cards = self.valueAllCards
        for i in range(len(cards)):

            # If the first identified element is a pair, check if it's part of a full house or double pair
            if cards.count(cards[i]) == 2:
                pairCard = cards[i]         # Keep track of the 1st pair to put it as first el of the highest array
                del cards[i]                # and delete it to be able to extend the array with the other numbers
                del cards[i]

                # check if there are still enough elements in the list
                if i < 2:
                    # Full house, highest is only one of the 3 similar cards
                    if i <= 3 and cards.count(cards[i]) == 3:
                        self.highest.append(cards[i])
                        return 5

                    # Double pair (had to split to be able to set for highest)
                    elif cards.count(cards[i]) == 2:
                        otherPair = cards[i]
                        del cards[i]
                        del cards[i]
                        self.highest.append(pairCard)    # Highest for double pair is 1st pair, 2nd pair, last element
                        self.highest.append(otherPair)   # The 1st pair is > 2nd because the list is sorted
                        self.highest.append(cards[0])
                        return 22

                    # Double pair
                    elif cards.count(cards[i + 1]) == 2:
                        otherPair = cards[i + 1]
                        del cards[i + 1]
                        del cards[i + 1]
                        self.highest.append(pairCard)
                        self.highest.append(otherPair)
                        self.highest.append(cards[0])
                        return 22

                    # Pair
                    else:
                        self.highest.append(pairCard)
                        self.highest.extend(cards)
                        return 2

                # There is no other repeating numbers
                # = Pair in the middle or end
                else:
                    self.highest.append(pairCard)
                    self.highest.extend(cards)
                    return 2

            # If the first identified element is a triple, needs to check for full house
            elif cards.count(cards[i]) == 3:
                self.highest.append(cards[i])

                # case of a full house
                if i == 0 and cards.count(cards[3]) == 2:
                    return 5

                # case of 3 of a kind
                return 3

            # Four of a kind, not other combination possible and only one el for the highest
            elif cards.count(cards[i]) == 4:
                self.highest.append(cards[i])
                return 4

        # has not found anything (in theory shouldn't happen
        return 0

    # As the list is sorted, if it's a straight the last element should be equals to the first - 4
    def isStraight(self):                           
        cards = self.valueAllCards
        if cards[len(cards) - 1] != (cards[0] - (len(cards) - 1)):
            return False
        else: 
            return True
        
    def isStraightWithAce(self):                   # Same as above + special case: ace as first card (a = 14)
        cards = self.valueAllCards
        if cards[0] == 14 and cards[len(cards) - 1] != (cards[1] - (len(cards) - 2)):
            return True
        else:
            return False

    def compareWith(self, hand2):

        self.setScore()
        hand2.setScore()

        score1 = self.score.value
        score2 = hand2.score.value

        # Use the usedCards list, turn into a set to check that 10 distinct cards are used. Otherwise raise an exception
        if len(set(usedCards)) < 10:
            raise Exception("Input error: one same card was found in two hands")

        if score1 > score2:
            self.status = self.Ranking.WIN
            hand2.status = hand2.Ranking.LOSS

        elif score2 > score1:
            self.status = self.Ranking.LOSS
            hand2.status = hand2.Ranking.WIN
        elif score1 == score2:
            for i in range(len(self.highest)):
                if self.highest[i] > hand2.highest[i]:
                    self.status = self.Ranking.WIN
                    hand2.status = hand2.Ranking.LOSS
                    return
                elif self.highest[i] < hand2.highest[i]:
                    self.status = self.Ranking.LOSS
                    hand2.status = hand2.Ranking.WIN
                    return
            self.status = self.Ranking.TIE
            hand2.status = hand2.Ranking.TIE

    def displayWinner(self):

        global usedCard
        usedCard = []

        if self.status == self.Ranking.WIN:
            print("Player 1 won this game!")
        elif self.status == self.Ranking.LOSS:
            print("Player 2 won this game!")
        elif self.status == self.Ranking.TIE:
            print("No winner for this game...")

