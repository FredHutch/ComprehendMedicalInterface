import boto3

from utils.decorators import validateargs, in_dict, is_string

class AmazonServiceInterface():
    VALID_ENDPOINTS = {
        'US_EAST': 'comprehendmedical.us-east-1.amazonaws.com',
        'US_WEST': 'comprehendmedical.us-west-2.amazonaws.com'
    }

    VALID_REGIONS = {
        'US_EAST': 'us-east-1',
        'US_WEST': 'us-west-2'
    }

    @validateargs
    def __init__(self, service_name, region: in_dict(VALID_REGIONS)):
        '''

        :param service_name: the AWS service name
        :param region:  the AWS operating region, like 'us-east-1', 'us-west-2'
        '''
        self.service = boto3.client(service_name=service_name,
                                    region_name=AmazonServiceInterface.VALID_REGIONS[region],
                                    use_ssl=True)