# -*- coding: utf-8 -*-

import argparse
import encodings
import os
import json
import csv
from jinja2 import Template,Environment,FileSystemLoader

COLOR_RED = '\033[31m'
COLOR_YELLOW = '\033[33m'
COLOR_CLEAR = '\033[0m'

def arg_parse():
    parser = argparse.ArgumentParser("Config Generator")
    parser.add_argument('template_file', help='template file')
    parser.add_argument('parameter_file', help='Parameter file')
    args = vars(parser.parse_args())
    return args


def is_file(a):
    if not(os.path.isfile(a)):
        print(a + ' is not found...')
    return os.path.isfile(a)

def generate_config(templatefilePath, parameterfilePath):
    env = Environment(loader=FileSystemLoader('./', encoding="utf8"))
    template = env.get_template(templatefilePath)

    with open(parameterfilePath) as f:
        params = json.load(f)
    
    render = template.render(params)
    print(render)

def main():
    print(COLOR_YELLOW + '########## Config Generate ##########' + COLOR_CLEAR)
    args = arg_parse()
    templateFile = args['template_file']
    parameterFile = args['parameter_file']
    if not(is_file(templateFile)):
        print(COLOR_RED + '[Error] ' + COLOR_CLEAR + 'Template file is not found...')
        exit()
    if not(is_file(parameterFile)):
        print(COLOR_RED + '[Error] ' + COLOR_CLEAR + 'Parameter file is not found...')
        exit()

    generate_config(templateFile, parameterFile)

    print(COLOR_YELLOW + '################ end ################' + COLOR_CLEAR)

if __name__ == "__main__":
    main()