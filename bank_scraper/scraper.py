import time
from typing import List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver


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

    driver: webdriver.Chrome

    def __init__(self, bank, headless=True, delay=5):
        """
        Args:
            bank: Bank object representing the bank.
            headless (bool, optional): Whether to run the browser in headless mode. Defaults to True.
            delay (int, optional): Delay in seconds for page loads. Defaults to 10.

        """
        self.__bank = bank
        self.__delay = delay
        options = webdriver.ChromeOptions()
        options.headless = headless
        options.add_argument("--window-size=1920,1080")
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )
        self.driver = webdriver.Chrome(options=options)

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

        login.submit.click(self.driver)

        if two_factor:
            if self.driver.current_url == two_factor.tf_factor_url:
                two_factor.tf_continue.click(self.driver)
                print("2-Factor Auth required. Input code:")
                self.__wait()
                two_factor.tf_pass_field.send_keys(self.driver, input())
                two_factor.tf_submit.click(self.driver)

        print("Login Successful.")

    def scrape_accounts(self) -> List:
        """
        Scrapes the account overview page to create account objects.

        Returns:
            list: A list of account objects.
        """

        schema = self.__bank.schema.overview_schema
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        account_items = schema.items.query(soup)
        for item in account_items:
            name = schema.account_name.text(item)
            a = schema.account_link.query(item)

            self.__bank.create_account(
                account_link=a["href"], account_type=item["data-accounttype"], name=name
            )
        return self.__bank.accounts

    def scrape_account(self, account) -> List:
        """
        Scrapes a given account page to create account objects for the transactions.

        Args:
            account: The account for which to scrape transactions.

        Returns:
            list: A list of transaction objects for the account.
        """
        domain = self.__get_domain(self.driver.current_url)
        self.driver.get(domain + account.url)
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

        return account.transactions()
