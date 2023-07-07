
# Bank Scraper
Extensible scraping package to gather personal transaction information from a variety of Banks. Create a configuration based on your bank's page layouts and scrape your transactions.

Create Bank objects to scrape and store bank information.
```python
from bank_scraper import Bank

boa = Bank("Bank of America", username, password, schema=BOA_schema)
```
Create a scraping object, create accounts, and scrape transactions.
```python
scraper = boa.generate_scraper()
scraper.login()
```
Scrape accounts from account overview page.
	  
```python
accounts = scraper.scrape_overview() 
first_account = boa.accounts[0]
```
scrape the first account for transactions
```python
transactions = scraper.scrape_account(first_account)  
```
## Configurations
Configure *your* scraper to work with *your* bank account.

Configurations are a collection of page schemas that identify the buttons and fields used to login and access your account. 

E.g. Create a schema for Bank of America's login page. All you have to do is input the url, and selectors for the username and password fields, and the submit button.
```python
BOA_login  =  LoginSchema(
    "https://bankofamerica.com/login/",
    Element("input",  "id",  "enterID-input"),
    Element("input",  "id",  "tlpvt-passcode-input"),
    Element("button",  "name",  "enter-online-id-submit")
)
```
All schemas come together in a bank configuration you can use to create a banking object for your banking sessions.
```python
your_bank_schema = BankSchema(
    login_schema=your_login,
    two_factor_schema=your_two_factor,
    overview_schema=your_overview,
    checking_schema=your_checking,
    liability_schema=your_liability,
)
```

Default configurations for Bank of America and Discover are available.
