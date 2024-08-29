# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

# def player(prev_play, opponent_history=[]):
#     opponent_history.append(prev_play)

#     guess = "R"
#     if len(opponent_history) > 2:
#         guess = opponent_history[-2]

#     return guess

import random

def player(prev_play, opponent_history=[]):
    # Record the opponent's moves
    opponent_history.append(prev_play)

    # Define responses to common strategies
    def counter_quincy():
        cycle = ["R", "R", "P", "P", "S"]
        index = len(opponent_history) % len(cycle)
        return cycle[index]

    def counter_mrugesh():
        last_ten = opponent_history[-10:]
        most_frequent = max(set(last_ten), key=last_ten.count, default="S")
        ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
        return ideal_response[most_frequent]

    def counter_kris():
        if not opponent_history:
            return "R"
        last_play = opponent_history[-1]
        ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
        return ideal_response[last_play]

    def counter_abbey():
        if len(opponent_history) < 2:
            return "R"  # Default response
        last_two = "".join(opponent_history[-2:])
        play_order = {
            "RR": 0, "RP": 0, "RS": 0,
            "PR": 0, "PP": 0, "PS": 0,
            "SR": 0, "SP": 0, "SS": 0,
        }
        play_order[last_two] += 1
        potential_plays = [last_two + "R", last_two + "P", last_two + "S"]
        sub_order = {k: play_order[k] for k in potential_plays if k in play_order}
        prediction = max(sub_order, key=sub_order.get, default=last_two[-1:])
        ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
        return ideal_response[prediction]

    # Select the appropriate counter strategy
    if prev_play == "":
        return random.choice(["R", "P", "S"])

    # Determine which opponent we are facing
    if len(opponent_history) < 5:
        return random.choice(["R", "P", "S"])  # Default random choice for initial moves

    # Use different counters based on the behavior observed
    # This is a heuristic approach; refine it based on testing
    if opponent_history[-1] == "P" and opponent_history[-2] == "R":
        return counter_quincy()
    elif len(opponent_history) > 10 and (opponent_history.count("R") > 5 or opponent_history.count("P") > 5):
        return counter_mrugesh()
    elif prev_play == "S":
        return counter_kris()
    else:
        return counter_abbey()


