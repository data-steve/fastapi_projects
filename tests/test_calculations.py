from app.calculations import add, subtract, multiply,divide

def test_add():
    print("testing add function")  
    assert add(3, 5) ==8
    
def test_subtract():
    assert subtract(5, 3) ==2
    
def test_multiply():
    assert multiply(3,4)== 12
    
def test_divide():
    assert divide(12,4)==3