import time
from typing import List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import undetected_chromedriver as uc


class BankingSession:
    """
    Represents a scraping session for a bank user.

    Attributes:
        driver (webdriver.Chrome): Chrome WebDriver instance for browser automation.

    Methods:
        __init__(self, bank, headless=True, delay=10): Initializes a BankingSession instance.
        __wait(self): Delays for page loads.
        close(self): Closes the WebDriver instance.
        login(self): Logs in to the bank account and lands on the account overview page.
        scrape_accounts(self): Scrapes the account overview page to create account objects.
        scrape_account(self, account): Scrapes a given account page to create account objects for the transactions.
    """

    driver: uc.Chrome

    def __init__(self, bank, headless=True, delay=3):
        """
        Args:
            bank: Bank object representing the bank.
            headless (bool, optional): Whether to run the browser in headless mode. Defaults to True.
            delay (int, optional): Delay in seconds for page loads. Defaults to 10.

        """
        self.__bank = bank
        self.__delay = delay

        options = uc.ChromeOptions()
        options.headless = headless

        self.driver = uc.Chrome()

    def __wait(self) -> None:
        """
        Delay for page loads.
        """
        time.sleep(self.__delay)

    def __get_domain(self, url: str) -> str:
        parsed_url = urlparse(url)
        result = "{uri.scheme}://{uri.netloc}".format(uri=parsed_url)
        return result

    def close(self) -> None:
        """
        Closes the WebDriver instance.
        """
        self.driver.close()

    def login(self) -> None:
        """
        Log in to bank account. Land on account overview page.
        """
        schema = self.__bank.schema
        login = schema.login_schema
        two_factor = schema.two_factor_schema

        self.driver.get(login.login_url)

        self.__wait()
        try:
            login.user_field.send_keys(self.driver, self.__bank.username)
            login.pass_field.send_keys(self.driver, self.__bank.password)
        except TypeError as e:
            print(f"{e}: Update youre username and password.")

        self.__wait()
        login.submit.send_submit(self.driver)

        if two_factor:
            if self.driver.current_url == two_factor.tf_factor_url:
                two_factor.tf_continue.click(self.driver)
                print("2-Factor Auth required. Input code:")
                self.__wait()
                two_factor.tf_pass_field.send_keys(self.driver, input())
                two_factor.tf_submit.click(self.driver)

        print("Login Successful.")

    def scrape_overview(self) -> List:
        """
        Scrapes the account overview page to create account objects.

        Returns:
            list: A list of account objects.
        """

        schema = self.__bank.schema.overview_schema
        self.__wait()
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        if not schema:
            print(f"There is no overview for {self.__bank.name}")
            return False

        account_items = schema.items.query(soup)
        for item in account_items:
            name = schema.account_name.text(item)
            a = schema.account_link.query(item)
            account_type = item.get("data-accounttype", "Liability")

            self.__bank.create_account(
                account_link=a["href"], account_type=account_type, name=name
            )

        print(f"{len(self.__bank.accounts)} accounts found.")
        return self.__bank.accounts

    def scrape_account(self, account) -> List:
        """
        Scrapes a given account page to create account objects for the transactions.

        Args:
            account: The account for which to scrape transactions.

        Returns:
            list: A list of transaction objects for the account.
        """
        account_url = account.url
        if account_url[0] == "/":
            domain = self.__get_domain(self.driver.current_url)
            account_url = domain + account.url

        self.driver.get(account_url)
        self.__wait()
        schema = account.get_account_schema()

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        table = schema.table.query(soup)
        rows = schema.rows.query(table)
        for trx in rows:
            try:
                date = schema.date.text(trx)
                description = schema.desc.text(trx)
                type_ = schema.type.text(trx)
                amount = schema.amount.text(trx)

                account.create_transaction(
                    type=type_, desc=description, amt=amount, dt=date
                )

            except AttributeError:
                # Skip header rows
                pass

        print(f"{len(account.transactions)} transactions found.")
        return account.transactions
