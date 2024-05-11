import Lexer

class TautologyDetector():
    def __init__(self, prop) -> None:
        self.prop = Lexer.tokenize(prop)

    def negation(self, p) -> bool:
        return not p

    def conjunction(self, p, q) -> bool:
        return p and q

    def disjunction(self, p, q) -> bool:
        return p or q

    def implication(self, p, q) -> bool:
        return not p or q

    def biimplication(self, p, q) -> bool: 
        return p == q

    # check if character is in proposition
    def check_char(self, prop, char):
        return Lexer.Token(char, Lexer.token_type[char]) in prop
    
    # solves proposition by repeatedly solving subproposition with one logical connective
    def solve_proposition(self, prop: list[Lexer.Token]) -> bool | None | str:
        for i in prop:
            print(i.value, '', end='')
        print()

        if len(prop) == 1:
            return prop[0].value
        
        for i, char in enumerate(prop):

            if char.type == Lexer.TokenType.BOOL:
                continue
            
            prop_change = False 
            prev_char = prop[i-1].value
            next_char = prop[i+1].value if i < len(prop) - 1 else True

            # check and handle parentheses
            if self.check_char(prop, ')'):
                if char.type == Lexer.TokenType.OPENP:
                    last_open_index = i
                elif char.type == Lexer.TokenType.CLOSEP:
                    closed_index = i
                    result = self.solve_proposition(prop[last_open_index + 1:closed_index])
                    prop[last_open_index:closed_index + 1] = [Lexer.Token(result, Lexer.TokenType.BOOL)]
                    prop_change = True

            # check if certain logical connective in proposition
            # if so, check if character
            elif self.check_char(prop, '~'):
                if char.type == Lexer.TokenType.NEG:
                    prop[i:i+2] = [Lexer.Token(self.negation(next_char), Lexer.TokenType.BOOL)]
                    prop_change = True
            elif self.check_char(prop, '&'):
                if char.type == Lexer.TokenType.CON:
                    prop[i-1:i+2] = [Lexer.Token(self.conjunction(prev_char, next_char), Lexer.TokenType.BOOL)]
                    prop_change = True
            elif self.check_char(prop, '|'):
                if char.type == Lexer.TokenType.DIS:
                    prop[i-1:i+2] = [Lexer.Token(self.disjunction(prev_char, next_char), Lexer.TokenType.BOOL)]
                    prop_change = True
            elif self.check_char(prop, '=>'):
                if char.type == Lexer.TokenType.IMP:
                    prop[i-1:i+2] = [Lexer.Token(self.implication(prev_char, next_char), Lexer.TokenType.BOOL)]
                    prop_change = True
            elif self.check_char(prop, '<=>'):
                if char.type == Lexer.TokenType.BIMP:
                    prop[i-1:i+2] = [Lexer.Token(self.biimplication(prev_char, next_char), Lexer.TokenType.BOOL)]
                    prop_change = True
            
            if prop_change:
                return self.solve_proposition(prop)
            else:
                continue

    def find_distinct_variables(self, prop):
        distinct_variables = []
        for i in prop:
            if i.type == Lexer.TokenType.VAR and i.value not in distinct_variables:
                distinct_variables.append(i.value)
        return distinct_variables

    def is_tautology(self):
        distinct_variables = self.find_distinct_variables(self.prop)

        # check all possible combinations of variable values
        for i in range(2**len(distinct_variables)):
            bin_rep = bin(i)[2:]
            zero_filler = '0' * (len(distinct_variables) - len(bin_rep))
            bin_num = zero_filler + bin_rep

            # proposition with variables turned into truth values
            new_prop = []

            truth_table = {}

            for j in self.prop:
                if j.value in distinct_variables:
                    var_value = bool(int(bin_num[distinct_variables.index(j.value)]))
                    new_prop.append(Lexer.Token(var_value, Lexer.TokenType.BOOL))
                    truth_table[j.value] = var_value
                else:
                    new_prop.append(Lexer.Token(j.value, j.type))
            
            # print proposition number
            print(f'{i+1}/{2**len(distinct_variables)}')
            
            for var in truth_table:
                print(f'{var} = {truth_table[var]}')
            print()
            if not self.solve_proposition(new_prop):
                print('It is not a tautology')
                return False
                
            print()

            if i == range(2**len(distinct_variables))[-1]:
                print('It is a tautology')
                return True


# Example inputs:
# tautologies
# p => p
# (p | (q | r)) <=> ((p | q) | r)
# (p | q | r) & (p | q | ~r) & (p | ~q | r) & (~p | q | r) & (~p | ~q | ~r) <=> (p | q) & (r | p & q) & (~p | ~q | ~r)
# (p => q) | (q => p)
# to_be | ~to_be
# non-tautologies
# p => q
# p & (p <=> q)
# p => p => p
# anthony <=> ~cool
proposition = input('Enter proposition: ')

a = TautologyDetector(proposition)

a.is_tautology()