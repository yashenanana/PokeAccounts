from datetime import datetime

from TransactionAdmin import TransactionAdmin

class UI:

    def __init__(self):
        """
        Initialises a "UI" instance:
        - Initialises an instance of TransactionAdmin to be used
        """
        self.tAdmin = TransactionAdmin()

    def firstDisplay(self):
        """
        The main menu where the user is able to choose between the programs different functionalities.
        If input does not correspond to the different cases, the method will call on itself again.
        """
        print("Welcome Trainer! \nThe first step to catching 'em all \nis proper finance management!\n--------------------------------")
        print("1 - Add Transaction")
        print("2 - Filter by Category")
        print("3 - Search by Description")
        print("4 - Show All Transactions")
        print("5 - Exit")
        x = input("What would you like to do today?\n")
        match x:
            case "1":
                self.addTransactionDisplay()
            case "2":
                self.filterTransactionDisplay()
            case "3":
                self.searchTransactionDisplay()
            case "4":
                self.showAllDisplay()
            case "5":
                print("We'll see you again.")
                exit()
            case _:
                print("Invalid input\n")
                self.firstDisplay()


    def addTransactionDisplay(self):
        """
        Method used to add transactions to the TransactionAdmin instance. A success message will be displayed if no errors are found followed by a call of the firstDisplay() method.
        If invalid category is chosen or if negative amount is given, a special error message will be displayed.
        Else, a generic error message will be displayed.

        """
        print("Please Fill Out The Following")
        try:
            category = int(input("Pick a Category \n1 - Quests \n2 - Trainer Battles \n3 - PokeBalls \n4 - Potions \n5 - Items\n6 - Main Menu\n"))
            if category == 6:
                self.firstDisplay()
            if category not in range(1,6):
                raise ValueError("Please choose a category")
            amount = float(input("Amount of Transaction:\n"))
            if(amount<0):
                raise ValueError("Please enter a non-negative price")
            description = input("Description of Transaction:\n")
            dateString = input("Date of Transaction Eg.2024-03-07 \n")
            datum = datetime.strptime(dateString, '%Y-%m-%d').date()
            self.tAdmin.addTransaction(category, datum, amount, description)
        except (ValueError, TypeError) as e:
            if "Please" not in str(e):
                print("Invalid input. Please try again\n")
            else:
                print(str(e))
            self.addTransactionDisplay()
        else:
            print("Transaction added successfully!\n")
        self.firstDisplay()


    def filterTransactionDisplay(self):
        """
        Method used to display transactions of a specific category followed by a call of the firstDisplay() method.
        If invalid category is chosen, a special error message will be displayed.
        Else, a generic error message will be displayed.

        """
        print("Transaction Filter Menu")
        try:
            category = int(input("Pick a Category \n1 - Quests \n2 - Trainer Battles \n3 - PokeBalls \n4 - Potions \n5 - Items\n6 - Main Menu\n"))
            if category == 6:
                self.firstDisplay()
            if category not in range(1, 6):
                raise ValueError("Please choose a category")
            print(self.tAdmin.filterTransaction(category),"\n")
        except (ValueError, TypeError) as e:
            if "Please" not in str(e):
                print("Invalid input. Please try again\n")
            else:
                print(str(e))
            self.filterTransactionDisplay()
        self.firstDisplay()


    def searchTransactionDisplay(self):
        """
        Method used to display all existing transactions for a specific description. firstDisplay() method is called leading user to main menu.
        If description string is empty, a special error message will be displayed and the method will call on itself again.

        """
        print("Search Transaction Menu")
        description = input("Enter a Description: \n")
        try:
            if description== "" :
                raise ValueError("Please enter a description")
        except ValueError as e:
            print(e)
            self.searchTransactionDisplay()
        print(self.tAdmin.findTransaction(description))
        self.firstDisplay()


    def showAllDisplay(self):
        """
        Method used to display a summary of transactions followed by breakdown of all existing transactions.
        Zero Division Error from the generateBarChart() method shows that there are no transactions to be displayed.
        """
        s = ""
        try:
            s += self.tAdmin.__str__()
        except ZeroDivisionError:
            print("There are no existing transactions\n")
            self.firstDisplay()
        print(s)
        self.firstDisplay()