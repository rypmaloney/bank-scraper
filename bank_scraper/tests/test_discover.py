import os

import unittest
from bank import Bank
from scraper import BankingSession
from config import Discover_schema


from dotenv import load_dotenv


load_dotenv()


class DiscoverBankingSessionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        user = os.environ.get("DISCOVER_USER")
        password = os.environ.get("DISCOVER_PASS")
        cls.bank = Bank("Discover", user, password, schema=Discover_schema)
        cls.session = BankingSession(cls.bank, headless=False)

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    def test_login(self):
        self.session.login()

    def test_scrape_overview(self):
        accounts = self.session.scrape_overview()
        print(f"{len(accounts)} found.")
        print(accounts)

        self.assertEqual(len(self.bank.accounts), len(accounts))
        self.assertTrue(accounts, "No accounts found!")

    def test_scrape_account(self):
        transactions = self.session.scrape_account(self.bank.accounts[0])
        print(f"{len(transactions)} found.")
        print(transactions)
        self.assertEqual(len(self.bank.account[0].trasactions), len(transactions))
        self.assertTrue(transactions, "No transactions found!")


if __name__ == "__main__":
    unittest.main()
