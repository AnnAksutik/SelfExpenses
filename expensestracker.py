class Expense:
    def __init__(self,id,category,amount,expense_time):
        self.id = id
        self.category = category
        self.amount = amount
        self.expense_time = expense_time

class ExpenseTracker:
    def __init__(self):
        self.values = []

    def add(self,expense):
        if isinstance(expense, Expense):
            self.values.add(expense)
        else:
            raise TypeError('The variable must be Expense type')

    def get_all(self):
        return self.values

    def remove(self,expense_id):
        self.values
        pass

    def get_stats():
        pass

    def generate():
        pass
