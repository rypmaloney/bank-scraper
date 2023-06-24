import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class BankingSession:
    def __init__(self, bank, headless=True, delay=10):
        self.bank = bank
        self.delay = delay
        options = webdriver.ChromeOptions()
        options.headless = headless
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        )
        self.driver = webdriver.Chrome(options=options)

    def wait(self):
        time.sleep(self.delay)

    def close(self):
        self.driver.close()

    def login(self):
        self.driver.get(self.bank.login_url)

        self.wait()
        self.driver.find_element(By.ID, "enterID-input").send_keys(self.bank.username)
        self.driver.find_element(By.ID, "tlpvt-passcode-input").send_keys(
            self.bank.password
        )
        self.driver.find_element(By.NAME, "enter-online-id-submit").click()

        if (
            self.driver.current_url
            == "https://secure.bankofamerica.com/login/sign-in/signOnSuccessRedirect.go"
        ):
            self.driver.find_element(By.ID, "btnARContinue").click()
            print("2-Factor Auth required. Input code:")
            self.wait()
            self.driver.find_element(By.CLASS_NAME, "authcode").send_keys(input())
            self.driver.find_element(By.ID, "continue-auth-number").click()

    def clear_modal(self):
        close_buttons = self.driver.find_elements(
            By.ID, "sasi-overlay-module-modalClose"
        )
        if len(close_buttons) > 0:
            self.driver.find_element(By.ID, "sasi-overlay-module-modalClose").click()

    def get_accounts(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        account_items = soup.find_all("div", {"class": "AccountItem"})
        for item in account_items:
            name = item.find(
                "span", {"class": "AccountName"}, recursive=False
            ).getText()
            account_id = item["data-adx"]
            account_type = item["data-accounttype"]

            self.bank.create_account(
                account_id=account_id, account_type=account_type, name=name
            )

    def scrape_account(self, account):
        self.driver.get(account.url)
        self.wait()
        attr = account.selectors  #

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        table = attr.table.query(soup)
        rows = attr.rows.query(table)
        for trx in rows:
            try:
                date = attr.date.text(trx)
                description = attr.desc.text(trx)
                type_ = attr.type.text(trx)
                amount = attr.amount.text(trx)

                account.create_transaction(
                    type=type_, desc=description, amt=amount, dt=date
                )

            except AttributeError:
                # Skip header rows
                pass

    def run_through(self):
        self.login()
        self.clear_modal()
        self.get_accounts()
