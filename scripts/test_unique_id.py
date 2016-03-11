"""
This script will test that create_unique_ide behaves as expected
"""

from __future__ import with_statement
import unittest
from create_database import create_unique_id

class TestUniqueID(unittest.TestCase):

    def test_bad_name(self):
        """
        Test that if you pass in an invalid SED name, create_unique_id fails
        """
        with self.assertRaises(RuntimeError) as ww:
            create_unique_id('hello', 0.9)

        self.assertIn('cannot return a unique id', ww.exception.args[0])


    def test_bad_redshift(self):
        """
        Test that if you pass in a redshift that is not an integer multiple
        of 0.1, create_unique_id fails
        """
        with self.assertRaises(RuntimeError) as ww:
            create_unique_id('Inst.79E06.002Z.spec', 1.11)

        self.assertIn('cannot return a unique id', ww.exception.args[0])


    def test_proper_input(self):
        """
        Test that create_unique_id runs when the input is sensible
        """
        ii = create_unique_id('Inst.79E06.002Z.spec', 1.1)
        self.assertIsInstance(ii, int)


if __name__ == "__main__":
    unittest.main()
