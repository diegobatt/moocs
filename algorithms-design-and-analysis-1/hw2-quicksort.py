"""WIP"""
def choose_pivot(array, type='first'):
    if type == 'first':
        return 0
    elif type == 'last':
        return -1
    else:
        raise NotImplementedError

def quicksort(array, pivot_type='first'):

    n = len(array)

    if n == 1:
        return array
    elif n == 2
        if array[0] > array[1]:
            return array[::-1]
        else:
            return array
    
    pivot_ix = choose_pivot(array, type=pivot_type)
    pivot = array[pivot_ix]

    i, j = 1, 1
    while j < n:
        if array[j] < pivot:
            array[i], array[j] = array[j], array[i]
            i += 1
            j += 1
        else:
            j += 1
    array[pivot_ix]
    



