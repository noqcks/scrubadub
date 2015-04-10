import unittest

import scrubadub

from base import BaseTestCase


class PhoneNumberTestCase(unittest.TestCase, BaseTestCase):

    def _test_phone_numbers(self, *phone_numbers):
        for phone_number in phone_numbers:
            self.assertEqual(
                self.clean(u'My phone number is %s' % phone_number),
                u'My phone number is {{PHONE}}',
                'missing phone number "%s"' % phone_number,
            )

    def test_american_phone_number(self):
        """test american-style phone numbers"""
        self._test_phone_numbers(
            '1-312-515-2239',
            '+1-312-515-2239',
            '1 (312) 515-2239',
            '312-515-2239',
            '(312) 515-2239',
            '(312)515-2239',
        )

    def test_extension_phone_numbers(self):
        """test phone numbers with extensions"""
        self._test_phone_numbers(
            '312-515-2239 x12',
            '312-515-2239 ext. 12',
            '312-515-2239 ext.12',
        )

    def test_international_phone_numbers(self):
        """test international phone numbers"""
        self._test_phone_numbers(
            '+47 21 30 85 99',
            '+45 69 19 88 56',
            '+46 852 503 499',
            '+31 619 837 236',
            '+86 135 3727 4136',
            '+61267881324',
        )

    def test_multiple_phone_numbers(self):
        # running this through scrubadub.clean replaces 'reached at
        # 312.714.8142' with '{{EMAIL}}'. See issue
        scrubber = scrubadub.scrubbers.Scrubber()
        result = scrubber.clean_phone_numbers(
            u'I can be reached at 312.714.8142 (cell) or 773.415.7432 (office)'
        )
        self.assertEqual(
            result,
            u'I can be reached at {{PHONE}} (cell) or {{PHONE}} (office)',
            'problem with multiple phone numbers: \n %s' % result,
        )