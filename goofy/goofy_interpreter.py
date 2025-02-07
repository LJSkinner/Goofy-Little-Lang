from enum import Enum
from goofy.goofy_tokenizer import GoofyTokenizer, TokenType
import logging

LOGGER = logging.getLogger(__name__)

class SupportedOpcodes(Enum):
    """ Represents the opcodes which
    are supported in goofy.
    """
    # Goofy's equivalent of PUSH, pushes a int onto the stack.
    SHOVE = "SHOVE"
    
    # Goofy's equivalent of SUB, pops two values off the stack and subtracts them, then pushes the result.
    YEET = "YEET"
    
    # Goofy's equivalent of ADD, pops two values off the stack and adds them, then pushes the result.
    GLUE = "GLUE"
    
    # Goofy's equivalent of PRINT, prints a string to stdout. 
    YELL = "YELL"
    
    # Goofy's equivalent of READ, reads a number from stdin and pushes onto the stack
    SNOOP = "SNOOP"
    
    # Goofy's equivalent of MUL, pops two values off the stack and multiplies them, then pushes the result.
    MOOSH = "MOOSH"
    
    # Goofy's equivalent of DIV, pops two values off the stack and divides them, then pushes the result.
    SNIP = "SNIP"
    
    # Goofy's equivalent of HALT, stops the execution at this point.
    FREEZE = "FREEZE"
    
    # Goofy's equivalent of JUMP, will jump based on a condition.
    BOUNCE = "BOUNCE"
    
