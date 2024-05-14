def create_dict():
    d = {}
    iter = 0
    for i in range(0,127):
        d[iter] = chr(i)
        iter = iter +1
    return d

def encode_val(val):
    list_code = []
    lent = len(val)
   
    d = create_dict() # получаем словарь кода
    
    for w in range(lent):
        for value in d:
            if val[w] == d[value]:
               list_code.append(value) 
    return list_code

def comparator(value, key):
    len_key = len(key)
    dic = {}
    iter = 0
    full = 0
    for i in value:
        dic[full] = [i,key[iter]]
        full = full + 1
        iter = iter +1
        if (iter >= len_key):
            iter = 0 
 
    return dic  

def encode(value_encoded, key_encoded):
    dic = comparator(value_encoded, key_encoded)
  
    lis = []
    d = create_dict()
 
    for v in dic:
        go = (dic[v][0]+dic[v][1]) % len(d)
        lis.append(go) 
    return lis

def EncodeText(text ,key):
    key_encoded = encode_val(key)
    value_encoded = encode_val(text)
    shifre = encode(value_encoded, key_encoded)
    print(shifre)
    shifreStr = ''.join(decode_val(shifre))
    return shifreStr, shifre


def full_decode(value, key):
    dic = comparator(value, key)
    d = create_dict() 
    lis =[]
    for v in dic:
        go = (dic[v][0]-dic[v][1]+len(d)) % len(d)
        lis.append(go) 
    return lis

def decode_val(list_in):
    list_code = []
    lent = len(list_in)
    d = create_dict() 
    
    for i in range(lent):
        for value in d:
            if list_in[i] == value:
               list_code.append(d[value]) 
    return list_code
 

def DecodeText(text, key):
    key_encoded = encode_val(key)
    decoded = full_decode(text, key_encoded)
    decoded_word = decode_val(decoded)
    return ''.join(decoded_word)