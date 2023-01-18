"""
Determines the score for a certain rock-paper-scissor strategy.
Advent of code day 2

Input requires opponents choice, and instruction for the player.
Instruction can be rock-paper-scissor, or lose-draw-win
Different scores are obtained with the 2 interpretations
"""


def calculate_score(choice_opponent, choice_own) -> int:
    """
    Calculates score of a rock-paper-scissors round.

    choices should be integers:
    1 = rock
    2 = paper
    3 = scissors
    """
    score = choice_own
    # 2 = win, 1 = lose, 0 = draw
    outcome = (choice_opponent - choice_own) % 3
    if outcome == 2:
        score += 6
    elif outcome == 0:
        score += 3
    return score


def determine_my_action(choice_opponent, outcome):
    """In part 2, my_instruction is lose, draw, win"""
    if outcome == 2:
        choice_me = choice_opponent
    elif outcome == 1:
        choice_me = (choice_opponent - 1)
    else:
        choice_me = (choice_opponent + 1)
    if choice_me > 3:
        choice_me -= 3
    elif choice_me == 0:
        choice_me = 3
    return choice_me


def main():
    # Convert input letters into input numbers
    choice_dict = {k: int(v) for k, v in zip("ABCXYZ", "123123")}

    with open("Excercises/02/input.txt") as file:
        score_total_1 = score_total_2 = 0
        for line in file:
            choice_opponent = choice_dict[line.split()[0]]
            my_instruction = choice_dict[line.split()[1]]
            score_total_1 += calculate_score(choice_opponent, my_instruction)
            choice_own = determine_my_action(choice_opponent, my_instruction)
            score_total_2 += calculate_score(choice_opponent, choice_own)

        print(score_total_1)
        print(score_total_2)


if __name__ == "__main__":
    main()
