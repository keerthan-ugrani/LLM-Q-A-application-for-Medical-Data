"""
This module Tests the XML_Parser class and its functionalities

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

from preprocessing import XML_Parser


class TestXMLParser(unittest.TestCase):
    def setUp(self):
        self.parser = XML_Parser("./datasets/data_test.xml")
        self.df = self.parser.to_df()
        print(self.df.head())
        self.parser.export_to_json("./datasets/data_test.json")

    def test_normal_article(self):
        normal_article = self.df.iloc[0]
        self.assertEqual(normal_article["pmid"], "0")
        self.assertEqual(normal_article["title"], "ArticleTitle intelligence")
        self.assertEqual(
            normal_article["authors"][0],
            "ArticleAuthor1_LastName, ArticleAuthor1_ForeName",
        )
        self.assertEqual(
            normal_article["authors"][1],
            "ArticleAuthor2_LastName, ArticleAuthor2_ForeName",
        )
        self.assertEqual(normal_article["date"], "2013-01-01")
        self.assertEqual(normal_article["journal"], "JournalTitle")
        self.assertEqual(normal_article["abstract"], "AbstractText\n\n ")

    def test_normal_book(self):
        normal_book = self.df.iloc[1]
        self.assertEqual(normal_book["title"], "Article_of_BookTitel intelligence")
        self.assertEqual(
            normal_book["authors"][0], "BookAuthor1_LastName, BookAuthor1_ForeName"
        )
        self.assertEqual(
            normal_book["authors"][1], "BookAuthor2_LastName, BookAuthor2_ForeName"
        )
        self.assertEqual(
            normal_book["authors"][2],
            "ArticleAuthor1_LastName, ArticleAuthor1_ForeName",
        )
        self.assertEqual(
            normal_book["authors"][3],
            "ArticleAuthor2_LastName, ArticleAuthor2_ForeName",
        )
        self.assertEqual(normal_book["date"], "2013-01-01")
        self.assertEqual(normal_book["journal"], "None")
        self.assertEqual(normal_book["abstract"], "AbstractText\n\n ")


if __name__ == "__main__":
    unittest.main()
