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
        print('Integrity file already exists! Deleted.')
        os.remove(file)
    else:
        contents.append(open(file,'r').read())

# Gen hashes
hashes = []

config = open('file.integrity','a+')
for i in contents:
    hashed = str(shash(i))
    print(f'{hashed=}')
    hashes.append(hashed+'\n')
    
config.close()


config = open('file.integrity','w')

key = shash(ur_private_secret_key+''.join(hashes))

write = []
write.append(f'KEY={key}\n')

for i in hashes:
    write.append(i)


config.writelines(write)


