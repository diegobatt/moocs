import heapq

def online_median(array):
    inf = [-min(array[0], array[1])]
    sup = [max(array[0], array[1])]
    medians = [array[0], -inf[0]]

    for x in array[2:]:
    
        if -inf[0] >= x:
            heapq.heappush(inf, -x)
        elif sup[0] <= x:
            heapq.heappush(sup, x)
        else:
            heapq.heappush(inf, -x)

        while abs(len(inf) - len(sup)) > 1:
            if len(inf) > len(sup):
                aux = heapq.heappop(inf)
                heapq.heappush(sup, -aux)
            else:
                aux = heapq.heappop(sup)
                heapq.heappush(inf, -aux)

        if len(sup) > len(inf):
            medians.append(sup[0])
        else:
            medians.append(-inf[0])
        
    return medians


if __name__ == '__main__':
    import csv
    import sys

    try:
        filepath = sys.argv[1]
        nums = []
        with open(filepath) as f: 
            csv_reader = csv.reader(f, delimiter='\t')
            for row in csv_reader:
                nums.append(int(row[0]))

    except:
        nums = [5, 4, 6, 3, 2, 1]

medians = online_median(nums)
print(medians)
print(sum(medians), sum(medians) % 10000)
