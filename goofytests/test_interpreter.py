from goofy.goofy_interpreter import GoofyInterpreter

def test_interpreter_unknown_opcode():
    test_lines = ["UNKNOWN"]
    
    interpreter = GoofyInterpreter(test_lines)
    
    success = interpreter.interpret()
    
    stack = interpreter.stack
    
    assert len(stack) == 0
    
    assert not success

def test_interpreter_stack_contains_correct_values():
    test_lines = ["SHOVE 3 SHOVE 4 SHOVE 5 SHOVE 6"]
    
    interpreter = GoofyInterpreter(test_lines)
    
    success = interpreter.interpret()
    
    stack = interpreter.stack
    
    assert len(stack) == 4
    
    assert stack[0] == 3
    assert stack[1] == 4
    assert stack[2] == 5
    assert stack[3] == 6
    
    assert success
    
def test_interpreter_stack_top_is_correct():
    test_lines = ["SHOVE 3 SHOVE 4 SHOVE 5 SHOVE 6"]
    
    interpreter = GoofyInterpreter(test_lines)
    
    success = interpreter.interpret()
    
    stack = interpreter.stack
    
    top_of_stack = stack[len(stack) - 1]
    
    assert top_of_stack == 6
    
    assert success
    
def test_interpreter_stack_is_empty():
    test_lines = [""]
    
    interpreter = GoofyInterpreter(test_lines)
    
    success = interpreter.interpret()
    
    stack = interpreter.stack
    
    assert len(stack) == 0
    
    assert not success


def test_interpreter_unknown_token():
    test_lines = ["^^^^"]
    
    interpreter = GoofyInterpreter(test_lines)
    
    success = interpreter.interpret()
    
    stack = interpreter.stack
    
    assert len(stack) == 0
    
    assert not success

def test_interpreter_stack_operation_shove():
    test_lines = ["SHOVE 3"]
    
    interpreter = GoofyInterpreter(test_lines)
    
    success = interpreter.interpret()
    
    stack = interpreter.stack
    
    assert len(stack) == 1
    
    assert stack[0] == 3
    
    assert success
    
def test_interpreter_stack_operation_shove_no_integer():
    test_lines = ["SHOVE"]
    
    interpreter = GoofyInterpreter(test_lines)
    
    success = interpreter.interpret()
    
    stack = interpreter.stack
    
    assert len(stack) == 0
    
    assert not success
    
def test_interpreter_stack_operation_shove_wrong_type_string():
    test_lines = ["SHOVE \"wdwdw\""]
    
    interpreter = GoofyInterpreter(test_lines)
    
    success = interpreter.interpret()
    
    stack = interpreter.stack
    
    assert len(stack) == 0
    
    assert not success

def test_interpreter_stack_operation_shove_unknown_token():
    test_lines = ["SHOVE ^^^^"]
    
    interpreter = GoofyInterpreter(test_lines)
    
    success = interpreter.interpret()
    
    stack = interpreter.stack
    
    assert len(stack) == 0
    
    assert not success
    