from schemas import (
    Element,
    AccountSchema,
    LoginSchema,
    TwoFactorSchema,
    BankSchema,
    AccountOverviewSchema,
)

#  BOA SETUP
BOA_checking = AccountSchema(
    Element("table", selector="id", value="txn-activity-table"),
    Element("tr", selector="class", value="activity-row", find_all=True),
    Element("td", selector="class", value="date-cell"),
    Element("td", selector="class", value="type-cell"),
    Element("td", selector="class", value="desc-cell"),
    Element("td", selector="class", value="amount-cell"),
)
BOA_liability = AccountSchema(
    Element("table", selector="id", value="transactions"),
    Element("tr", find_all=True),
    Element("td", selector="class", value="trans-date-cell"),
    Element("td", selector="class", value="trans-type-cell"),
    Element("td", selector="class", value="trans-desc-cell"),
    Element("td", selector="class", value="trans-amount-cell"),
)

BOA_overview = AccountOverviewSchema(
    Element("div", "class", "AccountItem", find_all=True),
    Element("span", "class", "AccountName"),
    Element("a"),
)

BOA_login = LoginSchema(
    "https://bankofamerica.com/login/",
    Element("input", "id", "enterID-input"),
    Element("input", "id", "tlpvt-passcode-input"),
    Element("button", "name", "enter-online-id-submit"),
)

BOA_two_factor = TwoFactorSchema(
    "https://secure.bankofamerica.com/login/sign-in/signOnSuccessRedirect.go",
    Element("button", "id", "btnARContinue"),
    Element("input", "class", "authcode"),
    Element("button", "id", "continue-auth-number"),
)

BOA_schema = BankSchema(
    login_schema=BOA_login,
    two_factor_schema=BOA_two_factor,
    overview_schema=BOA_overview,
    checking_schema=BOA_checking,
    liability_schema=BOA_liability,
)


# Discover Setup
Discover_login = LoginSchema(
    "https://portal.discover.com/customersvcs/universalLogin/ac_main",
    Element("input", "id", "userid-content"),
    Element("input", "id", "password-content"),
    Element("input", "id", "password-content"),
)

Discover_two_factor = TwoFactorSchema(
    "https://card.discover.com/cardmembersvcs/strongauth/app/sa_main",
    Element("input", "value", "Continue"),
    Element("input", "id", "codeEntry"),
    Element("input", "value", "Submit"),
)

Discover_overview = AccountOverviewSchema(
    Element("div", "class", "recent-activity-button-container", find_all=True),
    Element("a", "data-testid", "at-allactivity-statments"),
    Element("a", "data-testid", "at-allactivity-statments"),
)

Discover_liability = AccountSchema(
    Element("table", selector="id", value="transactionTbl"),
    Element("tr", find_all=True),
    Element("td", selector="class", value="transaction-date"),
    Element("td", selector="class", value="merchant-container"),
    Element("td", selector="class", value="merchant-container"),
    Element("td", selector="class", value="transaction-amount"),
)

Discover_schema = BankSchema(
    login_schema=Discover_login,
    two_factor_schema=Discover_two_factor,
    overview_schema=Discover_overview,
    checking_schema=None,
    liability_schema=Discover_liability,
)
