import Lexer

class Node:
    def __init__(self, type) -> None:
        self.type = type

    def __str__(self) -> str:
        return f'{self.type}'
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Node):
            return self.type == other.type
        return False


class DoubleEndedNode(Node):
    def __init__(self, type, left_child, right_child) -> None:
        super().__init__(type)
        self.left_child = left_child
        self.right_child = right_child
    
    def __str__(self) -> str:
        return f'({self.left_child} {self.type} {self.right_child})'
    
    def __eq__(self, other) -> bool:
        if type(other) == DoubleEndedNode:
            return self.left_child == other.left_child and self.right_child == other.right_child
        return False


class NegativeNode(Node):
    def __init__(self, type, child) -> None:
        super().__init__(type)
        self.child = child
    
    def __str__(self) -> str:
        return f'{self.type}{self.child}'
    
    def __eq__(self, other) -> bool:
        if type(other) == NegativeNode:
            return self.child == other.child
        return False


class TokenList:
    def __init__(self, token_list: list) -> None:
        self.token_list = token_list
        self.parse_tree = self.parse_proposition()
     
    # Returns first "smalllest" proposition with logical connectives inside proposition
    # and replaces it with temp. Also returns index of temp
    # (a => (b => c & d)) => (e => f) returns b => c & d and 3
    def find_scope(self) -> tuple:
        # check for parentheses
        for index, token in enumerate(self.token_list):
            if token.type == Lexer.TokenType.OPENP:
                last_openp = index
            elif token.type == Lexer.TokenType.CLOSEP:
                smallest_prop = self.token_list[last_openp + 1:index]
                # replace and save location of smallest proposition
                self.token_list[last_openp:index + 1] = [Lexer.Token('temp', Lexer.TokenType.TEMP)]
                return smallest_prop, last_openp
        else: # smallest proposition is entire token list
            smallest_prop = self.token_list.copy()
            self.token_list[0:] = [Lexer.Token('temp', Lexer.TokenType.TEMP)]
            return smallest_prop, 0

    def parse_proposition(self):
        # parse until proposition is one object
        while(len(self.token_list) > 1):
            self.parse()
        return self.token_list[0]

    def parse(self):
        # check if list already parsed
        if isinstance(self.token_list[0], Node) and len(self.token_list) == 1:
            return self.token_list[0]
        
        # find smallest proposition
        proposition, prop_index = self.find_scope()

        # for i in proposition:
        #     print(i, end=' ')
        # print()

        # recursively parse left and right side of smallest proposition
        for index, symbol in reversed(list(enumerate(proposition))):
            if symbol.type == Lexer.TokenType.IMP or symbol.type == Lexer.TokenType.BIMP:
                parsed_object = DoubleEndedNode(symbol,
                                                TokenList(proposition[:index]).parse(),
                                                TokenList(proposition[index + 1:]).parse())
                self.token_list[prop_index] = parsed_object
                return parsed_object
        
        for index, symbol in reversed(list(enumerate(proposition))):
            if symbol.type == Lexer.TokenType.CON or symbol.type == Lexer.TokenType.DIS:
                parsed_object = DoubleEndedNode(symbol, 
                                                TokenList(proposition[:index]).parse(), 
                                                TokenList(proposition[index + 1:]).parse())
                self.token_list[prop_index] = parsed_object
                return parsed_object
        
        for index, symbol in enumerate(proposition):
            if symbol.type == Lexer.TokenType.NEG:
                parsed_object = NegativeNode(symbol, TokenList(proposition[index + 1:]).parse())
                self.token_list[prop_index] = parsed_object
                return parsed_object
            
        for index, symbol in enumerate(proposition):
            if symbol.type == Lexer.TokenType.VAR:
                parsed_object = Node(symbol)
                self.token_list[prop_index] = parsed_object
                return parsed_object
        else:
            return proposition

# Will eventually be able to print the parse tree in a fancy way
class TreePrinter:
    def __init__(self, parse_tree: Node | DoubleEndedNode | NegativeNode) -> None:
        self.parse_tree = parse_tree
        self.tree = []
        self.listify()
    
    # turn node object into array (list) representation
    def listify(self):
        self.queue = []
        self.queue.append(self.parse_tree)
        while len(self.queue) > 0:
            if isinstance(self.queue[0], Node):
                self.tree.append(self.queue[0].type)
            else: # then the first element in the queue is None
                self.tree.append(None)

            if type(self.queue[0]) == DoubleEndedNode:
                self.queue.append(self.queue[0].left_child)
                self.queue.append(self.queue[0].right_child)
            elif type(self.queue[0]) == NegativeNode:
                self.queue.append(self.queue[0].child)
                self.queue.append(None)
            else:
                # Only add to queue if there are elements in the queue which are not None
                for node in self.queue:
                    if node != None:
                        self.queue.append(None)
                        self.queue.append(None)
                        break
            self.queue.pop(0)

    # This method is a work in progress. It should eventually print the parse tree like this:
    #           =>
    #     =>          b
    #  a     &
    #      a   b
    def print_tree(self):
        for index, node in enumerate(self.tree):
            if index == 0 or bin(index + 2)[2:].count('1') == 1: # if power of 2
                print(node)
            else:
                print(node, end=' ')

# Example inputs:
# 'a => a & b => b'
# ~anthony <=> a | anthony
# ~a & (b => c) | d
proposition = input('Enter logical proposition: ')
tokenized_proposition = Lexer.tokenize(proposition)
parsed_proposition = TokenList(tokenized_proposition)

print(parsed_proposition.parse_tree)