class Transaction:
    """
    The transaction object has date, amount and description as class attributes
    """

    def __init__(self, datum, amount, description):
        self.datum = datum
        self.amount = amount
        self.description = description

    def __str__(self):
        return f"Date: {self.datum}, Amount: {self.amount}, Description: {self.description}"