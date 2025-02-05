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
        elif str.isnumeric(statement.lstrip('-')):
            type = TokenType.INT_LITERAL
        elif str.__contains__(statement, "\""):
            type = TokenType.STRING_LITERAL
        elif statement in CONDITIONALS:
            type = TokenType.CONDITIONAL
        
        return type
    
    def parse_statement_with_quotes(self, statement: str) -> list[str]:
        """ For parsing a statement which contains quotes
        to account for spaces.

        Args:
            statement (str): the statement to parse

        Returns:
            list[str]: the list of statement parts that have been parsed accounting for quotes
        """
        parts = []
        
        quote = False
    
        current_part = ""
        
        for character in statement:
            if character == "\"":
                quote = not quote
            
            if not quote:
                if str.isspace(character):
                    parts.append(current_part)
                    
                    current_part = ""
                    
                    continue
            
            current_part += character
            
        parts.append(current_part)  
        
        return parts
            
    def tokenize(self) -> list[Token]:
        """ Derives a list of tokens from the goofy lang file
        and returns a list of those tokens.

        Returns:
            list[Token]: the list of derived tokens from the goofy lang file.
        """
        parsed_statements = []
        
        for line in self.file_lines:
            # NOTE: If more tokens require this kind of granular parsing, should switch the entire tokenizer to looking at characters.
            if line.__contains__("\""):
                statement_parts = self.parse_statement_with_quotes(line)
            else:
                statement_parts = line.split() 
            
            parsed_statements.extend(statement_parts)
        
        for statement in parsed_statements:
            token_value = statement
            
            token_type = self.get_token_type(statement)
           
            current_token = self.Token(token_value, token_type)
            
            self.tokens.append(current_token)
            
        return self.tokens       