def some_hash(val):
    retval = [0x0f, 0xff, 0x00]
    retvalI = [0x0f, 0xff, 0x00]

    for i in val: # Loop for each char in string
        print (retval)

        n = ord(i) # get unicode representation
        #print (n, i)    

        retval[0] ^= n     
        retval[1] &= n
        retval[2] |= n
        print (bin(n), retval)

    return '' + chr(retval[0]) + chr(retval[1]) + chr(retval[2])

x = some_hash("a2dfasdfasf")
print (x)


y = some_hash("asdfasdfasf")
print (y)

if (x == y):
    print ("Hashes are identical bro")