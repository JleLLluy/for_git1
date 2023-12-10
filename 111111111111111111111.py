stolb = int(input())
strok = int(input())
data = [int(x) for x in input().split(" ") i]
for i in range(len(data)):
    if data[i] == "false":
        data[i] = 0
    else:
        data[i] = 1


for i in range(stolb):
    for j in range(strok):
        above = (data[(i - 1) * strok + j] if i - 1 >= 0 else 0)
        below = (data[(i + 1) * strok + j] if (i + 1) <= stolb - 1 else 0)
        right = (data[i * strok + j + 1] if j + 1 <= strok - 1 else 0)
        left = (data[i * strok + j - 1] if j - 1 >= 0 else 0)
        right_above = (data[(i - 1) * strok + j + 1] if j + 1 <= strok - 1 and i - 1 >= 0 else 0)
        right_below = (data[(i + 1) * strok + j + 1] if j + 1 <= strok - 1 and (i + 1) <= stolb - 1 else 0)
        left_above = (data[(i - 1) * strok + j - 1] if j - 1 >= 0 and i - 1 >= 0 else 0)
        left_below = (data[(i + 1) * strok + j - 1] if j - 1 >= 0 and (i + 1) <= stolb - 1 else 0)
        print(above + below + right + left + right_above + right_below + left_below + left_above, end=" ")
    print()
