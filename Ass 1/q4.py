def some_hash(val):
    retval = [0x0f, 0xff, 0x00]
    for i in val:
        n = ord(i)
        retval[0] ^= n
        retval[1] &= n
        retval[2] |= n
        print bin(n), retval
    return '' + chr(retval[0]) + chr(retval[1]) + chr(retval[2])

x = some_hash("123")
print (x)

x = some_hash("123123123")
print (x)