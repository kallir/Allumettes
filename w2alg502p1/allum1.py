import sys
import random

#GLOBAL VARIABLES
arr_init = []
arr = []
current_line = -1

def draw(rows):
    width = rows*2 + 1
    print('*'*width)
    for i in range(rows):
        if arr[i] < arr_init[i]:
            k = arr_init[i] - arr[i]
        else:
            k = 0
        print('*' +' '*(rows-i-1) + '|'*arr[i]+ ' '* (rows-i-1+k)+"*")
    print('*'*width)

def game(total, remove, rows, pvp):
    draw(rows)
    while total > 1:
        if pvp:
            total = player_turn("Player 1", remove, rows, total, pvp)
        else:
            total = player_turn("Player", remove, rows, total, pvp)
        if total == 1:
            if pvp:
                print("Player 1 wins!")
                return
            else:
                 print("I lost... snif... but I'll get you next time!!")
                 return 1
        if pvp:
            total = player_turn("Player 2", remove, rows, total, pvp)
            if total == 1:
                print("Player 2 wins!")
                return
        else:
            ai = ai_turn(remove)
            if arr[ai[0]-1] > 0:
                arr[ai[0]-1] -= ai[1]
                total -= ai[1]
            draw(rows)
        if total == 1:
            print("You lost, too bad...")
            return 2

def player_turn(player_name, remove, rows, total, pvp):
    if pvp:
        print(player_name+"'s turn:")
    else:
        print("Your turn:")
    player = player_choice(remove, rows)
    if arr[player[0]-1] > 0:
            arr[player[0]-1] -= player[1]
            total -= player[1]
    print("\n"+player_name+" removed "+str(player[1]) + " match(es) from line "+str(player[0]))
    draw(rows)    
    return total

def player_choice(remove, rows):
    global current_line
    matches_input = "no"
    while matches_check(matches_input, remove) == False:
        line_input = input("Line: ")
        while line_check(line_input, rows) == False:
            line_input = input("Line: ")
        current_line = line_input
        matches_input = input("Matches: ")
    return [int(line_input), int(matches_input)]

def line_check(line_input, rows):
    if not line_input.isdigit() or (line_input.isdigit() and int(line_input) <= 0):
        print("Error: invalid input (positive number expected)")
        return False
    elif not 1 <= int(line_input) <= rows or (arr[int(line_input)-1] == 0):
        print("Error: this line is out of range")
        return False
    else:
        return True

def matches_check(matches_input, remove):
    if matches_input == "no":
        return False
    if int(matches_input) > arr[int(current_line)-1]:
        print("Error: not enough matches on this line")
        return False
    if int(matches_input) > remove:
        print("Error: you cannot remove more than "+str(remove)+" matches per turn")
        return False
    elif int(matches_input) <= 0:
        print("Error: you have to remove at least one match")
        return False
    else:
        return True

def ai_turn(remove):
    av_rows = []
    for i in range(len(arr)):
        if arr[i] > 0:
            av_rows.append(i+1)
    line = random.choice(av_rows)
    if arr[line-1] >= remove:
        matches = random.randint(1, remove)
    else:
        matches = random.randint(1, arr[line-1])
    print("\nAI's turn...\nAI removed " + str(matches) + " match(es) from line "+str(line))
    return [line, matches]

def init(args):
    rows = ""
    total = 0
    if args[-1] == "-pvp":
        pvp = True
    else:
        pvp = False

    if not args[1].isdigit() or not args[2].isdigit():
        print("Invalid input, integers expected")
        return
    if int(args[1])>=100 or int(args[1])<=1:
        print("Error: number of rows must be between 1 and 100")
        return
    elif int(args[2])<=0:
        print("Error: number of removable matchsticks must be bigger than 0")
        return
    else:
        rows = int(args[1])
        remove = int(args[2])
        for i in range(rows):
            arr_init.append(2*i+1)
            arr.append(2*i+1)
        for sticks in arr:
            total += sticks
        game(total, remove, rows, pvp)
init(sys.argv)