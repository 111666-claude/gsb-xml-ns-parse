import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xmlns import core


class XmlnsTest(unittest.TestCase):
    def test_single_element(self):
        doc = core.parse("<r/>", core.Counter())
        self.assertEqual((doc.elems[0].ns, doc.elems[0].local), ("", "r"))

    def test_prefixed_element(self):
        doc = core.parse('<r xmlns:p="urn:a"><p:x/></r>', core.Counter())
        self.assertEqual(doc.elems[1].ns, "urn:a")

    def test_attribute_count(self):
        doc = core.parse('<r a="1" b="2"/>', core.Counter())
        self.assertEqual(len(doc.elems[0].attrs), 2)

    def test_element_count(self):
        doc = core.parse("<r><a/><b/></r>", core.Counter())
        self.assertEqual(len(doc.elems), 3)

    def test_find_unknown(self):
        doc = core.parse("<r/>", core.Counter())
        self.assertEqual(doc.find("urn:z", "x", core.Counter()), [])

    def test_counter_counts(self):
        counter = core.Counter()
        core.parse("<r/>", counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
