def power_set(arr):
    ps=[[]]
    for i in arr:
        for sar in ps:
            ps = ps + [list(sar)+[i]]
    return ps

print(power_set(list(range(3))))
