from typing import List

from scraper import BankingSession
from config import BOA_schema
from schemas import AccountSchema, BankSchema


class Transaction:
    def __init__(self, txn_type: str, desc: str, amount: str, date: str):
        def clean_amount(amount):
            num = amount.replace(",", "")
            return float(num)

        self.__txn_type = txn_type
        self.__desc = desc
        self.__amount = clean_amount(amount)
        self.__date = date

    @property
    def txn_type(self) -> str:
        return self.__txn_type

    @property
    def desc(self) -> str:
        return self.__desc

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def date(self) -> str:
        return self.__date

    @property
    def id(self) -> str:
        str_amount = str(self.__amount)
        txn_id = f'{self.__date.replace("/","")}-{str_amount.replace(".","")}'
        return txn_id


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
            Account(
                self, kwargs["account_link"], kwargs["account_type"], kwargs["name"]
            )
        )

    @property
    def accounts(self):
        return self.__accounts

    @property
    def schema(self) -> BankSchema:
        return self.__schema

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, update: str):
        self.__username = update

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, update: str):
        self.__password = update


class Account:
    def __init__(self, bank: Bank, account_link: str, account_type: str, name: str):
        self.bank = bank
        self.__account_link = account_link
        self.account_type = account_type
        self.name = name
        self.__transactions = []

    def create_transaction(self, **kwargs: str):
        self.__transactions.append(
            Transaction(kwargs["type"], kwargs["desc"], kwargs["amt"], kwargs["dt"])
        )

    def get_account_schema(self) -> AccountSchema:
        bank_schema = self.bank.schema
        if self.account_type == "Checking":
            return bank_schema.checking_schema
        return bank_schema.liability_schema

    @property
    def transactions(self) -> List[Transaction]:
        return self.__transactions

    @property
    def url(self) -> str:
        return self.__account_link
