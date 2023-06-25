from datetime import datetime
from .scraper import BankingSession
from .config import BOA_schema
from .schemas import AccountSchema, BankSchema


class Transaction:
    def __init__(self, txn_type: str, desc: str, amount: float, date: datetime):
        self.txn_type = txn_type
        self.desc = desc
        self.amount = amount
        self.date = date
        self.txn_id = f'{date.replace("/","")}-{amount.replace(".","")}'


class Bank:
    def __init__(
        self, name: str, username: str, password: str, schema: BankSchema = BOA_schema
    ):
        self.name = name
        self.__username = username
        self.__password = password
        self.__schema = schema
        self.__accounts = []

    def generate_scraper(self, headless: bool = True) -> BankingSession:
        return BankingSession(self, headless=headless)

    def create_account(self, **kwargs):
        self.__accounts.append(
            Account(self, kwargs["account_id"], kwargs["account_type"], kwargs["name"])
        )

    def get_accounts(self):
        return self.__accounts

    def get_schema(self) -> BankSchema:
        return self.__schema

    def update_username(self, update: str):
        self.__username = update

    def get_username(self) -> str:
        return self.__username

    def update_password(self, update: str):
        self.__password = update

    def get_password(self) -> str:
        return self.__password


class Account:
    def __init__(self, bank: Bank, account_id: str, account_type: str, name: str):
        self.bank = bank
        self.account_id = account_id
        self.account_type = account_type
        self.name = name
        self.__transactions = []

    def create_transaction(self, **kwargs: str):
        self.__transactions.append(
            Transaction(kwargs["type"], kwargs["desc"], kwargs["amt"], kwargs["dt"])
        )

    def get_account_schema(self) -> AccountSchema:
        bank_schema = self.bank.get_schema()
        if self.account_type == "Checking":
            return bank_schema.checking_schema
        if self.account_type == "Liability":
            return bank_schema.liability_schema

    def get_transactions(self) -> list[Transaction]:
        return self.__transactions

    @property
    def url(self) -> str:
        uri = "https://secure.bankofamerica.com/"
        href = f"{uri}/myaccounts/brain/redirect.go?source=overview&target=acctDetails&adx={self.account_id}"
        return href
