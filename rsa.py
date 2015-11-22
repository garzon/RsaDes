def gen_128bit_prime():
    pass
    
def gen_key_pair():
    p = gen_128bit_prime()
    q = gen_128bit_prime()
    n = p*q
    r = (p-1)*(q-1)
    e = 65535
    d = e**(r-2) % r
    return (d, e, n)

def string2num(st):
    return sum([ord(b)*2**(8*i) for i, b in enumerate(st)])
    
def num2string(num):
    ret = ''
    while num>0:
        ret += chr(num&0xff)
        num = num / 256
    return ret
    
def encrypt_block(num128, public_key, n):
    return num128**public_key % n
    
def decrypt_block(num128, private_key, n):
    return num128**private_key % n
    
def encrypt(st, public_key, n):
    ret = ''
    for i in xrange(0, len(st), 16):  # 128bit(16bytes) per block
        block_string = st[i:i+16]
        block_num = string2num(block_string)
        cipher_num = encrypt_block(block_num, public_key, n)
        ret += num2string(cipher_num)
    return ret

def decrypt(st, private_key, n):
    ret = ''
    for i in xrange(0, len(st), 16):  # 128bit(16bytes) per block
        block_string = st[i:i+16]
        block_num = string2num(block_string)
        cipher_num = decrypt_block(block_num, private_key, n)
        ret += num2string(cipher_num)
    return ret

