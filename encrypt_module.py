from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
import hashlib, random, struct
import os, sys
import importlib

password = 'kitty'.encode()
key = hashlib.sha256(password).digest()

def encrypt_file(key, in_file, out_file=None, chunksize=64*1024):
    if not out_file:
        out_file = os.path.splitext(in_file)[0] + '.pye'

    iv = bytes((random.randint(0, 0xFF)) for i in range(16))
    # iv2 = 16 * '\x00' # this is a grave mistake.
    iv3 = Random.new().read( AES.block_size )
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_file)
    with open(in_file, 'rb') as infile:
        data = infile.read()
        check_sum = SHA256.new(data).digest()
    with open(in_file, 'rb') as infile:
        with open(out_file, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            outfile.write(check_sum)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    # chunk += (' ' * (AES.block_size - (len(chunk) % AES.block_size))).encode('utf-8')
                    chunk += (' ' * (16 - (len(chunk) % 16))).encode('utf-8')
                outfile.write(encryptor.encrypt(chunk))

def deccryp_file(key, in_file, out_file=None, chunksize=64*1024):
    if not out_file:
        out_file = os.path.splitext(in_file)[0]

    with open(in_file, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(origsize)

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


class StringImporter(object):
# http://stackoverflow.com/questions/14191900/pythonimport-module-from-memory
   def __init__(self, modules):
       self._modules = dict(modules)


   def find_module(self, fullname, path):
      if fullname in self._modules.keys():
         return self
      return None

   def load_module(self, fullname):
      if not fullname in self._modules.keys():
         raise ImportError(fullname)

      new_module = importlib.import_module(fullname)
      exec(self._modules[fullname], new_module.__dict__)
      return new_module

if __name__ == '__main__':
    encrypt_file(key, 'test_module.py')
    deccryp_file(key, 'test_module.pye')
    exec(decrypt_file_in_mem(key, 'test_module.pye'))
    # modules = {'decr' : decrypt_file_in_mem(key, 'test_module.pye')}
    # sys.meta_path.append(StringImporter(modules))
    # from decr import test1
    # my_module = importlib.
    # a = test1()
    # print(a)




