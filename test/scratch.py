import argparse
import os

import utils.json_parser_util as JSONParser
from compmed.CompMedServiceInterface import CompMedServiceInterface


cmd_arg_parser = argparse.ArgumentParser("CompMedService compmed: a encapsulated way to interact with Amazon Comprehend Medical using a python wrapper.")
cmd_arg_parser.add_argument('-t', action="store_true", default=False,
                            dest="is_test",
                            help="Set mode to test. There will be additional debug information and no computationally expensive functions will be run.")

cmd_arg_parser.add_argument('--input',
                            action="store",
                            dest="input_file",
                            help="Load input text from a file")

print(os.path.dirname(os.path.realpath(__file__)))
cmd_args = cmd_arg_parser.parse_args()


with open(cmd_args.input_file) as file:
   text = file.read()

comp_med = CompMedServiceInterface(JSONParser.xform_dict_to_json)
entities = comp_med.get_entities(text, entityTypes=["PERSONAL_IDENTIFIABLE_INFORMATION", "MEDICATION"])
print(entities)

