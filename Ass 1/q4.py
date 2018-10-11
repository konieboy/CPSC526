def some_hash(val):
    retval = [0x0f, 0xff, 0x00]

    for i in val: # Loop for each char in string
        print (retval)

        n = ord(i) # get unicode representation
        #print (n, i)    

        retval[0] ^= n  #Xor
        retval[1] &= n  #And
        retval[2] |= n  #or
        print (bin(n), retval)

    #return '' + chr(retval[0] ^ 0x0f) + chr(retval[1]) + chr(retval[2])
    return '' + chr(retval[0]) + chr(retval[1]) + chr(retval[2])


# def unhash(val):
#     retval = [0x0f, 0xff, 0x00] #[00001111, 11111111, 00000000]

#     print (retval)
#     for i in val: # Loop for each char in string
#         n = ord(i) # get unicode representation
#         #print (n, i)    

#         retval[0] ^= n  #Xor
#         retval[1] &= n  #And
#         retval[2] |= n  #or
#         print (bin(n), retval)

#     return '' + chr(retval[0]) + chr(retval[1]) + chr(retval[2])



# print (x)

# x = some_hash("2yy")

# print (x)

# x = some_hash("AAA")
# print (x)

# x = some_hash("BBB")
# print (x)

x = some_hash("BBB")
print (x)

x = some_hash("DBB")
print (x)
#

# z = unhash(x)
# print (z)

# y = some_hash("123")
# print (y)

# if (x == y):
#     print ("Hashes are identical")
# else:
#     print ("Hashes are diffierent")