import os

from dotenv import load_dotenv

from .schemas import Element, AccountSchema

load_dotenv()
# https://bankofamerica.com/login/


"""
BOA SETUP
"""

"""Checking account layout"""
BOA_checking = AccountSchema(
    Element("table", selector="id", value="txn-activity-table"),
    Element("tr", selector="class", value="activity-row", find_all=True),
    Element("td", selector="class", value="date-cell"),
    Element("td", selector="class", value="type-cell"),
    Element("td", selector="class", value="desc-cell"),
    Element("td", selector="class", value="amount-cell"),
)
"""Credit account layour"""
BOA_liability = AccountSchema(
    Element("table", selector="id", value="transactions"),
    Element("tr", find_all=True),
    Element("td", selector="class", value="trans-date-cell"),
    Element("td", selector="class", value="trans-type-cell"),
    Element("td", selector="class", value="trans-desc-cell"),
    Element("td", selector="class", value="trans-amount-cell"),
)


# u = os.environ.get("BOA_USER")
# p = os.environ.get("BOA_PASS")
# bofa = Bank("Bank of America", "https://bankofamerica.com/login/", u, p)
