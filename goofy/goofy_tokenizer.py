from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
     OPCODE = 1
     STRING_LITERAL = 2
     INT_LITERAL = 3
     CONDITIONAL = 4
     UNKNOWN = 5 

class Tokenizer:
    @dataclass
    class Token:
        """ Represents an individual token
        """
        value: str
        type: TokenType
        line_number: int
        line_column: int
        
    def __init__(self, file_lines: list[str]):
        self.file_lines = file_lines
        
        self.tokens: list[self.Token] = []
        
    def tokenize(self):
        for line in self.file_lines:
            token_value = line
            
            
            
            current_token = self.Token(token_value, TokenType.STRING_LITERAL, 0, 0)
            
            self.tokens.append(current_token)
            
        return self.tokens
        
            