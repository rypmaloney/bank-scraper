from dataclasses import dataclass
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class Element:
    """
    Represents an element on a webpage.

    Attributes:
        element (str): HTML tag name of the element.
        selector (str, optional): Selector used to locate the element.
        value (str, optional): Value associated with the selector.
        find_all (bool, optional): Flag indicating whether to find all matching elements.
        recursive (bool): Flag indicating whether to search for the element recursively.
                          For 'td' elements, recursive is set to False.

    Methods:
        query(target): Finds the element in the target object.
        text(target): Retrieves the text content of the element from the target object.
        find_element(driver): Finds the element using the specified selector and value in the Selenium driver object.
        send_keys(driver, keys): Sends keys or text to the element found in the Selenium driver object.
        click(driver): Performs a click action on the element found in the Selenium driver object.
    """

    def __init__(self, element, selector=None, value=None, find_all=False):
        self.element = element
        self.selector = selector
        self.value = value
        self.find_all = find_all
        self.recursive = True
        if element == "td":
            self.recursive = False

    def query(self, target):
        """
        Finds the element in the target object.
        Target is a Beautiful Soup element.

        Args:
            target: The object on which to find the element.

        Returns:
            ResultSet or Tag: The result of the query.
        """
        if self.find_all:
            return target.find_all(self.element, {self.selector: self.value})
        return target.find(
            self.element, {self.selector: self.value}, recursive=self.recursive
        )

    def text(self, target) -> str:
        """
        Retrieves the text content of the element from the target object.

        Args:
            target: The object containing the element.

        Returns:
            str: The text content of the element after applying cleaning operations.
        """
        return (
            self.query(target)
            .getText()
            .replace("$", "")
            .replace("\n", " ")
            .replace("Expand transaction for Transaction date:", "")
            .replace("Expand transaction", "")
            .strip()
        )

    def find_element(self, driver) -> WebElement:
        """
        Finds the element using the specified selector and value in the Selenium driver object.

        Args:
            driver: The Selenium driver object.

        Returns:
            WebElement: The found element.
        """

        if self.selector == "id":
            return driver.find_element(By.ID, self.value)
        if self.selector == "name":
            return driver.find_element(By.NAME, self.value)
        if self.selector == "class":
            return driver.find_element(By.CLASS_NAME, self.value)

    def send_keys(self, driver, keys):
        """
        Sends keys or text to the element found in the Selenium driver object.

        Args:
            driver: The Selenium driver object.
            keys: The keys or text to send to the element.
        """
        self.find_element(driver).send_keys(keys)

    def click(self, driver):
        """
        Performs a click action on the element found in the Selenium driver object.

        Args:
            driver: The Selenium driver object.
        """
        self.find_element(driver).click()


@dataclass
class AccountOverviewSchema:
    """
    Represents a schema for an account overview.

    Attributes:
        items (Element): Element representing all account elements.
        account_name (Element): Element representing the account name.
        account_link (Element): anchor to the account page
    """

    items: Element
    account_name: Element
    account_link: Element


@dataclass
class AccountSchema:
    """
    Represents a schema for an account.

    Attributes:
        table (Element): Container of all transactions.
        rows (Element): All transaction rows.
        date (Element): Transaction date.
        type (Element): Transaction type.
        desc (Element): Transaction description.
        amount (Element): Transaction amount.
    """

    table: Element
    rows: Element
    date: Element
    type: Element
    desc: Element
    amount: Element


@dataclass
class TwoFactorSchema:
    """
    Represents a schema for 2-factor authentication.

    Attributes:
        tf_factor_url (str): URL for the 2-factor screen for test conditions.
        tf_continue (Element): Element representing the button to submit the 2-factor request.
        tf_pass_field (Element): Element representing the input field for the 2-factor password.
        tf_submit (Element): Element representing the button to submit the 2-factor input.
    """

    tf_factor_url: str
    tf_continue: Element
    tf_pass_field: Element
    tf_submit: Element


@dataclass
class LoginSchema:
    """
    Represents a schema for login credentials.

    Attributes:
        login_url (str): URL of the login page.
        user_field (Element): Element representing the input field for the username.
        pass_field (Element): Element representing the input field for the password.
        submit (Element): Element representing the button to submit the login credentials.
    """

    login_url: str
    user_field: Element
    pass_field: Element
    submit: Element


@dataclass
class BankSchema:
    """
    Represents a schema for a bank.

    Attributes:
        login_schema (LoginSchema, optional): Login schema for the bank. Defaults to None.
        two_factor_schema (TwoFactorSchema, optional): Two-factor authentication schema for the bank. Defaults to None.
        overview_schema (AccountOverviewSchema, optional): Schema for the account overview. Defaults to None.
        checking_schema (AccountSchema, optional): Schema for the checking account. Defaults to None.
        liability_schema (AccountSchema, optional): Schema for the liability account. Defaults to None.
    """

    login_schema: LoginSchema = (None,)
    two_factor_schema: TwoFactorSchema = (None,)
    overview_schema: AccountOverviewSchema = None
    checking_schema: AccountSchema = (None,)
    liability_schema: AccountSchema = (None,)
