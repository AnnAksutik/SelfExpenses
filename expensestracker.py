import datetime

import uuid

import random

class Expense:
    def __init__(self,name = 'Useless', category = None,amount = None):
        self.name = name
        self.expense_id = uuid.uuid4()
        self.category = category
        self.amount = amount
        self.expense_time = datetime.datetime.now()

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add(self,expense):
        if isinstance(expense, Expense):
            self.expenses.append(expense)
        else:
            raise TypeError ('The variable must be Expense type')

    def get_all(self):
        return self.expenses

    def get_expense_id(self,manual_expense_id):
        for expense_stage in range(len(self.expenses)):
            if self.expenses[expense_stage].expense_id == manual_expense_id:
                return expense_stage

    def remove(self,expense_id):
        del self.expenses[self.get_expense_id(expense_id)]


    def get_stats(self):
        statist = {}
        for expense in self.expenses:
            statist[expense.category] = statist.get(expense.category,[]) + expense.amount
        for key,values in statist:
            print(f'{key}:{sum(statist[key])/len(statist[key])}',sep = '\n')

    def generate(self,custom_number):

        possible_expenses = {'Travel': ['Visa','Tickets','Insurance'],
                             'Food': ['Grocery','Sweets','Dairy products'],
                             'Living': ['Rent','Repair','Furniture','Utility bills'],
                             'Clothes':['Shoes','Outerwear','Underwear'],
                             'Transport': ['Underground','Bus','Uber'],
                             'Entertainment': ['Sightseeing', 'Restaurant', 'Bar','Friends meeting'],
                             'Sport': ['Gym','Swimming pool', 'Ice rink']
                             }
        for _ in range(custom_number):
            new_expense = Expense()
            new_expense.category = random.choice(possible_expenses.keys())
            new_expense.name = random.choice(possible_expenses[new_expense.category])
            new_expense.amount = random.uniform(0,10000000)

            self.add(new_expense)
