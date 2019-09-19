def merge(l_1, l_2):

    n_1, n_2 = len(l_1), len(l_2)
    l_sorted = []
    i, j = 0, 0
    invs = 0

    while True:
        if i < n_1 and j < n_2:
            if l_1[i] < l_2[j]:
                l_sorted.append(l_1[i])
                i += 1
            else:
                l_sorted.append(l_2[j])
                j += 1
                invs += n_1 - i
        elif i < n_1:
            l_sorted.append(l_1[i])
            i += 1
        elif j < n_2:
            l_sorted.append(l_2[j])
            j += 1
        else:
            break

    return l_sorted, invs
        

def sort_list(l):

    n = len(l)

    if n > 2:
        l_1, invs_1 = sort_list(l[:n // 2])
        l_2, invs_2 = sort_list(l[n // 2:])
        l_merged, invs = merge(l_1, l_2)

        return l_merged, invs + invs_1 + invs_2

    elif n == 2:
        if l[0] > l[1]:
            return l[::-1], 1
        else:
            return l, 0
    else:
        return l, 0

if __name__ == "__main__":
    import os
    import random
    import sys

    import numpy as np

    try:
        filepath = sys.argv[1]
        integers = np.genfromtxt(filepath)
    except:
        integers = np.arange(1, 10)[::-1]
    
    print(sort_list(integers))