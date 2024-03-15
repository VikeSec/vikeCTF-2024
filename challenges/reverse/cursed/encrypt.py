flag = "vikeCTF{1MMUT4BL3_L4M3DA_M0NAD5}"


def shift(k, l):
    return [i + k for i in l]


def rotate(k, l):
    dist = len(l) - (k % len(l))
    return l[dist:] + l[:dist]


def swap(l):
    result = []
    for i in range(0, len(l) - 1, 2):
        result += [l[i + 1], l[i]]

    if len(l) % 2 == 1:
        result.append(l[-1])

    return result


a = [ord(c) for c in flag]

a = shift(-13, a)
a = swap(a)
a = rotate(5, a)
a = swap(a)
a = rotate(3, a)
a = shift(50, a)

print(a)
