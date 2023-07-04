import unittest

from bank import Transaction, Bank
from scraper import BankingSession
from schemas import BankSchema


class TestTransaction(unittest.TestCase):
    def test_transaction_attributes(self):
        txn_type = "debit"
        desc = "Grocery shopping"
        amount = "50.25"
        date = "6/30/2023"
        txn = Transaction(txn_type, desc, amount, date)

        # Test attribute values
        float_txn_amount = float(amount)
        self.assertEqual(txn.txn_type, txn_type)
        self.assertEqual(txn.desc, desc)
        self.assertEqual(txn.amount, float_txn_amount)
        self.assertEqual(txn.date, date)

    def test_transaction_txn_id(self):
        txn_type = "credit"
        desc = "Salary"
        amount = "1000.0"
        date = "6/30/2023"
        txn = Transaction(txn_type, desc, amount, date)

        # Test txn_id format
        expected_txn_id = "6302023-10000"
        self.assertEqual(txn.id, expected_txn_id)


class BankTests(unittest.TestCase):
    def setUp(self):
        self.dummy_schema = BankSchema()

    def test_generate_scraper(self):
        bank = Bank("Test Bank", "test_user", "test_password")
        scraper = bank.generate_scraper()
        self.assertIsInstance(scraper, BankingSession)

    def test_create_account(self):
        bank = Bank("Test Bank", "test_user", "test_password")
        bank.create_account(
            account_link="account_link_1",
            account_type="account_type_1",
            name="Account 1",
        )
        self.assertEqual(len(bank.accounts), 1)
        account = bank.accounts[0]
        self.assertEqual(account.url, "account_link_1")
        self.assertEqual(account.bank, bank)

    def test_username_property(self):
        bank = Bank("Test Bank", "test_user", "test_password")
        self.assertEqual(bank.username, "test_user")
        bank.username = "new_user"
        self.assertEqual(bank.username, "new_user")

    def test_password_property(self):
        bank = Bank("Test Bank", "test_user", "test_password")
        self.assertEqual(bank.password, "test_password")
        bank.password = "new_password"
        self.assertEqual(bank.password, "new_password")

    def test_schema_property(self):
        bank = Bank("Test Bank", "test_user", "test_password", schema=self.dummy_schema)
        self.assertEqual(bank.schema, self.dummy_schema)


if __name__ == "__main__":
    unittest.main()
