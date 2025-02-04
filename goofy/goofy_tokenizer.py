from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
     OPCODE = 1
     STRING_LITERAL = 2
     INT_LITERAL = 3
     CONDITIONAL = 4
     UNKNOWN = 5 
        
CONDITIONALS = ["=", ">", "<", ">=", "<=", "!="]
     
class Tokenizer:

    @dataclass
    class Token:
        """ Represents an individual token that has 
        been parsed by the tokenizer. 
        """
        value: str
        type: TokenType
      
        
    def __init__(self, file_lines: list[str]):
        self.file_lines: list[str] = file_lines
        
        self.tokens: list[self.Token] = []
    
    def get_token_type(self, statement: str) -> TokenType:
        type = TokenType.UNKNOWN
        
        if str.isupper(statement):
            type = TokenType.OPCODE
        elif str.isnumeric(statement):
            type = TokenType.INT_LITERAL
        elif str.__contains__(statement, "\""):
            type = TokenType.STRING_LITERAL
        elif statement in CONDITIONALS:
            type = TokenType.CONDITIONAL
        
        return type
        
    def tokenize(self):
        # For storing the non tokenized statements in the file
        parsed_statements = []
        
        for line in self.file_lines:
            statement_parts = line.split()
            
            parsed_statements.extend(statement_parts)
        
        for statement in parsed_statements:
            token_value = statement
            
            token_type = self.get_token_type(statement)
           
            current_token = self.Token(token_value, token_type)
            
            self.tokens.append(current_token)
            
        return self.tokens
        
            