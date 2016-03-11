from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import hashlib, random, struct, types, sys

file_with_code = 'test_module.pye'
password = input('please enter password:').encode()
key = hashlib.sha256(password).digest()

def decrypt_file_in_mem(key, in_file, chunksize=64*1024):
    with open(in_file, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        check_sum = infile.read(32)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        out_data = bytes()
        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            out_data += decryptor.decrypt(chunk)
        check_sum1 = SHA256.new(out_data[:origsize]).digest()
        if check_sum1 == check_sum:
            return out_data[:origsize].decode('utf-8')
        else:
            raise ValueError('integrity error')


code = decrypt_file_in_mem(key, file_with_code) # now it in memory, and availbale for !!!debuger!!!
code = compile(code, '<string>', mode='exec')
current_module = sys.modules[__name__]
exec(code, current_module.__dict__)
# it's beteter to make link on real functions
# test1 = test1

if __name__ == '__main__':
    file_with_code = 'test_module.pye'
    code = decrypt_file_in_mem(key, file_with_code) # now it in memory, and availbale for !!!debuger!!!
    code = compile(code, '<string>', mode='exec')
    current_module = sys.modules[__name__]
    exec(code, current_module.__dict__)
    assert 'test1' in dir(current_module), 'missing test1 function'
    assert 'test2' in dir(current_module), 'missing test2 function'


