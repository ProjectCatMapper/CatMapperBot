import unittest

from catmapperbot.manifest import claim_value, validate_rows


class ManifestValidationTests(unittest.TestCase):
    def test_valid_rows(self):
        validate_rows([{"qid": "Q42", "cmid": "SM1"}])

    def test_rejects_duplicate_qid(self):
        with self.assertRaisesRegex(ValueError, "duplicate QID"):
            validate_rows([{"qid": "Q42", "cmid": "SM1"}, {"qid": "Q42", "cmid": "SM2"}])

    def test_rejects_archamap_id_for_sociomap_target(self):
        with self.assertRaisesRegex(ValueError, "invalid sociomap"):
            validate_rows([{"qid": "Q42", "cmid": "AM1"}])

    def test_accepts_archamap_id_for_exact_match_target(self):
        validate_rows([{"qid": "Q42", "cmid": "AM1"}], "archamap")
        self.assertEqual(
            "https://catmapper.org/archamap/AM1",
            claim_value("AM1", "archamap"),
        )
