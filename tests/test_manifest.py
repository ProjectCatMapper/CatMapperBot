import unittest

from catmapperbot.manifest import validate_rows


class ManifestValidationTests(unittest.TestCase):
    def test_valid_rows(self):
        validate_rows([{"qid": "Q42", "cmid": "SM1"}])

    def test_rejects_duplicate_qid(self):
        with self.assertRaisesRegex(ValueError, "duplicate QID"):
            validate_rows([{"qid": "Q42", "cmid": "SM1"}, {"qid": "Q42", "cmid": "SM2"}])

    def test_rejects_archamap_id(self):
        with self.assertRaisesRegex(ValueError, "invalid SocioMap"):
            validate_rows([{"qid": "Q42", "cmid": "AM1"}])

