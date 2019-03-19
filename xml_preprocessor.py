import sys
import re
from math import *

def main():
    if len(sys.argv) != 3:
        print('Wrong arguments: first argument must be path to input XML!')
        print('Wrong arguments: second argument must be output path for XML!')
        return

    in_path = sys.argv[1]
    out_path = sys.argv[2]
    
    f = open(in_path, 'r')
    data = f.read()
    f.close()
    
    r_exec = r'\$\{([^\}]*)\}'
    r_eval = r'\$\(([^\)]*)\)'
    
    while True:
        search = re.search(r_exec, data)
        if search == None:
            break
        exec(search.group(1))
        data = re.sub(r_exec, '', data, 1)
    
    while True:
        search = re.search(r_eval, data)
        if search == None:
            break
        data = re.sub(r_eval, str(eval(search.group(1))), data, 1)
    
    f = open(out_path, 'w')
    f.write(data)
   
if __name__ == '__main__':
    main()
