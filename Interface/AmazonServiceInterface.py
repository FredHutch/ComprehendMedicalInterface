import boto3


class AmazonServiceInterface():
    def __init__(self, service_name, region, endpoint):
        '''

        :param service_name: the AWS service name
        :param region:  the AWS operating region, like 'us-east-1', 'us-west-2'
        :param endpoint: The AWS URL endpoint, like: https://aws707.us-east-1.amazonaws.com/
        '''
        self.service = boto3.client(service_name=service_name,
                                    region_name=region,
                                    endpoint_url=endpoint,
                                    use_ssl=True);