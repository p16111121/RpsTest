# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
from time import sleep
from sklearn.tree import DecisionTreeClassifier


def is_win(play1, play2):
    if play1 == play2:
        return 0
    elif (play1 == "P" and play2 == "R") or (play1 == "R" and play2 == "S") or (play1 == "S" and play2 == "P"):
        return 1
    elif (play2 == "P" and play1 == "R") or (play2 == "R" and play1 == "S") or (play2 == "S" and play1 == "P"):
        return -1


def player(prev_play, opponent_history=[], play_history=[], model=[], play_order=[], index=[]):
    # parameters
    guess = 'S'
    encode = {'P': [0], 'R': [1], 'S': [2]}
    decode = ['P', 'R', 'S']
    win = {'P': 'S', 'R': 'P', 'S': 'R'}

    # player
    if prev_play == '':
        if len(index) == 0: index.append(0)
        else: index[0] += 1
        opponent_history.clear()
        play_history.clear()
        model.clear()
        play_order.clear()
        play_order.append({
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          })

        model.append(DecisionTreeClassifier())
        play_history.append(guess)
        return guess
    else: opponent_history.append(prev_play)

    # strategy
    x = [ encode[ play_history[-1:][0] ] ]
    y = encode[ opponent_history[-1:][0] ]
    model[0].fit(x, y)
    tree_pred = model[0].predict(x)[0]
    tree_play = win[ decode[tree_pred] ]

    # predict
    last_two = "".join(play_history[-2:])
    if len(last_two) == 2:
        play_order[0][last_two] += 1

    potential_plays = [
        play_history[-1] + "R",
        play_history[-1] + "P",
        play_history[-1] + "S",
    ]

    sub_order = {
        k: play_order[0][k]
        for k in potential_plays if k in play_order[0]
    }

    play_pred = max(sub_order, key=sub_order.get)[-1:]
    opp_move = win[ play_pred ]

    # check
    count = 0
    if index[0] != -1 and len(play_history) > 10:
        for i in range(1, 10):
            if is_win(opponent_history[-i], play_history[-i-1]) == 1:
                count += 1
        if count >= 5:
            index[0] = -1

    # combine
    if index[0] == -1:
        guess = win [ win[ play_history[-1] ] ]
    elif play_pred == tree_play and tree_play == play_history[-1]:
        guess = win[ win[tree_play] ]
    else:
        guess = tree_play

    play_history.append(guess)
    return guess