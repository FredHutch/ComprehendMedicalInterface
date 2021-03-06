import unittest
import utils.json_parser_util as JSONParser

from compmed.CompMedServiceInterface import CompMedServiceInterface
import unittest.mock as mock

class TestMedLPServiceInterface(unittest.TestCase):

    def setUp(self):
        self.CompMedServiceInterface = CompMedServiceInterface(JSONParser.xform_dict_to_json)
        self.INPUT_TEXT = "big happy case stuff \n that's small."
        self.INPUT_TEXT_MULTIPLE_NEWLINES = "big happy case stuff \n\r that's small."
        self.INPUT_TEXT_NO_VALID_SPlIT = "big happy case stuff that's small."

    def tearDown(self):
        pass

    def test_vet_text_happycase(self):
        '''
        case: when text is smaller than the provided cutoff, and the text wrapped as a list is returned
        '''
        expectedOutput = [self.INPUT_TEXT]
        actualOutput = self.CompMedServiceInterface.vet_text(self.INPUT_TEXT, cutoff=10000)

        self.assertEqual(expectedOutput, actualOutput, "when text is smaller than the provided cutoff, "
                                                       "and the text wrapped as a list is returned")

    def test_vet_text_single_split(self):
        '''
        case: when text is larger than the provided cutoff, the text will split on first available newline
        '''

        expectedOutput = [self.INPUT_TEXT[0:22], self.INPUT_TEXT[22:]]
        actualOutput = self.CompMedServiceInterface.vet_text(self.INPUT_TEXT, cutoff=25)

        self.assertEqual(expectedOutput, actualOutput, "the text will split on first available newline")


    def test_vet_text_no_valid_split_available(self):
        '''
        case: when text is larger than the provided cutoff, the text will default to
        splitting at the cutoff if no viable option is found
        '''

        expectedOutput = [self.INPUT_TEXT_NO_VALID_SPlIT[0:25], self.INPUT_TEXT_NO_VALID_SPlIT[25:]]
        actualOutput = self.CompMedServiceInterface.vet_text(self.INPUT_TEXT_NO_VALID_SPlIT, cutoff=25)

        self.assertEqual(expectedOutput, actualOutput, "the text will default to splitting at the cutoff"
                                                       " if no viable option is found")


    def test_vet_text_single_split_multiple_valid_newlines(self):
        '''
        case: when text is larger than the provided cutoff, the text will split on first available newline
        even if there are multiple valid candidates
        '''

        expectedOutput = [self.INPUT_TEXT_MULTIPLE_NEWLINES[0:23], self.INPUT_TEXT_MULTIPLE_NEWLINES[23:]]
        actualOutput = self.CompMedServiceInterface.vet_text(self.INPUT_TEXT_MULTIPLE_NEWLINES, cutoff=26)

        self.assertEqual(expectedOutput, actualOutput, "the text will split on first available newline, "
                                                       "even if there are multiple valid candidates")

    def test_inject_offset_for_paginated_query(self):
        '''
        case: entity chunk is returned with offsets injected

        '''
        input = [{'Id': 0, 'BeginOffset': 10, 'EndOffset': 20, 'Score': .99},
                 {'Id': 1, 'BeginOffset': 30, 'EndOffset': 35, 'Score': .99}]
        expectedOutput = [{'Id': 20, 'BeginOffset': 20, 'EndOffset': 30, 'Score': .99},
                          {'Id': 21, 'BeginOffset': 40, 'EndOffset': 45, 'Score': .99}]
        actualOutput = self.CompMedServiceInterface._inject_offset_for_paginated_query(input, 10, 20)

        self.assertEqual(expectedOutput, actualOutput, "entity chunk is returned with offsets injected")


    def test_get_paginated_entities(self):
        '''
        case: when the MedLPService is called with paginated input, the output is correctly stitched together.
        '''
        serviceOutput_1 = {'Entities':
                               [{'Id': 0, 'BeginOffset': 20, 'EndOffset': 30, 'Score': .99},
                               {'Id': 1, 'BeginOffset': 40, 'EndOffset': 45, 'Score': .99}]
                           }
        serviceOutput_2 = {'Entities':
                               [{'Id': 0, 'BeginOffset': 20, 'EndOffset': 30, 'Score': .99},
                               {'Id': 1, 'BeginOffset': 40, 'EndOffset': 45, 'Score': .99}]
                           }
        serviceOutput_3 = {'Entities':
                               [{'Id': 0, 'BeginOffset': 20, 'EndOffset': 30, 'Score': .99},
                                {'Id': 1, 'BeginOffset': 40, 'EndOffset': 45, 'Score': .99}]
                           }
        mockCompMedService = mock.MagicMock()
        mockCompMedService.detect_entities.side_effect = iter([serviceOutput_1, serviceOutput_2, serviceOutput_3])
        self.CompMedServiceInterface.service = mockCompMedService

        input = ["foo bar baz", "bif zoom pow", "bof zow bonk"]
        expectedOutput = [{'Id': 0, 'BeginOffset': 20, 'EndOffset': 30, 'Score': .99},
                          {'Id': 1, 'BeginOffset': 40, 'EndOffset': 45, 'Score': .99},
                          {'Id': 2, 'BeginOffset': 31, 'EndOffset': 41, 'Score': .99},
                          {'Id': 3, 'BeginOffset': 51, 'EndOffset': 56, 'Score': .99},
                          {'Id': 4, 'BeginOffset': 43, 'EndOffset': 53, 'Score': .99},
                          {'Id': 5, 'BeginOffset': 63, 'EndOffset': 68, 'Score': .99}
                          ]
        actualOutput = self.CompMedServiceInterface._get_paginated_entities(input, apicall='entities')

        self.assertEqual(expectedOutput,
                         actualOutput,
                         "The returns from the MedLPService will be correctly stitched together across calls")

