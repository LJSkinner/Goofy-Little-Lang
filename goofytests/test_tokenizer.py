
from goofy.goofy_tokenizer import Tokenizer, TokenType

def func(x):
    return x + 1

def test_tokenizer_returns_correct_length():
    # ASSIGN
    test_lines = ["SHOVE", "3", "FREEZE"]
    
    tokenizer = Tokenizer(test_lines)
    
    # DO
    tokens = tokenizer.tokenize()
    
    # ASSERT
    assert len(tokens) == 3
    
    
def test_tokenizer_assigns_correct_value():
    # ASSIGN
    test_lines = ["SHOVE", "3", "FREEZE"]
    
    tokenizer = Tokenizer(test_lines)
      
    # DO
    tokens = tokenizer.tokenize()
    
    passed = True
    
    for i in range(len(tokens)):
        if test_lines[i] != tokens[i].value:
            passed = False
            
    assert passed
    
def test_tokenizer_assings_correct_type_1():
    # ASSIGN
    test_lines = ["SHOVE", "3", "FREEZE"]
    
    expected_types = [TokenType.OPCODE, TokenType.INT_LITERAL, TokenType.OPCODE]
    
    tokenizer = Tokenizer(test_lines)
    
    # DO
    tokens = tokenizer.tokenize()
    
    passed = True
    
    for i in range(len(tokens)):
        if expected_types[i].name != tokens[i].type.name:
            passed = False
            
    assert passed
    
def test_tokenizer_assings_correct_type_2():
    # ASSIGN
    test_lines = ["SHOVE 3", "GLUE", "SHOVE 5", "YEET", "FREEZE"]
    
    expected_types = [TokenType.OPCODE, TokenType.INT_LITERAL, TokenType.OPCODE, 
                      TokenType.OPCODE, TokenType.INT_LITERAL, TokenType.OPCODE, 
                      TokenType.OPCODE]
    
    tokenizer = Tokenizer(test_lines)
    
    # DO
    tokens = tokenizer.tokenize()
    
    passed = True
    
    for i in range(len(tokens)):
        if expected_types[i].name != tokens[i].type.name:
            passed = False
            
    assert passed
    
def test_tokenizer_assings_correct_type_3():
    # ASSIGN
    test_lines = ["HOP > 3", "GLUE", "SHOVE 5", "YEET", "FREEZE"]
    
    expected_types = [TokenType.OPCODE, TokenType.CONDITIONAL, TokenType.INT_LITERAL, 
                      TokenType.OPCODE, TokenType.OPCODE, TokenType.INT_LITERAL, 
                      TokenType.OPCODE, TokenType.OPCODE]
    
    tokenizer = Tokenizer(test_lines)
    
    # DO
    tokens = tokenizer.tokenize()
    
    passed = True
    
    for i in range(len(tokens)):
        if expected_types[i].name != tokens[i].type.name:
            passed = False
            
    assert passed
    