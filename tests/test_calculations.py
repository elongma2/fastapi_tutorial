import pytest
from app.calculations import add, BankAccount


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

#another way to add test
@pytest.mark.parametrize("a,b,expected", [(5,3,8),(7,1,8),(12,4,16)])
def test_add(a,b,expected):
    sum = add(a,b)
    assert sum == expected


def test_bank_set_initinial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_deposit():
    bank_account = BankAccount()
    bank_account.deposit(1000)
    assert bank_account.balance == 1000