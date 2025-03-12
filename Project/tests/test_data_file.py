"""
This module Tests the created data.json file

Author: Luke Voss
Email: luke.voss@stud.uni-heidelberg.de
Created: 23.02.2024
Last Updated: 23.02.2024
Version: 1.0.0

Requirements:
- Pandas
"""

import unittest
import pandas as pd


class TestJson(unittest.TestCase):
    def setUp(self):
        """
        Load dataset once before each test method.
        """
        self.docs = pd.read_json("./datasets/data.json")

    def test_articles_contain_intelligence(self):
        """
        Ensure 'intelligence' is present in the title or the abstract for each entry
        """
        mask = self._contains_intelligence("title") | self._contains_intelligence(
            "abstract"
        )
        self.assertTrue(mask.all())

    def test_articles_between_2013_and_2023(self):
        """
        Check if Puplication Date is between 2013 and 2023 for each entry
        """
        years = self.docs["date"].str[:4]
        years = pd.to_numeric(years, errors="coerce")
        mask = years.between(2013, 2023, inclusive="both")
        self.assertTrue(mask.all())

    def _contains_intelligence(self, row):
        return self.docs[row].str.contains("intelligence", case=False, na=False)


if __name__ == "__main__":
    unittest.main()
