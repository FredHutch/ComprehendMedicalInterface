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
> from amazonserviceinterface.MedLPServiceInterface import MedLPServiceInterface
> import ClinicalNotesProcessor.JSONParser as JSONParser
> note_text = 'cerealx 84 mg daily'

> types = ['PROTECTED_HEALTH_INFORMATION', 'MEDICATION']

> medlp = MedLPServiceInterface(JSONParser.xform_dict_to_json)
> medlp.get_entities(note_text, entityTypes=types)  
> medlp.get_entities(note_text)
