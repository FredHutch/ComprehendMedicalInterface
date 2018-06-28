import unittest
import clinicalnotesprocessor.JSONParser as JSONParser

from amazonserviceinterface.MedLPServiceInterface import MedLPServiceInterface

class TestMedLPServiceInterface(unittest.TestCase):

    def setUp(self):
        self.medLPServiceInterface = MedLPServiceInterface(JSONParser.xform_dict_to_json)
        self.INPUT_TEXT = "big happy case stuff \n that's small."
        self.INPUT_TEXT_NO_VALID_SPlIT = "big happy case stuff that's small."

    def tearDown(self):
        pass

    def test_vet_text_happycase(self):
        '''
        case: when text is smaller than the provided cutoff, and the text wrapped as a list is returned
        '''
        expectedOutput = [self.INPUT_TEXT]
        actualOutput = self.medLPServiceInterface.vet_text(self.INPUT_TEXT, cutoff=10000)

        self.assertEqual(expectedOutput, actualOutput, "when text is smaller than the provided cutoff, "
                                                       "and the text wrapped as a list is returned")

    def test_vet_text_single_split(self):
        '''
        case: when text is larger than the provided cutoff, the text will split on first available newline
        '''

        expectedOutput = [self.INPUT_TEXT[0:22], self.INPUT_TEXT[22:]]
        actualOutput = self.medLPServiceInterface.vet_text(self.INPUT_TEXT, cutoff=25)

        self.assertEqual(expectedOutput, actualOutput, "the text will split on first available newline")


    def test_vet_text_no_valid_split_available(self):
        '''
        case: when text is larger than the provided cutoff, the text will default to
        splitting at the cutoff if no viable option is found
        '''

        expectedOutput = [self.INPUT_TEXT_NO_VALID_SPlIT[0:25], self.INPUT_TEXT_NO_VALID_SPlIT[25:]]
        actualOutput = self.medLPServiceInterface.vet_text(self.INPUT_TEXT_NO_VALID_SPlIT, cutoff=25)

        self.assertEqual(expectedOutput, actualOutput, "the text will default to splitting at the cutoff"
                                                       " if no viable option is found")