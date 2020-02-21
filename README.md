# Amazon Service Interface
Python package of interfaces to AWS Services
## requires

boto3
awscli

## Valid Entity Types
Any one of the following can be supplied in order to check text for a subset of entity types 
By default, all entity types are evaluated

    "MEDICATION"
    "MEDICAL_CONDITION"
    "PROTECTED_HEALTH_INFORMATION"    
    "TEST_TREATMENT_PROCEDURE"
    "ANATOMY"
    
## set up
> from compmed.CompMedServiceInterface import CompMedServiceInterface
> import utils.json_parser_util as JSONParser
> 
note_text = 'Mr. Doe was diagnosed with Stage III adenocarcinoma of the left lung on 3/14/2018'

> types = ['PROTECTED_HEALTH_INFORMATION', 'MEDICATION']

> comp_med = CompMedServiceInterface(JSONParser.xform_dict_to_json)
> comp_med.get_entities(note_text, entityTypes=types)  
> comp_med.get_entities(note_text)
