class Bank_Account():
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance

    def __repr__(self):
        return f'Owner: {self.owner}, Balance: {self.balance}'

    def deposit(self, balance):
        self.balance = self.balance + balance
        print("Deposit was accepted")
    
    def withdraw(self, wd_balance):
        if self.balance - wd_balance >= 0:
            self.balance = self.balance - wd_balance
            print("Withdrawal successful")
        else: 
            print("Funds not available")
        

# Test

# 1. Instantiate the class
ngoc_account = Bank_Account('Ngoc Mai', 1000)

# 2. Print the object
print(ngoc_account)

# 3. Show the account
ngoc_account.owner

# 4. Show the balance
ngoc_account.balance

#5. Make a series of deposits and withdrawals
ngoc_account.deposit(200)
print(ngoc_account.balance)

ngoc_account.withdraw(700)
print(ngoc_account.balance)

# 6. Make a withdraw that exceeds the available balance
ngoc_account.withdraw(800)
print(ngoc_account.balance)