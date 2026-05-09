import json
from datetime import datetime
from enum import Enum
from json import JSONDecodeError
import termcharts as tc

from Transaction import Transaction

class Category(Enum):
    """
    The Category enum class defines various categories used to classify transactions in the financial manager system.
    Enum Members:
        Quests (1) : Represents income earned from completing quests.
        TrainerBattles (2) : Represents income earned from defeating fellow trainers.
        Pokeballs (3) : Represents expenses from purchasing PokéBalls.
        Potions (4) : Represents expenses from purchasing potions.
        Items (5) : Represents expenses from purchasing miscellaneous items.
    """
    Quests = 1
    TrainerBattles = 2
    PokeBalls = 3
    Potions = 4
    Items = 5



class TransactionAdmin:
    """
    The `TransactionAdmin` class serves as a manager for financial transactions.
    It organizes transactions into categories, tracks income and expenses, and provides functionality for storing, retrieving, filtering, and analyzing data.
    """

    def __init__(self):
        """
        Initializes a `TransactionAdmin` instance:
        - Creates a `transactions` dictionary, initializing empty lists for each category.
        - Initializes `income` and `expense` to zero.
        - Attempts to load transactions from a JSON file. If the file cannot be decoded, it initializes the file.

        """
        self.transactions = {category: [] for category in Category}
        self.income = 0
        self.expense = 0
        try:
           self.load_from_json("transactions.json")
        except JSONDecodeError:
           self.save_to_json("transactions.json")


    def matchCategory(self, category):
        """
        A helper function to match user input to a Category enum
        Args:
            category: an integer from the user

        Returns: The list corresponding to the category.

        """
        try:
            return self.transactions[Category(category)]
        except (KeyError, ValueError):
            return []


    def addTransaction(self, category, datum, amount, description):
        """
        Adds a transaction to the specified category list and updates income or expense totals.
        matchCategory() helper function used to append the transaction to the correct list.
        Args:
            category: An integer representing the transaction category.
            datum: The date of transaction.
            amount: The amount of transaction.
            description: A brief description of the transaction.

        """
        list = self.matchCategory(category)
        list.append(Transaction(datum, amount, description))
        if category in {1,2}:

            self.income += amount
        elif category in {3 , 4 , 5}:
            self.expense += amount

        self. save_to_json("transactions.json")


    def findTransaction(self, description):
        """
        Finds all transactions containing a specified description.
        2 for-loops are used to iterate through all existing transactions. The first for-loop is used to iterate through
        the different categories. The second for-loop is used to iterate through the list of respective categories
        Args:
            description: A string to search for in transaction descriptions.

        Returns:  A string summary of matching transactions and their total sum.

        """
        s = f"Transactions containing: {description}\n"
        sum = 0
        for x in self.transactions.keys():
            for y in self.transactions[x]:
                if description in y.description:
                    s+=f"{y}, \n"
                    sum += y.amount
        s += f"Total Sum : {sum}"
        return s


    def filterTransaction(self, category):
        """
        Filters transactions to a specific category and provides a summary.
        matchCategory() helper function used to determine the correct list.
        Total is used as a counter variable. If the variable post for-loop is still 0, this indicates there are no
        transactions in that category.
        Args:
            category: An integer representing the transaction category.

        Returns: A summary string of transactions and their total amount, or a message indicating no transactions exist.

        """
        sum = 0
        total = 0
        list = self.matchCategory(int(category))
        s=""
        for transaction in list:
            s+= f"{transaction}, \n"
            sum += transaction.amount
            total +=1
        s+= f"Total Sum : {sum}"
        if(total == 0):
            return "No Transactions"
        return s


    def save_to_json(self, filename):
        """
        Saves all transactions, income, and expense data to a JSON file.
        Args:
            filename: The name of the file to save the data.

        """
        data = {
            "transactions": {
                category.name: [
                    {
                        "datum": transaction.datum.strftime('%Y-%m-%d'),
                        "amount": transaction.amount,
                        "description": transaction.description
                    }
                    for transaction in transactions
                ]
                for category, transactions in self.transactions.items()
            },
            "income":self.income,
            "expense":self.expense
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)


    def load_from_json(self, filename):
        """
        Loads transactions, income, and expense data from a JSON file.
        Args:
            filename: The name of the file to load data from.

        """
        with open(filename, 'r') as file:
            data = json.load(file)

        self.transactions = {Category[category]: [
            Transaction(
                datetime.strptime(t["datum"], '%Y-%m-%d').date(),
                t["amount"],
                t["description"]
            )
            for t in transactions
        ] for category, transactions in data["transactions"].items()}

        self.income = data["income"]
        self.expense = data["expense"]


    def generateBarChart(self):
        """
        Generates a bar chart visualization of the transaction data.
        A dictionary variable data containing the category as keys and the sum of each category as the corresponding
        value is initialised.
        A function from termcharts library accepts this variable as a parameter to generate the bar chart.

        Returns: A string representation of the chart.
        """
        data = {}
        for x in self.transactions.keys():
            sum = 0
            for y in self.transactions[x]:
                sum += y.amount
            data[x.name] = sum
        chart_pie = tc.bar(data, title="Trainer's Expenses")
        return chart_pie


    def __str__(self):
        """
        Generates a summary string for the `TransactionAdmin` instance.
        Returns: A string containing a summary of total income, expense, balance and a bar chart to visually represent the data, followed by detailed transaction breakdowns.
        """
        sum = self.income - self.expense
        s = ""
        s += f"------------------------------------\nSummary\nTotal Income: {self.income}\nTotal Expense: {self.expense}\nTotal Sum: {sum}\n"
        s += self.generateBarChart()
        for k, transactions in self.transactions.items():
            s += f"Category: {k.name} \nTransactions:\n"
            for transaction in transactions:
                s += f"{transaction} \n"
            s+="\n"
        return s