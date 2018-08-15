from poker import Hand

if __name__ == '__main__':
    try:
        hand1 = Hand("As Ac Kc Kd Td")

    except Exception as e:
        print("First hand error: " + str(e))

    try:
        hand2 = Hand("Ah Kh Qh Js Tc")

    except Exception as e:
        print("Second hand error: " + str(e))

    try:
        hand1.compareWith(hand2)

    except Exception as e:
        print("Comparison: " + str(e))

    hand1.displayWinner()