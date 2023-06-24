from .scraper import BankingSession
from .config import BOA_checking, BOA_liability


class Bank:
    def __init__(self, name, login_url, username, password):
        self.name = name
        self.login_url = login_url
        self.username = username
        self.password = password
        self.accounts = list()

    def generate_scraper(self, headless=True):
        return BankingSession(self, headless=headless)

    def create_account(self, **kwargs):
        self.accounts.append(
            Account(kwargs["account_id"], kwargs["account_type"], kwargs["name"])
        )


class Account:
    def __init__(self, bank, account_id, account_type, name):
        self.bank = bank
        self.account_id = account_id
        self.account_type = account_type
        self.name = name

        self.selectors = self.get_selectors(bank, account_type)

        self.transactions = list()

    def create_transaction(self, **kwargs):
        self.transactions.append(
            Transaction(kwargs["type"], kwargs["desc"], kwargs["amt"], kwargs["dt"])
        )

    @staticmethod
    def get_selectors(bank, account_type):
        if bank.name == "Bank of America":
            if account_type == "Checking":
                return BOA_checking
            if account_type == "Liability":
                return BOA_liability

    @property
    def url(self):
        uri = "https://secure.bankofamerica.com/"
        href = f"{uri}/myaccounts/brain/redirect.go?source=overview&target=acctDetails&adx={self.account_id}"
        return href


class Transaction:
    def __init__(self, txn_type, desc, amount, date):
        self.txn_type = txn_type
        self.desc = desc
        self.amount = amount
        self.date = date
        self.txn_id = f'{date.replace("/","")}-{amount.replace(".","")}'