class GoofyInterpreter:
    """ Responsible for doing the interpretation
    of a goofy lang file, determining which operations
    to perform.
    """
    def __init__(self, file_lines: list[str]):
        self._stack: list[int] = []
        
        self.tokenizer = GoofyTokenizer(file_lines)
        
    def interpret(self) -> bool:
        """ Responsible for interpreting the goofy file
        lang that was provided when the interpreter object
        was created. 

        Returns:
            bool: whether the interpreter was successful at parsing the tokens or not
        """
        tokens = self.tokenizer.tokenize()
        
        interpreting_succeded = True
        
        # We should never hit this case since this is handled when the file is read, but just in case something weird happens I've left it here.
        if len(tokens) == 0: 
            LOGGER.error("The token count is 0, which means the file provided was empty. Try another file")
            
            return not interpreting_succeded
        
        i = 0
        
        while i < len(tokens):
           token = tokens[i]
          
           if token.type == TokenType.OPCODE:
               if not SupportedOpcodes.__contains__(token.value):
                   LOGGER.error("Token %d:%s contains an unsupported opcode", i + 1, token.value)
                   
                   return not interpreting_succeded
               
               # Where actual interpretation work begins: 
               match token.value:
                   
                   case SupportedOpcodes.SHOVE.value:
                        if len(tokens) > i + 1:
                         next_token = tokens[i + 1]
                        
                         if not next_token.type == TokenType.INT_LITERAL:
                            LOGGER.error("Token %d:%s is not an integer. SHOVE must be supplied an integer. Ex: SHOVE 3", i + 1, next_token.value)
                            
                            return not interpreting_succeded
                        
                         self.stack.append(int(next_token.value))  
                          
                        else:
                            LOGGER.error("There was no token to the right of SHOVE. Please make sure you remember to add a number")
                            
                            return not interpreting_succeded
                   
                   case SupportedOpcodes.BOUNCE.value:
                       if len(tokens) > i + 3:
                           conditional_token = tokens[i + 1]
                           
                           comparison_token = tokens[i + 2]
                           
                           label_definition_token = tokens[i + 3]
                        
                           if not conditional_token.type == TokenType.CONDITIONAL:
                            LOGGER.error("There as no conditional token provided to the right of BOUNCE. Ex: BOUNCE > 0 #L1")
                            
                            return not interpreting_succeded
                        
                           if not comparison_token.type == TokenType.INT_LITERAL:
                            LOGGER.error("The comparison token provided for BOUNCE was not an integer. Ex: BOUNCE > 0 #L1")
                            
                            return not interpreting_succeded
                        
                           if not label_definition_token.type == TokenType.LABEL_DEFINITION:
                            LOGGER.error("The label definition token provided for BOUNCE was not correct. Must contain a '#' before label name. Ex: BOUNCE > 0 #L1")
                            
                            return not interpreting_succeded
                        
                           if self.is_stack_empty():
                            LOGGER.error("There is no value on the stack for bounce to compare to. Make sure you add a value to the stack. Ex: SHOVE 10 | SNOOP")
                            
                            return not interpreting_succeded
                        
                           top = self.get_stack_top()
                           
                           expression_result = eval(f"{top} {conditional_token.value} {comparison_token.value}")
                           
                           if not expression_result:
                               # skip the bounce statement if it's false
                               i += 4 
                               
                               continue
                            
                           label_start_tokens = self.tokenizer.get_tokens_by_type(TokenType.LABEL_START)
                           
                           found_label_start = False
                           
                           for label_start_token in label_start_tokens:
                               if label_definition_token.value.strip("#") == label_start_token.value.strip(":"):
                                   i = tokens.index(label_start_token)
                                   
                                   found_label_start = True
                                   
                                   break
                                   
                           if found_label_start:
                               continue
                           else:         
                               LOGGER.error("There was no label start found for label definition token: %s. Did you forget it?", label_definition_token.value) 
                               
                               return not interpreting_succeded   
                       else:
                            LOGGER.error("There was a missing token to the right of BOUNCE. Please review your code")
                            
                            return not interpreting_succeded   
                           
                    
                   case SupportedOpcodes.FREEZE.value:
                       return interpreting_succeded
                        
                   case SupportedOpcodes.YELL.value:
                       if len(tokens) > i + 1:
                           next_token = tokens[i + 1]
                           
                           print(next_token.value.strip("\""))
                    
                       else:
                           LOGGER.error("There was no token to the right of YELL. Please make sure you remember to add a value")
                           
                           return not interpreting_succeded
                   
                   case SupportedOpcodes.SNOOP.value:
                       user_input = input()
                       
                       if not str.isnumeric(user_input):
                           LOGGER.error("The input entered was not a number, please supply a number")
                           
                           return not interpreting_succeded
                       
                       self.stack.append(int(user_input))
                       
                   case SupportedOpcodes.YEET.value:
                        if len(self.stack) < 2:
                            LOGGER.error("The stack does not contain at least two values to YEET. Ex: SHOVE 3 SHOVE 4 YEET")
                            
                            return not interpreting_succeded
                        
                        first = self.stack.pop()
                        
                        second = self.stack.pop()
                        
                        result = first - second
                        
                        self.stack.append(result)
                        
                   case SupportedOpcodes.GLUE.value:
                        if len(self.stack) < 2:
                            LOGGER.error("The stack does not contain at least two values to GLUE. Ex: SHOVE 3 SHOVE 4 GLUE")
                            
                            return not interpreting_succeded
                        
                        first = self.stack.pop()
                        
                        second = self.stack.pop()
                        
                        result = first + second
                        
                        self.stack.append(result)
                  
                   case SupportedOpcodes.MOOSH.value:
                        if len(self.stack) < 2:
                            LOGGER.error("The stack does not contain at least two values to MOOSH. Ex: SHOVE 3 SHOVE 4 MOOSH")
                            
                            return not interpreting_succeded
                        
                        first = self.stack.pop()
                        
                        second = self.stack.pop()
                        
                        result = first * second
                        
                        self.stack.append(result)
                        
                   case SupportedOpcodes.SNIP.value:
                        if len(self.stack) < 2:
                            LOGGER.error("The stack does not contain at least two values to SNIP. Ex: SHOVE 3 SHOVE 4 SNIP")
                            
                            return not interpreting_succeded
                        
                        first = self.stack.pop()
                        
                        second = self.stack.pop()
                        
                        if second == 0:
                            LOGGER.error("Attempt to divide by zero, please review your program flow.")
                            
                            return not interpreting_succeded
                        
                        result = int(first / second)
                        
                        self.stack.append(result)
        
           elif token.type == TokenType.UNKNOWN:
               LOGGER.error("Token %d:%s is an unknown token type. Please review the provided source", i + 1, token.value)
               
               return not interpreting_succeded
           
           i += 1
               
        return interpreting_succeded    
                                     
    @property
    def stack(self) -> list[int]:
        """ Returns the current stack which
        contains the values added during interpretation.

        Returns:
            list[int]: the current stack which contains 
            the values added during interpretation.
        """
        return self._stack    
    
    def get_stack_top(self) -> int:
        """ Gets the element at the top of the stack

        Returns:
            int: the element currently at the top of the stack
        """
        return self.stack[len(self.stack) - 1] 
    
    def is_stack_empty(self) -> bool:
        """ Deterimens whether the stack is empty or not.

        Returns:
            bool: true if the stack is empty, false otherwise
        """
        return len(self.stack) == 0