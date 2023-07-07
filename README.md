
# Bank Scraper
Extensible scraping package to gather personal transaction information from a variety of Banks. Create a configuration based on your bank's page layouts and scrape your transactions.

Create Bank objects to scrape and store bank information.

    from bank_scraper import Bank
    	
    bofa = Bank("Bank of America", username, password, schema=BOA_schema)

Create a scraping object, create accounts, and scrape transactions.

    scraper = bofa.generate_scraper()
    scraper.login()

Scrape accounts from account overview page.
	  

    accounts = scraper.scrape_overview() 

    first_account = bofa.accounts[0]

scrape the first account for transactions

    transactions = scraper.scrape_account(first_account)  

## Configurations
Configure *your* scraper to work with *your* bank account.

Configurations are a collection of page schemas used to identify the buttons and fields used to login and access your account. 

E.g. Create a schema for Bank of America's login page. All you have to do is input the url, and selectors for the username and password fields, and the submit button.

    BOA_login  =  LoginSchema(
	    "https://bankofamerica.com/login/",
	    Element("input",  "id",  "enterID-input"),
	    Element("input",  "id",  "tlpvt-passcode-input"),
	    Element("button",  "name",  "enter-online-id-submit")
    )
