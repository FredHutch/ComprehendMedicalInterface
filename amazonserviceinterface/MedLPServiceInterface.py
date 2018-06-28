import boto3
import logging

from amazonserviceinterface.AmazonServiceInterface import AmazonServiceInterface

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CUTOFF_LENGTH = 20000

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
        cleaned_text = self.vet_text(text)
        if "entityTypes" in kwargs:
            vetted_types = self._vet_entity_types(kwargs["entityTypes"])
            result = self.service.detect_entities(Text=text, Types=vetted_types)
        else:
            result = self.service.detect_entities(Text=text)

        return self.parser(result['Entities'])


    def vet_text(self, text, cutoff=CUTOFF_LENGTH):
        text_len = len(text)
        if text_len < cutoff:
            logger.info("the vetted text had a length of {} where the cutoff was: {}."
            "returning without resizing or chunking".format(text_len, cutoff))
            return [text]

        current_idx = 0
        resized_text_chunks = []

        while(current_idx < text_len):
            text_chunk = text[current_idx : current_idx + cutoff]
            if current_idx + cutoff < text_len:
                text_chunk = self._find_cutoff_point_in_text(text_chunk)
            resized_text_chunks.append(text_chunk)
            current_idx += len(text_chunk)

        logger.info("{} resized chunks were returned for the original text of length: {}"
                    .format(len(resized_text_chunks), text_len))
        return resized_text_chunks


    def _find_cutoff_point_in_text(self, text_chunk):
        newline_list = ["\n", "\r"]
        idx = max([text_chunk.rfind(candidate)+ len(candidate) for candidate in newline_list])


        if idx > 0:
            return text_chunk[0:idx]

        logger.warning("No suitable cutoff was found in text of length {}. returning original text at final character: '{}'"
                       .format(len(text_chunk), text_chunk[-1]))
        return text_chunk


    def _vet_entity_types(self, type_list):
        print(type_list)
        print(type(type_list))
        print(isinstance(type_list, str))
        if (not isinstance(type_list, list)) and (not isinstance(type_list, str)):
            logger.warning("Type Format Error encountered for type_list parameter: {}".format(type_list))
            raise ValueError("Type Format Error")

        if isinstance(type_list, str):
            if type_list not in ALLOWED_ENTITY_TYPES:
                logger.warning("Singleton bad type found: {}".format(type_list))
                raise ValueError("Invalid Type Error")
            return [type_list]
        else:
            for checked_type in type_list:
                if checked_type not in ALLOWED_ENTITY_TYPES:
                    logger.warning("bad type in list found: {}".format(checked_type))
                    raise ValueError("Invalid Type Error")

        return type_list
