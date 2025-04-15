import pytest
from app.calculations import add, subtract, multiply,divide

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