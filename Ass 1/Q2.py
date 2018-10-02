#######################################################
# Encoding Algorithm (Python)
# I assume that each block uses 256 bits
# 256 bits is a hexadecimal string with 64 characters
padding = "0000000000000000000000000000000000000000000000000000000000000000" 

message = "Some message that needs to be secret"

IV = getIV()
key = getKey()

# AES 256 so we need to pad with 256bit buffer
message = padding + message
encryptedMessage = encrypt(message, key, IV)

#######################################################
#Decoding Algorithm (Python)
key = getKey()
IV = "RandomTextThatIs64CharsSoThatTheAlgorithmStillWorksButIsPointles"

decryptedMessage = decrypt(message, key, IV)

# Ignore first padded part of message
finalMessage = decryptedMessage[64:]
#######################################################
