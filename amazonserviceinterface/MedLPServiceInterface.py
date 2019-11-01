import boto3
import itertools
import logging

from amazonserviceinterface.AmazonServiceInterface import AmazonServiceInterface

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CUTOFF_LENGTH = 20000

ALLOWED_ENTITY_TYPES = [
    "MEDICATION",
    "MEDICAL_CONDITION",
    "PROTECTED_HEALTH_INFORMATION",
    "TEST_TREATMENT_PROCEDURE",
    "ANATOMY",
]

ENTITY_CALL = 'entities'
PHI_CALL = 'phi'

class MedLPServiceInterface(AmazonServiceInterface):
    def __init__(self, output_parser):
        '''

        :param output_parser: a function that accepts a dictionary and returns shaped output
        '''

        super(MedLPServiceInterface, self).__init__(
            'comprehendmedical',
            'US_WEST')

        self.parser = output_parser

    def get_entities(self, text, **kwargs):
        kwargs['apicall'] = ENTITY_CALL
        return self._get_call(text, **kwargs)

    def get_phi(self, text, **kwargs):
        kwargs['apicall'] = PHI_CALL
        return self._get_call(text, **kwargs)

    def _get_call(self, text, **kwargs):
        cleaned_text = self.vet_text(text)
        return self._get_paginated_entities(cleaned_text, **kwargs)

    def _get_service_function(self, **kwargs):
        if 'apicall' not in kwargs.keys():
            logger.warning("call type Unspecified, returning default (get_entities) "
                           "this can occur if entering through a function other "
                           "than get_entities or get_phi")
            return self.service.detect_entities_v2
        if kwargs['apicall'] is ENTITY_CALL:
            return self.service.detect_entities_v2
        elif kwargs['apicall'] is PHI_CALL:
            return self.service.detect_phi
        else:
            logger.warning("Unexpected Call Type Encountered: {}, returning default (get_entities) "
                           "this can occur if entering through a function other "
                           "than get_entities or get_phi".format(kwargs['apicall']))
            return self.service.detect_entities_v2

    def _pare_returned_types(self, chunk_result, vetted_types):
        '''
        take a returned chunk from ComprehendMedical(ie: MedLPService)
        '''
        pared_dict = chunk_result
        pared_dict['Entities'] = [item for item in chunk_result['Entities'] if item['Category'] in vetted_types]

        return pared_dict

    def _get_paginated_entities(self, text_list, **kwargs):
        results = []
        char_offset = 0
        id_offset = 0

        fn = self._get_service_function(**kwargs)

        for i, text_chunk in enumerate(text_list):
            if "entityTypes" in kwargs:
                vetted_types = self._vet_entity_types(kwargs["entityTypes"])
                chunk_result = fn(Text=text_chunk)
                chunk_result = self._pare_returned_types(chunk_result, vetted_types)
            else:
                chunk_result = fn(Text=text_chunk)

            id_increment = 0
            try:
                id_increment = chunk_result['Entities'][-1]['Id'] + 1  # add the id Int of the last entity to the ongoing count
            except IndexError as e:
                logger.warning("no entities within range of {} to {}".format(char_offset, char_offset + CUTOFF_LENGTH))

            results.append(self._inject_offset_for_paginated_query(chunk_result['Entities'], char_offset, id_offset))
            char_offset += len(text_chunk)
            id_offset += id_increment #add the id Int of the last entity to the ongoing count


        flattened_results = list(itertools.chain.from_iterable(results))

        return flattened_results


    def _inject_offset_for_paginated_query(self, entity_chunk, char_offset: int, id_offset: int):
        '''
        Given a JSON-like entity, use the provided initial char offset and entity ID offset to
        :param entity_chunk: a list of dicts containing: 'Id', 'BeginOffset', 'EndOffset'
        :param char_offset: the int offset to add to all entities
        :param id_offset: the ID count offset to add to all ID's
        :return:
        '''
        for entity in entity_chunk:
            entity['Id'] = entity['Id'] + id_offset
            entity['BeginOffset'] = entity['BeginOffset'] + char_offset
            entity['EndOffset'] = entity['EndOffset'] + char_offset

        return entity_chunk


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

        logger.warning("No suitable cutoff was found in text of length {}."
                       " returning original text at final character: '{}'"
                       .format(len(text_chunk), text_chunk[-1]))
        return text_chunk


    def _vet_entity_types(self, type_list):
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
