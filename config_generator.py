# -*- coding: utf-8 -*-

import argparse
import encodings
import os
import shutil
import re
import datetime as at
import json
import csv
from jinja2 import Template,Environment,FileSystemLoader
from enum import Enum

COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_YELLOW = '\033[33m'
COLOR_CLEAR = '\033[0m'

class Color():
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    CLEAR = '\033[0m'

class Format(Enum):
    JSON = 1
    CSV = 2
    UNKNOWN = 3

class LoggingSeverity():
    ERROR = Color.RED + '[Error] ' + Color.CLEAR
    INFO = Color.GREEN + '[Info] ' + Color.CLEAR

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
        if is_file(output):
            print(LoggingSeverity.INFO + 'Append ' + output)
        else:
            print(LoggingSeverity.INFO + output + ' is not found...')
            print(LoggingSeverity.INFO + 'Generate ' + output)
        with open(output, mode='a') as f:
            f.write(render)
    else:
        if is_file(output):
            BACKUP_OUTPUT_PATH = './backup/'
            backupFilename = filename + '_' + to_datetime_text()
            backupOutput = BACKUP_OUTPUT_PATH + backupFilename
            msg = ' (Copy ' + output + ' to ' + backupOutput + ')'
            shutil.copy2(output, backupOutput)
        else:
            msg = ""
        with open(output, mode='w') as f:
            print(LoggingSeverity.INFO + 'Generate ' + output + msg)
            f.write(render)

def judge_format(parameterfilePath):
    matchJson = re.compile('\.json$')
    matchCsv = re.compile('\.csv$')
    if matchJson.search(parameterfilePath):
        with open(parameterfilePath) as f:
            try:
                params = json.load(f)
            except json.JSONDecodeError:
                print(LoggingSeverity.ERROR + 'This parameter file is not in Json format.')
                exit()
        return Format.JSON
    elif matchCsv.search(parameterfilePath):
        return Format.CSV
    else:
        return Format.UNKNOWN

def is_array(v):
    return type(v) is list

def generate_config(templatefilePath, parameterfilePath, mode):
    env = Environment(loader=FileSystemLoader('./', encoding="utf8"))
    template = env.get_template(templatefilePath)
    format = judge_format(parameterfilePath)
    if format == Format.JSON:
        print(LoggingSeverity.INFO + 'Parameter file is JSON')
        with open(parameterfilePath) as f:
            params = json.load(f)
        if is_array(params):
            for row in params:
                try:
                    filename = row['filename']
                except KeyError:
                    filename = None   
                render = template.render(row)
                save_file(render, mode, filename)
        else:
            try:
                filename = params['filename']
            except KeyError:
                filename = None   
                render = template.render(params)
                save_file(render, mode, filename)
    elif format == Format.CSV:
        print(LoggingSeverity.INFO + 'Parameter file is CSV')
    else:
        print(LoggingSeverity.ERROR + 'Invalid parameter file. (Available Files is .csv/.json)')

def main():
    args = arg_parse()
    templateFile = args['template_file']
    parameterFile = args['parameter_file']
    mode = args['append']
    if not(is_file(templateFile)):
        print(LoggingSeverity.ERROR + 'Template file is not found...')
        exit()
    if not(is_file(parameterFile)):
        print(LoggingSeverity.ERROR + 'Parameter file is not found...')
        exit()
    print(COLOR_YELLOW + '########## Config Generate ##########' + COLOR_CLEAR)
    generate_config(templateFile, parameterFile, mode)

    print(COLOR_YELLOW + '################ end ################' + COLOR_CLEAR)

if __name__ == "__main__":
    main()