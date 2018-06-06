import argparse
import os
from Interface.MedLPServiceInterface import MedLPServiceInterface


cmd_arg_parser = argparse.ArgumentParser("medLPService Interface: a encapsulated way to interact with Amazon MedLP using a python wrapper.")
cmd_arg_parser.add_argument('-t', action="store_true", default=False,
                            dest="is_test",
                            help="Set mode to test. There will be additional debug information and no computationally expensive functions will be run.")

cmd_arg_parser.add_argument('--input',
                            action="store",
                            dest="input_file",
                            help="Load input text from a file")

print(os.path.dirname(os.path.realpath(__file__)))
cmd_args = cmd_arg_parser.parse_args()

'''

text = ""
for line in fileinput.input():
    text = text + line
'''

with open(cmd_args.input_file) as file:
   text = file.read()

medlp = MedLPServiceInterface()
entities = medlp.get_entities(text)

for entity in entities:
    print('Entity', entity)