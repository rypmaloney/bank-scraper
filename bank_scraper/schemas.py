class AccountSchema:
    def __init__(self, table, rows, date, type_, desc, amount):
        self.table = table
        self.rows = rows
        self.date = date
        self.type = type_
        self.desc = desc
        self.amount = amount


class Element:
    def __init__(self, element, selector=None, value=None, find_all=False):
        self.element = element
        self.selector = selector
        self.value = value
        self.find_all = find_all
        self.recursive = True
        if element == "td":
            self.recursive = False

    def query(self, target):
        if self.find_all:
            return target.find_all(self.element, {self.selector: self.value})
        return target.find(
            self.element, {self.selector: self.value}, recursive=self.recursive
        )

    def text(self, target):
        return (
            self.query(target)
            .getText()
            .replace("$", "")
            .replace("\n", " ")
            .replace("Expand transaction for Transaction date:", "")
            .replace("Expand transaction", "")
            .strip()
        )
