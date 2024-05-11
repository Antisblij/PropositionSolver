from enum import Enum

# Symbols used
# ¬ = ~
# ∧ = &
# v = |
# → = =>
# ↔ = <=>

class TokenType(Enum):
    NEG = 1
    CON = 2
    DIS = 3
    IMP = 4
    BIMP = 5
    OPENP = 6
    CLOSEP = 7
    VAR = 8
    TEMP = 9


class Token:
    def __init__(self, value: str | bool | None, type: TokenType) -> None:
        self.value = value
        self.type = type

    def __str__(self) -> str:
        return f'{self.value}'
    
    def __eq__(self, other):
        return isinstance(other, Token) and self.value == other.value and self.type == other.type

token_type = {
    '~' : TokenType.NEG,
    '&' : TokenType.CON,
    '|' : TokenType.DIS,
    '=>' : TokenType.IMP,
    '<=>' : TokenType.BIMP,
    '(' : TokenType.OPENP,
    ')' : TokenType.CLOSEP,
    'aap' : TokenType.VAR, # propositional variables consist of letters (and underscores) and can be more than one character long
    'temp' : TokenType.TEMP, # used when parsing
}

sorted_symbols = sorted(token_type.keys(), key=len, reverse=True)

def tokenize(prop: str) -> list:
    tokens = []

    # Build each token
    while len(prop) > 0:
        for symbol in sorted_symbols:
            # remove whitespace
            if prop.startswith(' '):
                prop = prop[1:]
                break
            if prop.startswith(symbol):
                # remove characters from proposition
                prop = prop[len(symbol):]
                tokens.append(Token(
                    value=symbol,
                    type=token_type[symbol],
                ))
                break
        else:
            # build propositional variable
            count = 1
            for i in range(1, len(prop)):
                if prop[i].isalpha() or prop[i] == '_':
                    count += 1
                    continue
                break
            tokens.append(Token(
                value=prop[:count],
                type=TokenType.VAR,
            ))
            prop = prop[count:]
        
    return tokens