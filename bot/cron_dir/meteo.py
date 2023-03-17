#!/usr/bin/env python3
def mid_sum(weights, l, r, mid):
    sum_l = sum([weights[x] for x in range(l, mid)])
    sum_r = sum([weights[x] for x in range(mid, r)])
    print(sum_l, sum_r)
    if sum_l > sum_r:
        k = -1
    else:
        k = 1
    min, max = sorted([sum_l, sum_r])

    while l <= mid < r-1 and max > min:
        max -= weights[mid]
        min += weights[mid]
        mid += k

    print(mid, min, max)

if __name__ == "__main__":
    l, r = 0, 6
    mid_sum([3,2,2,4,1,4], l, r, (l+r)//2)
