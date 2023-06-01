import os
import subprocess as sp
from sys import argv
import hashlib

ur_private_secret_key = argv[2]

os.chdir(argv[1])

def shash(text):
    try: text = text.encode()
    except: pass
    return int(hashlib.sha256(text).hexdigest()[:16], 16)-2**63

def hash_files(dir):
    files = os.listdir(dir)
    write = []
    for file in files:
        path = f'{dir}/{file}'
        print(file)
        if file.endswith('.integrity'):
            os.remove(file)
            print(f'Deleted already existing integrity file. [{file}]')
            continue
        if file.count('.') == 0:
            print('Folder detected! looping in folder..')
            write.extend(hash_files(path))
        print(path)
        try: content = open(path,'rb').read()
        except PermissionError:
            print('Permission denied! Continuing...')
            continue
        hashed = shash(content)
        line = f'{file}={hashed}\n'
        write.append(line)
    return write

write = hash_files(argv[1])

key = shash(''.join(write))

a = ''.join(write)

print(f"{a=}")

write.insert(0,f'KEY={key}\n')

with open('file.integrity', 'w+') as file:
    file.writelines(write)

