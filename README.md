# Simple_encrypt_import
#### Purpose: hide some code by encrypting it. It not save you from debuging but it more secre put it on open repositories.

## How to use it:
### encryption
- function **AES.block_size** to encrypt file with code
- save module **encrypt_module.py** with password in secure place

### decryption
- put secret.py inside code (rename if needed)
- ``import secret`` inside code
- it requests password, if it's correct, then objects available
for example ``secret.test1``
- for **IDE** inside secret put link on object
for example  ``test1 = test1``

#### **.pye* file structure
1. in 'Q' structure file size
> the function saves the original file size in the first 8 bytes of the output file (more precisely, the first sizeof(long long) bytes)
2. The initialization vector.
> Randomly generates a 16-byte IV
3. 32 byte SHA256 checksum of cleare data. Needed to check key during decryption.
And raise **ValueError** if it wrong (stop main program)
4. encrypted data
5. last chink fulfilled with spaces


