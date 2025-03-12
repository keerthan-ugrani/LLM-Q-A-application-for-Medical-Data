"""
This module provides an XML_Parser Object, that can be given a path to a PubMed XML format
and the file can be converted to a list or df object and cleans the search results. 

If executed as main, the script will parse the data.xml in /datasets to data.json 
in the same folder

Author: Luke Voss
Email: luke.voss@stud.uni-heidelberg.de
Created: 05.01.2024
Last Updated: 03.03.2024
Version: 1.3.0

Requirements:
- lxml
- Pandas
"""

import pandas as pd
from lxml import etree


class XML_Parser:
    """
    Parses a PubMed XML file to the required data format and filters articles to
    contain the word 'intelligence' and being published between 2013 and 2023

    Sample Usage:
    parser = XML_Parser('datasets/data.xml')
    df = parser.to_df()
    print(df.head())
    """

    def __init__(self, file_path):
        """
        Initializes the XML_Parser class.

        Args:
            file_path (str): File Path to PubMed XML file.
        """
        self.root = self._preprocess_and_parse_xml(file_path)
        self.df = None
        self.count_not_splitted = 0
        self.MONTHS_MAP = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12",
        }

    def to_df(self):
        """
        Converts the XML data to a Pandas DataFrame.

        Returns:
            pandas.DataFrame: DataFrame containing the parsed data.
        """
        articles_data = self.to_list()
        self.df = pd.DataFrame(articles_data)
        self.df = self.df.sort_values(by="pmid", ascending=True)
        self._clean_dataframe()
        print("Succesfully created df!")
        return self.df

    def to_list(self):
        """
        Converts the XML data to a list of dictionaries.

        Returns:
            list: List of dictionaries containing the parsed data.
        """
        articles_data = []
        for article in self.root.findall(".//PubmedArticle"):
            articles_data.append(self._process_article(article))
        for book in self.root.findall(".//PubmedBookArticle"):
            articles_data.append(self._process_article(book))
        return articles_data

    def export_to_json(self, file_path: str):
        """
        Exports the DataFrame to a JSON file.

        Args:
            file_path (str): The path to the file where the JSON will be saved.
        """
        self._ensure_valid_df()
        self.df.to_json(file_path, orient="records", lines=False, indent=4)
        print("Succesfully exported JSON File!")

    def export_to_pickle(self, file_path: str):
        """
        Exports the DataFrame to a Pickle file.

        Args:
            file_path (str): The path to the file where the Pickle file will be saved.
        """
        self._ensure_valid_df()
        self.df.to_pickle(file_path)
        print("Succesfully exported PKL File!")

    def _ensure_valid_df(self):
        if getattr(self, "df", None) is None or self.df.empty:
            self.to_df()

    def _preprocess_and_parse_xml(self, file_path):
        try:
            with open(file_path, "rb") as file:
                file_content = file.read().replace(b"&", b"&amp;")
            return etree.fromstring(file_content)
        except Exception as e:
            raise Exception(f"Error processing XML file: {e}")

    def _process_article(self, article):
        return {
            "pmid": self._get_element_text(article, ".//PMID"),
            "title": self._get_element_text(article, ".//ArticleTitle"),
            "authors": self._get_authors(article),
            "date": self._get_pub_date(article),
            "journal": self._get_element_text(article, ".//Journal/Title"),
            "abstract": self._get_abstract(article),
        }

    def _get_element_text(self, element, xpath):
        found = element.find(xpath)
        return found.text if found is not None else "None"

    def _get_authors(self, article):
        authors = []
        for author in article.findall(".//Author"):
            lastname = self._get_element_text(author, "LastName")
            if lastname:
                firstname = self._get_element_text(author, "ForeName")
                authors.append(f"{lastname}, {firstname}")
            else:
                collective_name = self._get_element_text(author, "CollectiveName")
                authors.append(collective_name)
        return authors

    def _get_pub_date(self, article):
        # Extract year, month, and day from the article
        year = self._get_element_text(article, ".//PubDate/Year")
        month = self._get_element_text(article, ".//PubDate/Month")
        day = self._get_element_text(article, ".//PubDate/Day")

        # Correct the month and day formats to ensure uniformity
        month = self._correct_month_format(month)
        day = self._correct_day_format(day)

        return f"{year}-{month}-{day}"

    def _correct_month_format(self, month):
        # Convert month abbreviation to number if necessary
        if month in self.MONTHS_MAP:
            return self.MONTHS_MAP[month]
        # Ensure month is two digits
        return month.zfill(2) if month else month

    def _correct_day_format(self, day):
        # Ensure day is two digits
        return day.zfill(2) if day else day

    def _get_abstract(self, article):
        abstract_text = ""
        for abstract_part in article.findall(".//Abstract/AbstractText"):
            text = abstract_part.text
            abstract_text = abstract_text + text + "\n\n "
        return abstract_text

    def _clean_dataframe(self):
        self._clean_no_intelligence()
        self._clean_wrong_pubdate()

    def _clean_no_intelligence(self):
        mask = self._contains_intelligence("title") | self._contains_intelligence(
            "abstract"
        )
        self.df = self.df[mask]

    def _clean_wrong_pubdate(self):
        years = self.df["date"].str[:4]
        years = pd.to_numeric(years, errors="coerce")
        mask = years.between(2013, 2023, inclusive="both")
        self.df = self.df[mask]

    def _contains_intelligence(self, row):
        return self.df[row].str.contains("intelligence", case=False, na=False)


if __name__ == "__main__":
    parser = XML_Parser("./datasets/data.xml")
    parser.export_to_json("./datasets/data_new.json")
