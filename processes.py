#! /usr/bin/env python3

import xml.etree.ElementTree as ET
import sys
import argparse
import json

arg_parse = argparse.ArgumentParser()
arg_parse.add_argument('age', help='The maximum uptime to filter',type=int)
arg_parse.add_argument('file', help='Xml file to read. Use - for stdin')

args = arg_parse.parse_args()

# Read from stdin if - is used
def read_json(file_path):

    if file_path == '-':
        try:
            return json.load(sys.stdin)
        except:
            print('Cannot open stdin')
    else:
        try:
            with open(file_path) as content:
                return json.load(content)
        except FileNotFoundError as e:
            sys.stderr.write('Error opening file: {}'.format(e))


def find_longrunning(json_data, age):

        try:
            for thread, stats in json_data.items():
                for client in stats['active_clients'].values():
                    if client['connected_at']['relative_timestamp'] < age:
                        print(stats['pid'], client['connected_at']['relative_timestamp'])
        except (AttributeError, TypeError) as e:
            sys.stderr.write('Key/Val not iterable {}:{} : {}'.format(thread, stats, e))

find_longrunning(read_json(args.file), args.age)

# tree = ET.parse(source)
# root = tree.getroot()
#
# for child in root.findall('supergroups/supergroup/group/processes/process'):
#     print(child.find('pid').text, child.find('uptime').text)



# data = json.load(source)
#
# for thread in data.items():
#     for thing in thread:
#         print(k, v)
#     # for attribute, value in thread.iter():
#     #     print(attribute, value)
