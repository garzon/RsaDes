from rsa import *
import requests, json, random, string, os

def put_contents(path, content):
    f = open(path, 'wb')
    f.write(content)
    f.close()

domain = 'http://garzon.science/RsaDes'

# step 1: recv the public key of server
recv = json.loads(requests.get(domain + '/rsa_des_server.php?step=1').text)
server_e = int(recv['e'])
server_n = int(recv['n'])
print 'step 1: server public key received - e: %d, n: %d' % (server_e, server_n)

print '------------------------'
# step 2: generate des key, encrypt it and send it to the server
des_key = ''.join([chr(random.randint(1, 255)) for x in xrange(8)])

print 'step 2: des key generated, hex encoded: %s' % des_key.encode('hex')

# save the des key for calling php des code
put_contents('/tmp/my_des_key.txt', des_key)

cipher = encrypt(des_key, server_e, server_n)
if requests.post(domain + '/rsa_des_server.php?step=2', data={'des_key': cipher}).text != 'success':
    raise RuntimeError, 'something wrong'
print 'step 2: encrypted des key sent'

print '------------------------'
# step 3: using des to encrypt the content of the communication
content = str(random.randint(10000, 99999)) # simulate the content of communication
print 'step 3: the plaintext of the communication is %s' % content
put_contents('/tmp/my_des_plaintext.txt', content)
os.system('php des_encrypt.php') # calling the php code to use the des encryption
cipher = open('/tmp/my_des_encrypt_result.txt', 'rb').read()
recv = requests.post(domain + '/rsa_des_server.php?step=3', data={'cipher': cipher}).text
print 'step 3: recv the response of the server(hex_encoded): %s' % recv.encode('hex')
put_contents('/tmp/my_des_cipher.txt', recv)
os.system('php des_decrypt.php') # calling the php code to use the des decryption
result = open('/tmp/my_des_decrypt_result.txt', 'rb').read()
print 'step 3: the plaintext of the response is %s (should be %s+1)' % (result, content)

print 'test end.'
