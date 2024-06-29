def player(prev_play, opponent_history=[]):
    # Add the previous play to the opponent history
    if prev_play:
        opponent_history.append(prev_play)

    # Initialize variables
    n = 3  # Number of previous moves to consider for pattern recognition
    if len(opponent_history) < n:
        return "R"  # Default move

    # Identify the most common sequence of the last n moves
    sequence_freq = {"R": 0, "P": 0, "S": 0}
    for i in range(len(opponent_history) - n):
        sequence = "".join(opponent_history[i:i + n])
        next_move = opponent_history[i + n]
        if sequence == "".join(opponent_history[-n:]):
            sequence_freq[next_move] += 1

    # Choose the move that is most likely to follow the identified sequence
    if sequence_freq["R"] > sequence_freq["P"] and sequence_freq["R"] > sequence_freq["S"]:
        guess = "P"
    elif sequence_freq["P"] > sequence_freq["R"] and sequence_freq["P"] > sequence_freq["S"]:
        guess = "S"
    else:
        guess = "R"

    return guess

# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

# def player(prev_play, opponent_history=[]):
#     opponent_history.append(prev_play)

#     guess = "R"
#     if len(opponent_history) > 2:
#         guess = opponent_history[-2]

#     return guess

