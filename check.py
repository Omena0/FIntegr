import os
import subprocess as sp
from sys import argv

ur_private_secret_key = argv[2]

files = os.listdir(argv[1])

os.chdir(argv[1])

contents = []

intact = True

def shash(text,seed:str=598225):
    seed = str(seed)
    if len(seed) > 9:
        seed = str(round(int(seed) / (10 * len(seed)-8)))
    text = text.replace('\n','\\n')
    cmd = ['python', '-c', f'print(hash("{text}"),end="")']
    p = sp.Popen(cmd, env={'PYTHONHASHSEED': seed},text=True,stdout=sp.PIPE)
    return p.communicate()[0]

for file in files:
    if file.endswith('.FIntegr') or file.endswith('.integrity'):
        try:
            config
        except: pass
        else:
            print('DOUBLE CONFIG DETECTED')
            intact = False
            break
        config = open(file,'r').readlines()
        config[0] = ''
        config = ''.join(config)
        key = open(file,'r').readlines()[0]
        config.replace(key,'')
        key = key.split('=')
        if key[0] != 'KEY':
            print('Invalid integrity file!')
            intact = False
            break
        key = key[1]
    else:
        contents.append(open(file,'r').read())

keyhash = shash(ur_private_secret_key+config)
if key.replace('\n','') != keyhash:
    print('INTEGRITY FILE NOT INTACT!!!')
    print(keyhash)
    intact = False

for i in contents:
    hashed = str(shash(i))
    print(f'{hashed=}')
    if hashed+'\n' in config:
        continue
    else:
        intact = False
        break


if intact:
    print('FILES INTACT!!!')
else:
    print('FILES NOT INTACT!!!')

