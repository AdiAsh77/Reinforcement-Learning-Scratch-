import random
import numpy as np
import matplotlib.pyplot as plt

gamma = 0.8
rate_of_inc = 0.1
starting = (2, 0)
goal = (2,5)

print(" ___  ___  ___  ___  ___")
def puz_dis(p):
    for i in p:
        for j in i:
            if j == 0:
                print("|___|", end="")
            elif j == 1:
                print("|_X_|", end="")
            elif j == 2:
                print("|_O_|", end="")

        print("")
    print("\n")

puzzle_matrix = [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 2]]
# block_tuple = [(2,2), (1,2), (2,1), (1,3)]
# block_tuple = [(0,1), (1,1), (2,3), (3,3)]
block_tuple = [(0,1), (1,1), (2,3), (3,3), (2,1), (1, 3)]
row_mat = 4
column_mat = 5

q_table = []
for i in range(row_mat):
    temp = []
    for j in range(column_mat):
        temp.append([0,0,0,0])
    q_table.append(temp)

puz_dis(puzzle_matrix)

action_list = [1,2,3,4] # [up, down, left, right]
state = starting

def action_out(state, action):
    if action == 1:
        new_state = (state[0]-1, state[1])
        
    elif action == 2:
        new_state = (state[0]+1, state[1])

    elif action == 3:
        new_state = (state[0], state[1]-1)

    elif action == 4:
        new_state = (state[0], state[1]+1)

    if (new_state[0] >=0 and new_state[0] <= row_mat-1 and new_state[1] >= 0 and new_state[1] <= column_mat-1 and new_state not in block_tuple):
        return new_state
    else:
        return state

def probability(state, episodes):

    percent = 0.9
    val = percent / 200
    new_per = max(0.15, round((percent - (episodes*val)),3))
    # print(new_per)
    random_num = random.random()
    prob_rand = round(random_num,3)

    if (new_per >= prob_rand):
        return random.choice([1, 2, 3, 4])
    else:
        prob = q_table[ state[0] ][ state[1] ]
        min_list = []
        m = prob[0]

        for i in range(len(prob)):
            if prob[i] > m:
                m = prob[i]

        for i in range(len(prob)):
            if prob[i] == m:
                min_list.append(i+1)

        return random.choice(min_list)
    
return_list = []
penalty_list = []

def maze_path(episodes):
    state = starting
    list_of_states = [state]
    penalty_list = []
    action_list = []
    for i in range(20):
        action = probability(state, episodes)
        next_state = action_out(state, action)
        # print(state, "   ", action, "   ", next_state)

        if (next_state == goal):
            temp = [state, action, 0]
            penalty_list.append(temp)
            list_of_states.append(next_state)
            action_list.append(action)
            break
        else:
            temp = [state, action, -1]
            penalty_list.append(temp)

        state = next_state
        list_of_states.append(state)
        action_list.append(action)
    # print(list_of_states)
    return list_of_states, action_list, penalty_list
# maze_path()

def evaluation(episodes):
    state = starting
    list_of_states = [state]
    reward = 0
    for i in range(20):
        # prob = q_table[ state[0] ][ state[1] ]
        # min_list = []
        # m = prob[0]

        # for i in range(len(prob)):
        #     if prob[i] > m:
        #         m = prob[i]

        # for i in range(len(prob)):
        #     if prob[i] == m:
        #         min_list.append(i+1)

        # action = random.choice(min_list)

        action = probability(state, episodes)
        next_state = action_out(state, action)

        if (next_state == goal):
            reward = reward + 0
            list_of_states.append(next_state)
            break
        else:
            reward = reward + (-1)

        state = next_state
        list_of_states.append(state)
    # print(list_of_states)
    return reward

def eval_plot(j):
    x = j[0]
    y = j[1]
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()
    
# for i in q_table:
#     print(i)

# print("\n")

def rl(episodes):
    list_of_states = []
    penalty_list = []
    action_list = []
    list_of_states, action_list, penalty_list = maze_path(episodes)

    # return calculation:--------
    ans = 0
    for i in range(len(penalty_list)-1, -1,-1):
        ans = penalty_list[i][2] + gamma*ans
        # print(round(ans,2))
        penalty_list[i].append(round(ans,2))

    # updating q_table
    for i in penalty_list:
        # print(i[0], i[3], i[1])
        val = q_table[ i[0][0] ] [ i[0][1] ] [i[1]-1] 
        new_val = round(val + (i[3] - val) * rate_of_inc,3)
        q_table[i[0][0] ][ i[0][1] ][i[1]-1] = new_val
    
    return list_of_states, action_list, q_table

# a,b,c = rl(4)
# for i in c:
#     print(i)

# print("\n")
