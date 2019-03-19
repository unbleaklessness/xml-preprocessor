import xml.etree.ElementTree as ET
import sys
import re
from math import *

TAG_NAME = 'variable'
NAME_ATTRIBUTE = 'name'
VALUE_ATTRIBUTE = 'value'

def is_variable_element(element):
    return element.tag == TAG_NAME and NAME_ATTRIBUTE in element.attrib and VALUE_ATTRIBUTE in element.attrib

def pair_from_variable_element(element):
    return (element.attrib[NAME_ATTRIBUTE], eval(element.attrib[VALUE_ATTRIBUTE]))

def substitude_pair(pair, root):
    v_key, v_value = pair

    for element in root.iter():
        for key, value in element.attrib.items():
            new_value = re.sub(r'\$\{.*(?:%s)[^\}]*\}' % v_key, str(v_value), value)
            element.set(key, new_value)

def main():
    if len(sys.argv) != 3:
        print('Wrong arguments: first argument must be path to input XML!')
        print('Wrong arguments: second argument must be output path for XML!')
        return

    in_path = sys.argv[1]
    out_path = sys.argv[2]
    
    tree = ET.parse(in_path)
    root = tree.getroot()

    # Get variables:
    for child in list(root):
        if is_variable_element(child):
            pair = pair_from_variable_element(child)
            root.remove(child)
            substitude_pair(pair, root)

    tree.write(out_path)

if __name__ == '__main__':
    main()
