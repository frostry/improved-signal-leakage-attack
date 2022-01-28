def likeliest_abs_secret_from_signals_count(f, sig, sigma):
    curr = 0
    count = 0
    for i in range(len(f)-1):
        if f[i] != curr: #and f[i+1] == f[i]:
            count += 1
            curr = f[i]
    if curr != 0:
        count += 1
    return count // 2
#a = [0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1]

#print(likeliest_abs_secret_from_signals_count(a, 1, 1))
