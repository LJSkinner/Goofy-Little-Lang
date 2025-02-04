from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
    """ Enum that represents the different
    types of tokens that can exist in goofy lang.
    """
    OPCODE = 1
    STRING_LITERAL = 2
    INT_LITERAL = 3
    CONDITIONAL = 4
    UNKNOWN = 5 

# Stores the types of conditional operators supported in goofy lang        
CONDITIONALS = ["=", ">", "<", ">=", "<=", "!="]
     
class GoofyTokenizer:
    """ Responsible for tokenizing
    a goofy lang file, determining the
    types and values associated with them.
    """

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
        
    def __str__(self):
        return "Tokens:\n" + "\n".join(f"{i + 1}: Value = {token.value} Type = {token.type.name}" for i, token in enumerate(self.tokens))
    
    def get_token_type(self, statement: str) -> TokenType:
        """ Derives a token type from the provided string literal
        statement.

        Args:
            statement (str): the statement to derive the token type from

        Returns:
            TokenType: the token type derived from the provided statement.
        """
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
        
    def tokenize(self) -> list[Token]:
        """ Derives a list of tokens from the goofy lang file
        and returns a list of those tokens.

        Returns:
            list[Token]: the list of derived tokens from the goofy lang file.
        """
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