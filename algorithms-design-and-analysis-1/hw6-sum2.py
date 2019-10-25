import progressbar


def sum2(nums, targets):
    count = 0
    values = []
    for t in progressbar.progressbar(targets):
        for n in nums:
            query = t - n
            if query == n:
                pass
            elif query in nums:
                count += 1
                values.append((n, query, t))
                break
            else:
                pass
    return count, values


if __name__ == '__main__':
    import csv
    import sys

    try:
        filepath = sys.argv[1]
        nums = set()
        with open(filepath) as f: 
            csv_reader = csv.reader(f, delimiter='\t')
            for row in csv_reader:
                nums.add(int(row[0]))

    except:
        nums = set([1, 2, 3 ,5 ,8 ,13])

targets = range(-10000,10001)
count, values = sum2(nums, targets)
print(count, values)

