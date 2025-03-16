class Bank_Account():
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def __repr__(self):
        return f'Owner: {self.owner}, Balance: {self.balance}'

    def deposit(self, balance):
        return self.balance + balance
    
    def withdraw(self, balance):
        if self.balance - balance >= 0:
            return self.balance - balance

ngoc_account = Bank_Account('Ngoc Mai', 10000)
print(ngoc_account)
ngoc_account.withdraw(1000)
print(ngoc_account)