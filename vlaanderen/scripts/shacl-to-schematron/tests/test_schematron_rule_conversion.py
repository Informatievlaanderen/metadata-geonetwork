import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

SRC_DIR = Path(__file__).resolve().parents[1] / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import SchematronGenerator as generator_module  # noqa: E402
from SchematronGenerator import SchematronGenerator  # noqa: E402
from SchematronRule import SchematronRule  # noqa: E402
from constants import schNamespaces  # noqa: E402


class SchematronRuleConversionTest(unittest.TestCase):
    def _find_let_map(self, rule_el):
        lets = {}
        for let_el in rule_el.findall('sch:let', schNamespaces):
            lets[let_el.get('name')] = let_el.get('value')
        return lets

    def _base_prop(self, **overrides):
        prop = {
            '@id': 'rule-1',
            'sh:path': 'dct:title'
        }
        prop.update(overrides)
        return prop

    def test_cardinality_langstring_uses_multilingual_abstract_pattern(self):
        rule = SchematronRule(
            self._base_prop(**{
                'sh:datatype': 'rdf:langString',
                'sh:minCount': '1',
                'sh:maxCount': 'n'
            }),
            ['dcat:Dataset'],
            False
        )

        pattern = rule.getCardinalityPatternElement()
        self.assertIsNotNone(pattern)
        self.assertEqual('MultilingualCardinalityCheck', pattern.get('is-a'))

        params = {
            p.get('name'): p.get('value')
            for p in pattern.findall('sch:param', schNamespaces)
        }
        self.assertEqual('//dcat:Dataset', params['context'])
        self.assertEqual('dct:title', params['element'])
        self.assertEqual('1', params['min'])
        self.assertEqual('n', params['max'])

    def test_cardinality_non_langstring_uses_standard_abstract_pattern(self):
        rule = SchematronRule(
            self._base_prop(**{
                'sh:datatype': 'xs:string',
                'sh:minCount': '0',
                'sh:maxCount': '1'
            }),
            ['dcat:Dataset'],
            False
        )

        pattern = rule.getCardinalityPatternElement()
        self.assertIsNotNone(pattern)
        self.assertEqual('CardinalityCheck', pattern.get('is-a'))

    def test_datatype_literal_generates_literal_assertion(self):
        rule = SchematronRule(
            self._base_prop(**{
                'sh:datatype': 'xs:string',
                'sh:name': {'en': 'title'}
            }),
            ['dcat:Dataset'],
            False
        )

        pattern = rule.getPatternElement()
        self.assertIsNotNone(pattern)
        rule_el = pattern.find('sch:rule', schNamespaces)
        self.assertIsNotNone(rule_el)
        self.assertEqual('//dcat:Dataset/dct:title', rule_el.get('context'))

        lets = self._find_let_map(rule_el)
        self.assertIn('isLiteral', lets)
        self.assertEqual("normalize-space(.) != ''", lets['isLiteral'])

        assert_el = rule_el.find('sch:assert', schNamespaces)
        self.assertIsNotNone(assert_el)
        self.assertEqual('$isLiteral', assert_el.get('test'))
        self.assertIn('(dct:title)', assert_el.text)

    def test_nodekind_iri_for_mbox_requires_mailto(self):
        rule = SchematronRule(
            {
                '@id': 'rule-mailto',
                'sh:path': 'foaf:mbox',
                'sh:nodeKind': 'sh:IRI',
                'sh:name': {'en': 'email'}
            },
            ['dcat:Dataset'],
            False
        )

        pattern = rule.getPatternElement()
        self.assertIsNotNone(pattern)
        rule_el = pattern.find('sch:rule', schNamespaces)
        lets = self._find_let_map(rule_el)

        self.assertIn('resource', lets)
        self.assertIn('isIRI', lets)
        self.assertIn('isMailto', lets)

        assert_el = rule_el.find('sch:assert', schNamespaces)
        self.assertEqual('$isIRI and $isMailto', assert_el.get('test'))

    def test_generate_schematron_writes_externalized_localized_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / 'schematron'

            generator = SchematronGenerator(
                'schematron-rules-test-output',
                {
                    'dut': 'Test',
                    'eng': 'Test',
                    'fre': 'Test',
                    'ger': 'Test'
                },
                profile=None,
                enableTranslation=False
            )
            generator.addRule(
                SchematronRule(
                    self._base_prop(**{
                        'sh:datatype': 'xs:string',
                        'sh:name': {'en': 'title'}
                    }),
                    ['dcat:Dataset'],
                    False
                )
            )

            with patch.object(generator_module, 'schOutput', str(output_dir)):
                generator.generateSchematron()

            output_file = output_dir / 'schematron-rules-test-output.sch'
            self.assertTrue(output_file.exists())

            root = ET.parse(output_file).getroot()
            pattern = root.find('sch:pattern', schNamespaces)
            self.assertIsNotNone(pattern)

            title = pattern.find('sch:title', schNamespaces)
            self.assertIsNotNone(title)
            self.assertTrue(title.text.startswith('$loc/strings/test-output.pattern.title.'))

            assert_el = pattern.find('sch:rule/sch:assert', schNamespaces)
            report_el = pattern.find('sch:rule/sch:report', schNamespaces)
            self.assertIsNotNone(assert_el)
            self.assertIsNotNone(report_el)
            self.assertTrue(assert_el.text.startswith('$loc/strings/test-output.pattern.assert.'))
            self.assertTrue(report_el.text.startswith('$loc/strings/test-output.pattern.report.'))


if __name__ == '__main__':
    unittest.main()

