import boto3


class MedLPServiceInterface():

    def __init__(self, output_parser):
        '''

        :param output_parser: a function that accepts a dictionary and returns shaped output
        '''
        self.hera = boto3.client(service_name='deepinsighthera', region_name='us-east-1',
                            endpoint_url='https://aws707.us-east-1.amazonaws.com/', use_ssl=True);

        self.parser = output_parser


    def get_entities(self, text):
        result = self.hera.detect_entities(Text=text)

        return self.parser(result['Entities'])