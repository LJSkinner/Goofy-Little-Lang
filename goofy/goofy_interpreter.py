from enum import Enum
from goofy.goofy_tokenizer import GoofyTokenizer, TokenType, Token
import logging

LOGGER = logging.getLogger(__name__)

class SupportedOpcodes(Enum):
    """ Represents the opcodes which
    are supported in goofy.
    """
    # Goofy's equivalent of PUSH, pushes a int onto the stack.
    SHOVE = "SHOVE"
    
    # Goofy's equivalent of PRINT, prints a string to stdout. 
    YELL = "YELL"
    
    # Goofy's equivalent of READ, reads a number from stdin and pushes onto the stack
    SNOOP = "SNOOP"
    
    # Goofy's equivalent of SUB, pops two values off the stack and subtracts them, then pushes the result.
    YEET = "YEET"
    
    # Goofy's equivalent of ADD, pops two values off the stack and adds them, then pushes the result.
    GLUE = "GLUE"

    # Goofy's equivalent of MUL, pops two values off the stack and multiplies them, then pushes the result.
    MOOSH = "MOOSH"
    
    # Goofy's equivalent of DIV, pops two values off the stack and divides them, then pushes the result.
    SNIP = "SNIP"
    
    # Goofy's equivalent of JUMP, will jump based on a condition.
    BOUNCE = "BOUNCE"
    
    # Goofy's equivalent of HALT, stops the execution at this point.
    FREEZE = "FREEZE"

