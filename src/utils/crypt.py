alfabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
number = ['0','1','2','3','4','5','6','7','8','9']
extend = alfabet + number
move = 1

def forEncrypt(string):
    encodeString = ""
    for x in range(len(string)):
        tempString = extend.index(string[x]) + move
        encodeString = encodeString + extend[tempString % len(extend)]
    return encodeString

def forDecrypt(string):

    decodeString = ""
    for x in range(len(string)):
        tempString = extend.index(string[x]) - move
        decodeString = decodeString + extend[tempString % len(extend)]

    return decodeString        
