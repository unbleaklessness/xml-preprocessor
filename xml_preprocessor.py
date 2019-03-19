import xml.etree.ElementTree as ET
import sys
import re

TAG_NAME = 'variable'
NAME_ATTRIBUTE = 'name'
VALUE_ATTRIBUTE = 'value'

variables = dict()

def is_variable_element(element):
    return element.tag == TAG_NAME and NAME_ATTRIBUTE in element.attrib and VALUE_ATTRIBUTE in element.attrib

def add_to_variables(variables, element):
    variables[element.attrib[NAME_ATTRIBUTE]] = element.attrib[VALUE_ATTRIBUTE]

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
    for child in reversed(root):
        if is_variable_element(child):
            add_to_variables(variables, child)
            root.remove(child)

    # Substitude variables:
    for element in root.iter():
        for key, value in element.attrib.items():
            new_value = value
            for v_key, v_value in variables.items():
                new_value = re.sub(r'\$\{(?:%s)\}' % v_key, v_value, new_value)
            element.set(key, new_value)

    tree.write(out_path)

if __name__ == '__main__':
    main()
