def median_of_3(a, b, c):
    if a > b:
        if b > c:
            return 1, b
        elif c > a:
            return 0, a
        else:
            return 2, c
    else:
        if b < c:
            return 1, b
        elif c < a:
            return 0, a
        else:
            return 2, c


def swap_pivot(array, from_ix, to_ix, pivot_type='first'):
    if pivot_type == 'first':
        pass
    elif pivot_type == 'last':
        array[from_ix], array[to_ix] = array[to_ix], array[from_ix]
    elif pivot_type == 'median':
        size = to_ix - from_ix + 1
        half_ix = ((size // 2 - 1) if size % 2 == 0 else (size // 2)) + from_ix
        first, half, last = array[from_ix], array[half_ix], array[to_ix]
        ixs = [from_ix, half_ix, to_ix]
        med_ix = ixs[median_of_3(first, half, last)[0]]
        array[from_ix], array[med_ix] = array[med_ix], array[from_ix]
    else:
        raise NotImplementedError
    return array[from_ix]

def quicksort(array, from_ix=None, to_ix=None, pivot_type='first'):

    comps = 0
    from_ix = from_ix if from_ix is not None else 0
    to_ix = to_ix if to_ix is not None else len(array) - 1

    size = to_ix - from_ix + 1

    if size < 2:
        return comps
    elif size == 2:
        if array[from_ix] > array[to_ix]:
            array[from_ix], array[to_ix] = array[to_ix], array[from_ix]
        comps += size - 1
    else:
        comps += size - 1
        pivot = swap_pivot(array, from_ix, to_ix, pivot_type=pivot_type)
        pivot_ix = from_ix

        j = from_ix
        for i in range(from_ix, to_ix + 1):
            if i == pivot_ix:
                j += 1
            elif array[i] < pivot:
                array[i], array[j] = array[j], array[i]
                j += 1

        array[j - 1], array[pivot_ix] = array[pivot_ix], array[j - 1]

        comps_1 = quicksort(array, from_ix=from_ix, to_ix=j-2, pivot_type=pivot_type)
        comps_2 = quicksort(array, from_ix=j, to_ix=to_ix, pivot_type=pivot_type)
        comps = comps + comps_1 + comps_2

    return comps


if __name__ == "__main__":
    import os
    import random
    import sys

    import numpy as np

    N = 11
    try:
        filepath = sys.argv[1]
        integers = np.genfromtxt(filepath, dtype=int)
        N = len(integers) + 1
    except:
        integers = np.arange(1, N)
        np.random.shuffle(integers)

    print(integers)
    comps = quicksort(integers, pivot_type='median')
    print("COMPARISONS:", comps)
    print(all(np.array(integers) == np.arange(1, N)))



    



