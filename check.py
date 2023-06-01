import os
import subprocess as sp
from sys import argv
import hashlib
import time as t

start = t.time()

ur_private_secret_key = argv[2]

os.chdir(argv[1])

intact = True

key_intact = True

modified = []

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
            print(f'Skipping integrity file')
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

key = shash(''.join(write)+'\n')

write.insert(0,f'KEY={key}\n')


with open('file.integrity', 'r') as file:
    lines = file.readlines()
    keyhash = lines[0].split('=')[1]
    lines[0] = ''
    truehash = shash(''.join(lines))
    comp = f'{keyhash=}, {truehash=}, {"".join(lines)=}\n'
    if keyhash != truehash:
        intact = False
        key_intact = False
        print(f'KEYFILE NOT INTACT!!!')
        modified.append('file.integrity')
    for i,line in enumerate(lines):
        if i == 0: continue
        file = line.split('=')[0]
        hash = line.split('=')[1]
        print(f'Checking {file}')
        if hash == write[i].split('=')[1] and key_intact:
            print('File intect!\n')
            continue
        else:
            intact = False
            print('File MODIFIED!')
            print(f'{hash=}, {write[i]=}')
            modified.append(file)
            

time = round(t.time() - start,4)

print('\n'*50)
print(f'------------------------------------')
print(f'|{f"Operation competed! Time: {time}":^34}|')
print(f'|{f"Checked files: {len(write)}":^34}|')
print(f'|{f"All files intact: {intact}":^34}|')
print(f'|{f"Modified files: {len(modified)}":^34}|')
print(f'------------------------------------\n')

if not key_intact:
    print('KEYFILE is not intact. All files can be modified. \nThis means that either the file has been modified or you have typed your password incorrectly.')

print(comp)

if len(modified) != 0:
    if input('\nType "view" to view modified files. Press enter to exit.\n') == 'view':
        print('Modified files:')
        for i in modified:
            if i == 'file.integrity':
                i = 'file.integrity (KEYFILE)'
            print(i)
