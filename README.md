## requires

boto3
awscli

## set up
aws configure

aws configure add-model --service-model file://\\CENTER\fh\secure\_HDC\Teams\Data-Science\NLP\HutchHera\deepinsighthera-2017-01-01.normal.json --service-name deepinsighthera

aws deepinsighthera detect-entities --endpoint-url https://aws707.us-east-1.amazonaws.com/ --text "cerealx 84 mg daily" --region us-east-1