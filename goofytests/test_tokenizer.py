
from goofy.goofy_tokenizer import GoofyTokenizer, TokenType

def test_tokenizer_returns_correct_length():
    test_lines = ["SHOVE", "3", "FREEZE"]
    
    tokenizer = GoofyTokenizer(test_lines)
    
    tokens = tokenizer.tokenize()
    
    assert len(tokens) == 3
    
def test_tokenizer_assigns_correct_value():
    test_lines = ["SHOVE", "3", "FREEZE"]
    
    tokenizer = GoofyTokenizer(test_lines)
      
    tokens = tokenizer.tokenize()
    
    passed = True
    
    for i in range(len(tokens)):
        if test_lines[i] != tokens[i].value:
            passed = False
            
    assert passed
    
def test_tokenizer_assigns_correct_type_1():
    test_lines = ["SHOVE", "3", "FREEZE"]
    
    expected_types = [TokenType.OPCODE, TokenType.INT_LITERAL, TokenType.OPCODE]
    
    tokenizer = GoofyTokenizer(test_lines)
    
    tokens = tokenizer.tokenize()
    
    passed = True
    
    for i in range(len(tokens)):
        if expected_types[i].name != tokens[i].type.name:
            passed = False
            
    assert passed
    
def test_tokenizer_assigns_correct_type_2():
    test_lines = ["SHOVE 3", "GLUE", "SHOVE 5", "YEET", "FREEZE"]
    
    expected_types = [TokenType.OPCODE, TokenType.INT_LITERAL, TokenType.OPCODE, 
                      TokenType.OPCODE, TokenType.INT_LITERAL, TokenType.OPCODE, 
                      TokenType.OPCODE]
    
    tokenizer = GoofyTokenizer(test_lines)
    
    tokens = tokenizer.tokenize()
    
    passed = True
    
    for i in range(len(tokens)):
        if expected_types[i].name != tokens[i].type.name:
            passed = False
            
    assert passed
    
def test_tokenizer_assigns_correct_type_3():
    test_lines = ["HOP > 3", "GLUE", "SHOVE 5", "YEET", "FREEZE"]
    
    expected_types = [TokenType.OPCODE, TokenType.CONDITIONAL, TokenType.INT_LITERAL, 
                      TokenType.OPCODE, TokenType.OPCODE, TokenType.INT_LITERAL, 
                      TokenType.OPCODE, TokenType.OPCODE]
    
    tokenizer = GoofyTokenizer(test_lines)
    
    tokens = tokenizer.tokenize()
    
    passed = True
    
    for i in range(len(tokens)):
        if expected_types[i].name != tokens[i].type.name:
            passed = False
            
    assert passed
    
def test_tokenizer_assigns_correct_type_when_string_has_space():

    test_lines = ["SNOOP \"two words\""]
    
    expected_types = [TokenType.OPCODE, TokenType.STRING_LITERAL]
    
    tokenizer = GoofyTokenizer(test_lines)
    
    tokens = tokenizer.tokenize()
    
    passed = True
    
    for i in range(len(tokens)):
        if expected_types[i].name != tokens[i].type.name:
            passed = False
            
    assert passed    
    
def test_tokenizer_assigns_correct_type_when_string_has_no_space():

    test_lines = ["SNOOP \"oneword\""]
    
    expected_types = [TokenType.OPCODE, TokenType.STRING_LITERAL]
    
    tokenizer = GoofyTokenizer(test_lines)
    
    tokens = tokenizer.tokenize()
    
    passed = True
    
    for i in range(len(tokens)):
        if expected_types[i].name != tokens[i].type.name:
            passed = False
            
    assert passed        