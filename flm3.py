"""
Reimplementation of flm3.c program in Python.
"""


import json
import numpy as np
from numpy.polynomial import Polynomial
import math
import time

_MAX_HEIGHT_ = 13
_MAX_POWER_ = 4 * _MAX_HEIGHT_


def index_to_state(height, index):
    # This is equivalent to converting index to base 3
    state = [0] * (height + 2)
    for i in range(height + 1, 0, -1):
        state[i] = index % 3
        index //= 3
    state[0] = index
    # state[0] = 0, 1, 2, 3 = whether the left partial polygon touches the top or bottom boundary
    return state

def state_to_index(height, state):
    index = 0
    for i in range(0, height + 2):
        index = index * 3 + state[i]
    return index


class State:
    def __init__(self, index : int, coeff : list[int]):
        self.index = index
        self.coeff = coeff.copy()

    def get_state(self, height : int) -> list[int]:
        return index_to_state(height, self.index)


def get_real_total_count(filepath) -> dict[int, dict[int, int]]:
    """
    Reads existing results from a file and returns the results as a dictionary to test against the calculated results
    """
    real_total_count = {}
    with open(filepath, "r") as f:
        data  : dict[str, dict[str, int]] = json.load(f)
        for i, d in data.items():
            real_total_count[int(i)] = {}
            for kv, vv in d.items():
                real_total_count[int(i)][int(kv)] = vv
    return real_total_count


count = [[0] * (_MAX_POWER_ + 2) for _ in range(_MAX_POWER_ + 1)]

new_states_hash : dict[int, State] = {}

def update_state(height, power, p : State, state : list[int]):
    global new_states_hash
    
    sindex = state_to_index(height, state)
    new_states_hash[sindex] = new_states_hash.get(sindex, State(index=sindex, coeff=[0] * power))
        
    for i in range(0, len(p.coeff)):
        if (i + power) < len(new_states_hash[sindex].coeff):
            new_states_hash[sindex].coeff[i + power] += p.coeff[i]
        else:
            new_states_hash[sindex].coeff.append(p.coeff[i])
    
    return new_states_hash[sindex]


def add_site(p : State, row: int, col: int, HEIGHT : int, LENGTH : int):
    global count

    state = p.get_state(HEIGHT)

    oldstate0 = state[0]
    
    match(state[row + 1], state[row + 2]):        
        case (0, 1) | (1, 0):
            # either 1 0 or 0 1 (if row<L)
            if (col < LENGTH - 1):
                power = 1
                state[row + 1], state[row + 2] = 1, 0
                update_state(HEIGHT, power, p, state)
            if (row < HEIGHT - 1):
                power = 1
                state[row + 1], state[row + 2] = 0, 1
                if (row == HEIGHT - 2 and ((oldstate0 == 0) or (oldstate0 == 1))):
                    state[0] += 2
                update_state(HEIGHT, power, p, state)

        case (0, 2) | (2, 0):
            # either 2 0 or 0 2 (if row<L)
            if (col < LENGTH - 1):
                power = 1
                state[row + 1], state[row + 2] = 2, 0
                update_state(HEIGHT, power, p, state)
            if (row < HEIGHT - 1):
                power = 1
                state[row + 1], state[row + 2] = 0, 2
                if (row == HEIGHT - 2 and ((oldstate0 == 0) or (oldstate0 == 1))):
                    state[0] += 2
                update_state(HEIGHT, power, p, state)

        case (2, 2):
            # 0 0, relabel
            # change the first unpaired 1, working downward
            power = 0
            state[row + 1], state[row + 2] = 0, 0
            ncount = 0
            for i in range(row + 3, HEIGHT + 2):
                ncount += 1 if (state[i] == 2) else -1 if (state[i] == 1) else 0
                if (ncount < 0):
                    state[i] = 2
                    break
            update_state(HEIGHT, power, p, state)

        case (1, 1):
            # 0 0, relabel
            # change the first unpaired 2, working upward
            power = 0
            state[row + 1], state[row + 2] = 0, 0
            ncount = 0
            for i in range(row, 0, -1):
                ncount += 1 if (state[i] == 1) else -1 if (state[i] == 2) else 0
                if (ncount < 0):
                    state[i] = 1
                    break
            update_state(HEIGHT, power, p, state)

        case (0, 0):
            # either 2 1 (if row<L) or 0 0
            # 0 0
            power = 0
            update_state(HEIGHT, power, p, state)
            # 2 1
            if((row < HEIGHT - 1) and (col < LENGTH - 1)):
                if (row == 0 and ((oldstate0 == 0) or (oldstate0 == 2))):
                    state[0] += 1
                if (row == HEIGHT - 2 and ((oldstate0 == 0) or (oldstate0 == 1))):
                    state[0] += 2
                power = 2
                state[row + 1], state[row + 2] = 2, 1
                update_state(HEIGHT, power, p, state)

            # power = 0
            # state[row + 1], state[row + 2] = 0, 0
            # update_state(HEIGHT, power, p, state)

        case (1, 2):
            # 0 0
            power = 0
            state[row + 1], state[row + 2] = 0, 0
            update_state(HEIGHT, power, p, state)

        case (2, 1):
            if (state[0] == 3 and len([i for i in state[1:] if i > 0]) <= 2):
                for i in range(0, min(len(p.coeff), _MAX_POWER_)):
                    count[col][i] += p.coeff[i]
                

