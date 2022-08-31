# -*- coding: utf-8 -*-

import argparse
import encodings
import os
import shutil
import datetime as at
import json
import csv
from jinja2 import Template,Environment,FileSystemLoader

COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_YELLOW = '\033[33m'
COLOR_CLEAR = '\033[0m'

def arg_parse():
    parser = argparse.ArgumentParser("Config Generator")
    parser.add_argument('template_file', help='template file')
    parser.add_argument('parameter_file', help='Parameter file')
    parser.add_argument('-a', '--append', action='store_true', help='Append mode')
    args = vars(parser.parse_args())
    return args


def is_file(a):
    return os.path.isfile(a)

def to_datetime_text():
    now = at.datetime.now()
    textNow = now.strftime('%Y%m%d%H%M%S')
    return  textNow

def save_file(render, appendMode, filename):
    OUTPUT_PATH = './output/'
    if filename == None:
        filename = str(input('What is the output file name? : '))
    output = OUTPUT_PATH + filename
    if appendMode:
        print(COLOR_GREEN + '[Info] ' + COLOR_CLEAR + 'Append mode')
        if is_file(output):
            print(COLOR_GREEN + '[Info] ' + COLOR_CLEAR + 'Append ' + output)
        else:
            print(COLOR_GREEN + '[Info] ' + COLOR_CLEAR + output + ' is not found...')
            print(COLOR_GREEN + '[Info] ' + COLOR_CLEAR + 'Generate ' + output)
        with open(output, mode='a') as f:
            f.write(render)
    else:
        if is_file(output):
            print(COLOR_GREEN + '[Info] ' + COLOR_CLEAR + output + ' is already exists.')
            BACKUP_OUTPUT_PATH = './backup/'
            backupFilename = filename + '_' + to_datetime_text()
            backupOutput = BACKUP_OUTPUT_PATH + backupFilename
            print(COLOR_GREEN + '[Info] ' + COLOR_CLEAR + 'Copy ' + output + ' to ' + backupOutput)
            shutil.copy2(output, backupOutput)
        with open(output, mode='w') as f:
            print(COLOR_GREEN + '[Info] ' + COLOR_CLEAR + 'Generate ' + output)
            f.write(render)

def generate_config(templatefilePath, parameterfilePath, mode):
    env = Environment(loader=FileSystemLoader('./', encoding="utf8"))
    template = env.get_template(templatefilePath)

    with open(parameterfilePath) as f:
        params = json.load(f)

    try:
        filename = params['filename']
    except KeyError:
        filename = None
    
    render = template.render(params)
    print('--------- start --------------')
    print(render)
    print('---------  end  --------------')
    save_file(render, mode, filename)

def main():
    args = arg_parse()
    templateFile = args['template_file']
    parameterFile = args['parameter_file']
    mode = args['append']
    if not(is_file(templateFile)):
        print(COLOR_RED + '[Error] ' + COLOR_CLEAR + 'Template file is not found...')
        exit()
    if not(is_file(parameterFile)):
        print(COLOR_RED + '[Error] ' + COLOR_CLEAR + 'Parameter file is not found...')
        exit()
    print(COLOR_YELLOW + '########## Config Generate ##########' + COLOR_CLEAR)
    generate_config(templateFile, parameterFile, mode)

    print(COLOR_YELLOW + '################ end ################' + COLOR_CLEAR)

if __name__ == "__main__":
    main()