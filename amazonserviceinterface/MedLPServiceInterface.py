import boto3

from amazonserviceinterface.AmazonServiceInterface import AmazonServiceInterface


ALLOWED_ENTITY_TYPES = [
    "MEDICATION",
    "MEDICAL_CONDITION",
    "PERSONAL_IDENTIFIABLE_INFORMATION",
    "TEST_TREATMENT_PROCEDURE",
    "ANATOMY",
]

class MedLPServiceInterface(AmazonServiceInterface):
    def __init__(self, output_parser):
        '''

        :param output_parser: a function that accepts a dictionary and returns shaped output
        '''

        super(MedLPServiceInterface, self).__init__(
            'deepinsighthera',
            'US_EAST')

        self.parser = output_parser


    def get_entities(self, text, **kwargs):
        if "entityTypes" in kwargs:
            vetted_types = self._vet_entity_types(kwargs["entityTypes"])
            result = self.service.detect_entities(Text=text, Types=vetted_types)
        else:
            result = self.service.detect_entities(Text=text)
        print(len(result['Entities']))
        return self.parser(result['Entities'])


    def _vet_entity_types(self, type_list):
        print(type_list)
        print(type(type_list))
        print(isinstance(type_list, str))
        if (not isinstance(type_list, list)) and (not isinstance(type_list, str)):
            raise ValueError("Type Format Error")

        if isinstance(type_list, str):
            if type_list not in ALLOWED_ENTITY_TYPES:
                print("Singleton bad type found")
                raise ValueError("Invalid Type Error")
            return [type_list]
        else:
            for checked_type in type_list:
                if checked_type not in ALLOWED_ENTITY_TYPES:
                    print("bad type in list found: {}".format(checked_type))
                    raise ValueError("Invalid Type Error")

        return type_list
