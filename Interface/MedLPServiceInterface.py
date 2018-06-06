import boto3

from Interface.AmazonServiceInterface import AmazonServiceInterface


class MedLPServiceInterface(AmazonServiceInterface):

    def __init__(self, output_parser):
        '''

        :param output_parser: a function that accepts a dictionary and returns shaped output
        '''

        super(MedLPServiceInterface, self).__init__(
            service_name='deepinsighthera',
            region='us-east-1',
            endpoint='https://aws707.us-east-1.amazonaws.com/')


        self.parser = output_parser


    def get_entities(self, text):
        result = self.service.detect_entities(Text=text)
        print(len(result['Entities']))
        return self.parser(result['Entities'])