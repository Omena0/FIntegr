import os
import subprocess as sp
from sys import argv
import hashlib
import time as t

start = t.time()

key = ''

modified = []

def fprint(text):
    global q
    if q: return
    print(text)

def shash(text):
    try: text = text.encode()
    except: pass
    return int(hashlib.sha256(text).hexdigest()[:16], 16)-2**63

def hash_files(dir):
    files = os.listdir(dir)
    write = []
    for file in files:
        path = f'{dir}/{file}'
        fprint(file)
        if file.endswith('.integrity'):
            fprint(f'Skipping integrity file')
            continue
        # Skip configuration files
        if file.endswith(('.config','.conf','.yaml','.properties','.json','.ini','.toml','.xml')): continue
        if file.count('.') == 0:
            fprint('Folder detected! looping in folder..')
            write.extend(hash_files(path))
        fprint(path)
        try: content = open(path,'rb').read()
        except PermissionError:
            fprint('Permission denied! Continuing...')
            continue
        hashed = shash(content)
        line = f'{file}={hashed}\n'
        write.append(line)
    return write


def check(path:str,secret_key:str,silent=True):
    global write, key, key_intact, intact,q
    key = secret_key
    q = silent
    
    intact = True

    key_intact = True
    
    os.chdir(path)

    write = hash_files(path)

    key = shash(''.join(write)+'\n')

    write.insert(0,f'KEY={key}\n')

    with open('file.integrity', 'r') as file:
        lines = file.readlines()
        keyhash = int(lines[0].split('=')[1].replace('\n', ''))
        lines[0] = ''
        truehash = shash(''.join(lines))
        comp = f'{keyhash=}, {truehash=}'
        if keyhash != truehash:
            intact = False
            key_intact = False
            fprint(f'KEYFILE NOT INTACT!!!')
            modified.append('file.integrity')
        for i,line in enumerate(lines):
            if i == 0: continue
            file = line.split('=')[0]
            hash = line.split('=')[1]
            fprint(f'Checking {file}')
            if hash == write[i].split('=')[1] and key_intact:
                fprint('File intect!\n')
                continue
            else:
                intact = False
                fprint('File MODIFIED!')
                fprint(f'{hash=}, {write[i]=}')
                modified.append(file)
                
    return intact

if __name__ == '__main__':
    
    intact = check(argv[1],silent=False)

    time = round(t.time() - start,4)

    fprint('\n'*50)
    fprint(f'------------------------------------')
    fprint(f'|{f"Operation competed! Time: {time}":^34}|')
    fprint(f'|{f"Checked files: {len(write)}":^34}|')
    fprint(f'|{f"All files intact: {intact}":^34}|')
    fprint(f'|{f"Modified files: {len(modified)}":^34}|')
    fprint(f'------------------------------------\n')

    if not key_intact:
        fprint('KEYFILE is not intact. All files can be modified. \nThis means that either the file has been modified or you have typed your password incorrectly.')

    if len(modified) != 0:
        if input('\nType "view" to view modified files. Press enter to exit.\n') == 'view':
            fprint('Modified files:')
            for i in modified:
                if i == 'file.integrity':
                    i = 'file.integrity (KEYFILE)'
                fprint(i)