def main():

    global count, new_states_hash

    real_total_count = get_real_total_count("flm3-results.json")

    total_count = {i: 0 for i in range(_MAX_POWER_)}

    print("starting program\n")

    begin_time = time.perf_counter()

    for HEIGHT in range(2, _MAX_HEIGHT_ + 1):
        start_time = time.perf_counter()
        LENGTH = 2 * _MAX_HEIGHT_ - HEIGHT + 2
        print(f"starting L={HEIGHT} M={LENGTH}")

        for length in range(HEIGHT, LENGTH):
            count[length - 1] = [0] * (_MAX_POWER_ + 2)
        
        states_hash = { 0 : State(index=0, coeff=[1]) }

        for col in range(LENGTH):            
            for row in range(HEIGHT):
                for p in states_hash.values():
                    add_site(p, row, col, HEIGHT, LENGTH)
                states_hash, new_states_hash = new_states_hash, {}
            if col == 0:
                # Remove the state with index=0
                states_hash.pop(0, None)
            for p in states_hash.values():
                state = p.get_state(HEIGHT)
                state.insert(1, 0)
                p.index = state_to_index(HEIGHT, state)
            states_hash = {s.index: s for s in states_hash.values()}
            
            # # DEBUG
            # states_count = len(states_hash)
            # print(f"col {col} L={HEIGHT} M={LENGTH} states count: {states_count} = {states_count ** (1 / (HEIGHT))} ^ {HEIGHT} = {states_count ** (1 / (HEIGHT + 2))} ^ {HEIGHT + 2}", end=" ")
            # if states_count > 0:    
            #     max_key = max(states_hash.keys())
            #     min_key = min(states_hash.keys())
            #     print(f"min_key={min_key}={states_hash[min_key].get_state(HEIGHT)} max_key={max_key}={states_hash[max_key].get_state(HEIGHT)}")


        for length in range(HEIGHT, LENGTH):
            weight = 1 if HEIGHT == length else 2
            for i in range(_MAX_POWER_):
                total_count[i] += weight * count[length - 1][i]

        for i in real_total_count[HEIGHT].keys():
            assert total_count[i] == real_total_count[HEIGHT][i]

        for i in range(_MAX_POWER_):
            if total_count[i] > 0:
                print(f"n={i}   SAR = {total_count[i]}")

        end_time = time.perf_counter()
        print(f"finished L={HEIGHT} M={LENGTH} in {end_time - start_time} seconds, total time: {end_time - begin_time}")

    for i in range(_MAX_POWER_):
        if total_count[i] > 0:
            print(f"n={i}   SAR = {total_count[i]}")



if __name__ == "__main__":
    main()
