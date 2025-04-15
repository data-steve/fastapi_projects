import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,5),
    (7,9,16),
    (14,3, 17)
])
def test_add(num1, num2, expected):
    print("testing add function")  
    assert add(num1, num2) ==expected

@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,1),
    (7,9,-2),
    (14,3, 11)
])  
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) ==expected

@pytest.mark.parametrize("num1, num2, expected",[
    (3,2,6),
    (14,2,28),
    (3,3, 9)
])   
def test_multiply(num1, num2, expected):
    assert multiply(num1, num2) ==expected

@pytest.mark.parametrize("num1, num2, expected",[
    (6,2,3),
    (14,2,7),
    (3,3, 1)
])     
def test_divide(num1, num2, expected):
    assert divide(num1, num2)==expected
    

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance==50
    
def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance ==0
    
def test_bank_withdraw(bank_account):
    bank_account.withdraw(15)
    assert bank_account.balance == 35
    
def test_bank_deposit(bank_account):
    bank_account.deposit(15)
    assert bank_account.balance == 65
    
def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert int(bank_account.balance) == 55

@pytest.mark.parametrize("deposit, withdrew, expected",[
        (50, 24, 26),
        (1500, 1200, 300),
        (110, 100, 10)
])
def test_bank_transaction(zero_bank_account, deposit, withdrew, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance==expected
    
    
def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
    