# . Write a Python program to get a list, sorted in increasing order by the last
# element in each tuple from a given list of non-empty tuples.
# Sample List : [(2, 5), (1, 2), (4, 4), (2, 3), (2, 1)]
# Expected Result : [(2, 1), (1, 2), (2, 3), (4, 4), (2, 5)]


# lst.sort(key=lambda item: item[1])
#
# print(lst)

lst = [(2, 5), (1, 2), (4, 4), (2, 3), (2, 1), (2, 1)]

result = []

for i in range(len(lst)):
    min_item = lst[0]
    for item in lst:
        if item[1] < min_item[1]:
            min_item = item
    result.append(min_item)
    lst.remove(min_item)
print(result)
