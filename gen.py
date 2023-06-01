import os
import subprocess as sp
from sys import argv
import hashlib

key = ''

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
        file = str(file)
        path = f'{dir}/{file}'
        fprint(file)
        if file.endswith('.integrity'):
            os.remove(file)
            fprint(f'Deleted already existing integrity file. [{file}]')
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

def gen(path:str,secret_key:str,silent=True):
    global key,q
    key = secret_key
    q = silent
    
    os.chdir(path)
    write = hash_files(path)

    key = shash(''.join(write))

    write.insert(0,f'KEY={key}\n')

    with open('file.integrity', 'w+') as file:
        file.writelines(write)
    return 'Generated.'

if __name__ == '__main__': gen(argv[1],silent=False)