class GoofyInterpreter:
    """ Responsible for doing the interpretation
    of a goofy lang file, determining which operations
    to perform.
    """
    def __init__(self, file_lines: list[str]):
        self._stack: list[int] = []
        
        self.tokenizer = GoofyTokenizer(file_lines)
        
        self._index = 0
        
    @property
    def stack(self) -> list[int]:
        """ Returns the current stack which
        contains the values added during interpretation.

        Returns:
            list[int]: the current stack which contains 
            the values added during interpretation.
        """
        return self._stack   
    
    @property
    def index(self) -> int:
        """ Returns the current index of where
        the interpreter is at.

        Returns:
            int: the current index of where the interpreter is at.
        """
        return self._index
    
    @index.setter
    def index(self, value: int):
        self._index = value
    
    def get_stack_top(self) -> int:
        """ Gets the element at the top of the stack

        Returns:
            int: the element currently at the top of the stack
        """
        return self.stack[len(self.stack) - 1] 
    
    def is_stack_empty(self) -> bool:
        """ Determines whether the stack is empty or not.

        Returns:
            bool: true if the stack is empty, false otherwise
        """
        return len(self.stack) == 0
        
    def interpret(self) -> bool:
        """ Responsible for interpreting the goofy file
        lang that was provided when the interpreter object
        was created. 

        Returns:
            bool: whether the interpreter was successful at parsing the tokens or not
        """
        tokens = self.tokenizer.tokenize()
        
        interpreting_success = True
        
        # We should never hit this case since this is handled when the file is read, but just in case something weird happens I've left it here.
        if len(tokens) == 0: 
            LOGGER.error("The token count is 0, which means the file provided was empty. Try another file")
            
            return not interpreting_success
        
        while self.index < len(tokens):
           token = tokens[self.index]
          
           if token.type == TokenType.OPCODE:
               if not SupportedOpcodes.__contains__(token.value):
                   LOGGER.error("Token %d:%s contains an unsupported opcode", self.index + 1, token.value)
                   
                   return not interpreting_success
               
               match token.value:
                   case SupportedOpcodes.SHOVE.value:
                       interpreting_success = self.interpret_shove(tokens)
                       
                   case SupportedOpcodes.YELL.value:
                       interpreting_success = self.interpret_yell(tokens)
                       
                   case SupportedOpcodes.SNOOP.value:
                        interpreting_success = self.interpret_snoop(tokens)
                        
                   case SupportedOpcodes.YEET.value:
                        interpreting_success = self.interpret_yeet(tokens)
                        
                   case SupportedOpcodes.GLUE.value:
                        interpreting_success = self.interpret_glue(tokens)
                        
                   case SupportedOpcodes.MOOSH.value:
                        interpreting_success = self.interpret_moosh(tokens)
                        
                   case SupportedOpcodes.SNIP.value:
                        interpreting_success = self.interpret_snip(tokens)
                        
                   case SupportedOpcodes.BOUNCE.value:
                        interpreting_success = self.interpret_bounce(tokens)
                        
                   case SupportedOpcodes.FREEZE.value:
                        return self.interpret_freeze()
                    
                   case _:
                        interpreting_success = False

               if not interpreting_success:
                    return False
                        
           elif token.type == TokenType.UNKNOWN:
               LOGGER.error("Token %d:%s is an unknown token type. Please review the provided source", self.index + 1, token.value)
               
               return not interpreting_success
           
           self.index += 1
               
        return interpreting_success    
      
    def interpret_shove(self, tokens: Token) -> bool:
        """ Responsible for interpreting the SHOVE opcode.
        This pushes an integer value onto the stack. 

        Args:
            tokens (Token): the current list of tokens to parse.

        Returns:
            bool: whether interpreting was successful or not. A SHOVE operation is unsuccessful if the next token is missing or
                  not an integer.
        """
        success = True
        
        if len(tokens) > self.index + 1:
            next_token = tokens[self.index + 1]
                        
            if not next_token.type == TokenType.INT_LITERAL:
               LOGGER.error("Token %d:%s is not an integer. SHOVE must be supplied an integer. Ex: SHOVE 3", self.index + 1, next_token.value)
                            
               return not success
                 
            self.stack.append(int(next_token.value))  
                          
        else:
         LOGGER.error("There was no token to the right of SHOVE. Please make sure you remember to add a number")
                            
         return not success
            
        return success
    
    def interpret_yell(self, tokens: Token) -> bool:
        """ Responsible for interpreting the YELL opcode.
        This prints a the value to stdout. 

        Args:
            tokens (Token): the current list of tokens to parse.

        Returns:
            bool: whether interpreting was successful or not. A YELL operation is unsuccessful if the next token is missing or
                  not an integer.
        """
        success = True
        
        if len(tokens) > self.index + 1:
            next_token = tokens[self.index + 1]
                           
            print(next_token.value.strip("\""))
                    
        else:
            LOGGER.error("There was no token to the right of YELL. Please make sure you remember to add a value")
                           
            return not success
        
        return success
    
    def interpret_snoop(self, tokens: Token) -> bool:
        """ Responsible for interpreting the SNOOP opcode.
        This reads an integer value from stdin and pushes it
        onto the stack.

        Args:
            tokens (Token): the current list of tokens to parse.

        Returns:
            bool: whether interpreting was successful or not. A SNOOP operation is unsuccessful if the user input is 
                  not an integer.
        """
        success = True
        
        user_input = input()
                       
        if not str.isnumeric(user_input.strip("-")):
            LOGGER.error("The input entered was not a number, please supply a number")
                           
            return not success
                       
        self.stack.append(int(user_input))
        
        return success
    
    def interpret_yeet(self, tokens: Token):
        """ Responsible for interpreting the YEET opcode.
        This pops two values off the stack, subtracts them and
        then pushes the result onto the stack. Alternatively,
        an integer can be supplied after the command to subtract
        that value from the stack. Ex: YEET 1

        Args:
            tokens (Token): the current list of tokens to parse.

        Returns:
            bool: whether interpreting was successful or not. A YEET operation is unsuccessful if the stack does
                  not contain at least two items.
        """
        success = True
        
        if len(tokens) > self.index + 1:
            next_token = tokens[self.index + 1]
            
            if next_token.type == TokenType.INT_LITERAL:
                first = self.stack.pop()
                
                second = int(next_token.value)
                
                result = first - second
                
                self.stack.append(result)
                
                return success

        if len(self.stack) < 2:
            LOGGER.error("The stack does not contain at least two values to YEET. Ex: SHOVE 3 SHOVE 4 YEET")
                                
            return not success
                            
        first = self.stack.pop()
                            
        second = self.stack.pop()
                            
        result = first - second
                            
        self.stack.append(result)
        
        return success
    
    def interpret_glue(self, tokens: Token):
        """ Responsible for interpreting the GLUE opcode.
        This pops two values off the stack, adds them and
        then pushes the result onto the stack. Alternatively,
        an integer can be supplied after the command to subtract
        that value from the stack. Ex: GLUE 1

        Args:
            tokens (Token): the current list of tokens to parse.

        Returns:
            bool: whether interpreting was successful or not. A GLUE operation is unsuccessful if the stack does
                  not contain at least two items.
        """
        success = True
        
        if len(tokens) > self.index + 1:
            next_token = tokens[self.index + 1]
            
            if next_token.type == TokenType.INT_LITERAL:
                first = self.stack.pop()
                
                second = int(next_token.value)
                
                result = first + second
                
                self.stack.append(result)
                
                return success

        if len(self.stack) < 2:
            LOGGER.error("The stack does not contain at least two values to GLUE. Ex: SHOVE 3 SHOVE 4 GLUE")
                            
            return not success
                        
        first = self.stack.pop()
                        
        second = self.stack.pop()
                        
        result = first + second
        
        self.stack.append(result)
        
        return success
    
    def interpret_moosh(self, tokens: Token):
        """ Responsible for interpreting the MOOSH opcode.
        This pops two values off the stack, multiplies them and
        then pushes the result onto the stack. Alternatively,
        an integer can be supplied after the command to subtract
        that value from the stack. Ex: MOOSH 2

        Args:
            tokens (Token): the current list of tokens to parse.

        Returns:
            bool: whether interpreting was successful or not. A MOOSH operation is unsuccessful if the stack does
                  not contain at least two items.
        """
        success = True
        
        if len(tokens) > self.index + 1:
            next_token = tokens[self.index + 1]
            
            if next_token.type == TokenType.INT_LITERAL:
                first = self.stack.pop()
                
                second = int(next_token.value)
                
                result = first * second
                
                self.stack.append(result)
                
                return success

        if len(self.stack) < 2:
            LOGGER.error("The stack does not contain at least two values to MOOSH. Ex: SHOVE 3 SHOVE 4 MOOSH")
                            
            return not success
                        
        first = self.stack.pop()
                        
        second = self.stack.pop()
                        
        result = first * second
                        
        self.stack.append(result)
        
        return success
    
    def interpret_snip(self, tokens: Token):
        """ Responsible for interpreting the SNIP opcode.
        This pops two values off the stack, multiplies them and
        then pushes the result onto the stack. Alternatively,
        an integer can be supplied after the command to subtract
        that value from the stack. Ex: SNIP 10

        Args:
            tokens (Token): the current list of tokens to parse.

        Returns:
            bool: whether interpreting was successful or not. A SNIP operation is unsuccessful if the stack does
                  not contain at least two items or there is an attempt to divide by zero.
        """
        success = True
        
        if len(tokens) > self.index + 1:
            next_token = tokens[self.index + 1]
            
            if next_token.type == TokenType.INT_LITERAL:
                first = self.stack.pop()
                
                second = int(next_token.value)
                
                if second == 0:
                 LOGGER.error("Attempt to divide by zero, please review your program flow.")
                            
                 return not success
                
                result = first / second
                
                self.stack.append(result)
                
                return success

        if len(self.stack) < 2:
            LOGGER.error("The stack does not contain at least two values to SNIP. Ex: SHOVE 3 SHOVE 4 SNIP")
                            
            return not success
                        
        first = self.stack.pop()
                        
        second = self.stack.pop()
                        
        if second == 0:
           LOGGER.error("Attempt to divide by zero, please review your program flow.")
                            
           return not success
                        
        result = int(first / second)
                        
        self.stack.append(result)
        
        return success
        
    def interpret_bounce(self, tokens: Token) -> bool:
        """ Responsible for interpreting the BOUNCE opcode.
        This is responsible for jumping to another location
        based on if a condition is met. Ex: BOUNCE > 0 #LOOP

        Args:
            tokens (Token): the current list of tokens to parse.

        Returns:
            bool: whether interpreting was successful or not. A BOUNCE operation is unsuccessful if any of the
                  required tokens after BOUNCE are missing or if the stack is empty.
        """
        success = True
        
        if len(tokens) > self.index + 3:
          conditional_token = tokens[self.index + 1]
          
          comparison_token = tokens[self.index + 2]
          
          label_definition_token = tokens[self.index + 3]
          
          if not conditional_token.type == TokenType.CONDITIONAL:
             LOGGER.error("There as no conditional token provided to the right of BOUNCE. Ex: BOUNCE > 0 #L1")
             
             return not success

          if not comparison_token.type == TokenType.INT_LITERAL:
             LOGGER.error("The comparison token provided for BOUNCE was not an integer. Ex: BOUNCE > 0 #L1")
             
             return not success

          if not label_definition_token.type == TokenType.LABEL_DEFINITION:
             LOGGER.error("The label definition token provided for BOUNCE was not correct. Must contain a '#' before label name. Ex: BOUNCE > 0 #L1")
             
             return not success

          if self.is_stack_empty():
             LOGGER.error("There is no value on the stack for bounce to compare to. Make sure you add a value to the stack. Ex: SHOVE 10 | SNOOP")
             
             return not success
      
          top = self.get_stack_top()
        
          expression_result = eval(f"{top} {conditional_token.value} {comparison_token.value}")

          if not expression_result:
             # Skip the bounce statement if it's false
             self.index += 3
             
             return success

          label_start_tokens = self.tokenizer.get_tokens_by_type(TokenType.LABEL_START)
        
          found_label_start = False
        
          for label_start_token in label_start_tokens:
             if label_definition_token.value.strip("#") == label_start_token.value.strip(":"):
                self.index = tokens.index(label_start_token)
                
                found_label_start = True
                
                break
              
          if found_label_start:
             return success
          else:
             LOGGER.error("There was no label start found for label definition token: %s. Did you forget it?", label_definition_token.value)
             
             return not success     
        else: 
           LOGGER.error("There was a missing token to the right of BOUNCE. Please review your code")
           
           return not success
       
    def interpret_freeze(self) -> bool:
        """ Responsible for interpreting the FREEZE opcode.
        This halts execution at the point it is called. 

        Returns:
            bool: returns true to indicate that the program should halt 
        """
        return True                                       