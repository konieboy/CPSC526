# CPSC526 Assignment 2
Coded in python 3.7 on Windows

## Intalling Libraries
- Install PyCryptodome for AES encryption (pip install PyCryptodome)
- install argon2_cffi -> used for hashing in argon2 (pip install argon2_cffi) https://pypi.org/project/argon2_cffi/

## Usage
- python .\enroll [username] [password]
- python .\authenticate [username] [password]

### Notes
- argon2_cffi implements salting by default
- PyCryptodome used for AES with CBC mode on
- The encrypted database already has some test data (ie. username = amanda, password = duckie)