import sys
from types import GeneratorType
import pprint
import json

"""
This is a generic parse tree generator that uses a mix of iterative and recursive decent. The program has a predefined
grammar(based on the quirk language) but that can modified depending on the language. Each key in the grammar object
corresponds to a rule(array) of the quirk grammar. Each index of the rule array is a possible replacement for that node
. A replacement rule greater with more than one entry is broken into tuples so the parser can parse 'subtrees', which I
believe negates left recursion.
Will raise an error if there is a problem with the syntax. I tried capture the point where syntax fails but it doesnt
seem to work.
"""


""" the grammar rules for the quirk language"""
grammar = {
    'Program': [('Statement', 'Program'), 'Statement'],
    'Statement': ['FunctionDeclaration', 'Assignment', 'Print'],
    'FunctionDeclaration': [
        (('FUNCTION', ('Name', 'LPAREN')), (('FunctionParams', 'LBRACE'), ('FunctionBody', 'RBRACE')))],
    'FunctionParams': [('NameList', 'RPAREN'), 'RPAREN'],
    'FunctionBody': [('Program', 'Return'), 'Return'],
    'Return': [('RETURN', 'ParameterList')],
    'Assignment': ['SingleAssignment', 'MultipleAssignment', ],
    'SingleAssignment': [(('VAR', 'Name'), ('ASSIGN', 'Expression'))],
    'MultipleAssignment': [(('VAR', 'NameList'), ('ASSIGN', 'FunctionCall'))],
    'Print': [('PRINT', 'Expression')],
    'NameList': [(('Name', 'COMMA'), 'NameList'), 'Name'],
    'ParameterList': [(('Parameter', 'COMMA'), 'ParameterList'), 'Parameter'],
    'Parameter': ['Expression', 'Name'],
    'Expression': [(('Term', 'ADD'), 'Expression'), (('Term', 'SUB'), 'Expression'), 'Term'],
    'Term': [(('Factor', 'MULT'), 'Term'), (('Factor', 'DIV'), 'Term'), 'Factor'],
    'Factor': [(('SubExpression', 'EXP'), 'Factor'), 'SubExpression', 'FunctionCall', (('Value', 'EXP'), 'Factor'),
               'Value'],
    'FunctionCall': [(('Name', 'LPAREN'), ('FunctionCallParams', ('COLON', 'Number'))),
                     ('Name', ('LPAREN', 'FunctionCallParams'))],
    'FunctionCallParams': [('ParameterList', 'RPAREN'), 'RPAREN'],
    'SubExpression': [('LPAREN', ('Expression', 'RPAREN'))],
    'Value': ['Name', 'Number'],
    'Name': ['IDENT', ('SUB', 'IDENT'), ('ADD', 'IDENT')],
    'Number': ['NUMBER', ('SUB', 'NUMBER'), ('ADD', 'NUMBER')]
}


# start utilities
def get_type(args, index):
    """
    Gets the type of the input, and index for the global token
    :param args: is a terminal token or key(rule) of grammar.
    :param index: index of the current token of the caller
    :return: a generator of the AST for the node, or a tuple of a token
    """
    if args in grammar:
        return parse_generator(args, index)
    else:
        return (get_token(args, index))


def get_token(var, index):
    """
    compares the given token with the global token at the given index
    :param var: token from a syntanx sequence
    :param index: of the global tokens
    :return: will return false if given token and global token are different,
            will return the token and new index if they are the same and
            will extract Ident or number if needed.
    """
    global token
    try:
        toke = token[index]
    except IndexError:
        return False, False
    sp = toke.split(':')
    if sp[0] == var:
        index += 1
        return toke, index
    else:
        return False, index


def get_tree(gen):
    """
    :param gen: an AST generator
    :return: returns a valid AST(as nested arrays) or false if there is none.
    """
    for tree, index in gen:
        if tree:
            return (tree, index), gen
    else:
        return (False, index), gen
# end utilities


def get_sub_node(var, index):
    """
    returns a node of a subtree(tuple pair in the grammar)
    :param var: is a syntax pair, AST generator, or terminal token
    :param index: of global tokens
    :return: a node of the a subtree, can be terminal or another tree, or false
    """
    if type(var) is tuple:
        child, index = get_sub_tree(var, index)
        return child, index, 0
    else:
        child = get_type(var, index)
        if type(child) is GeneratorType:
            child, index = get_tree(child)[0]
            return child, index, 1
        else:
            return child[0], child[1], 1


def get_sub_tree(pair, index):
    """
     returns a valid subtree(tuple pair in the grammar) or false
    :param pair: syntax pair from the grammar
    :param index: of global tokens
    :return:returns a subtree and new index, or false
    """
    node = []
    left, right = pair
    l_tree = get_sub_node(left, index)
    if l_tree[0]:
        r_tree = get_sub_node(right, l_tree[1])
        if r_tree[0]:
            if l_tree[2] == 0:
                node.extend(l_tree[0])
            else:
                node.append(l_tree[0])
            if r_tree[2] == 0:
                node.extend(r_tree[0])
            else:
                node.append(r_tree[0])
            return (node, r_tree[1])
        else:
            return (False, r_tree[1])
    else:
        return (False, l_tree[1])


def parse_generator(gram, index):
    """
    Generates a valid parse tree(possibly multiple) or false if there is none. Generators are 'lazy' and do not
    execute when call but return a generator object that can executed(iterated) later. This was done to more easily
    determin between subtrees(tuples), nodes, and terminals and because there could be multiple valid syntax paths (and
    because it was cool to learn). So it can probably be implemented as a standard function.
    :param gram: key to the entry in grammar
    :param index: of global tokens
    :return: a generator that yields a valid parse tree and new index of the given syntax, or false if there is none.
    """
    syntaxes = grammar.get(gram)
    my_index = index
    i = 0
    for path in syntaxes:
        index = my_index
        node = [gram + str(i)]
        if type(path) is tuple:
            child, index = get_sub_tree(path, index)
            if child:
                node.extend(child)
                yield (node, index)
            else:
                yield (False, index)
        else:
            child = get_type(path, index)
            if type(child) is GeneratorType:
                child, gen = get_tree(child)
            if child[0]:
                node.append(child[0])
                yield (node, child[1])
            else:
                yield (False, child[1])
        i += 1
    else:
        yield (False, index)


def parse():
    """
    The main method that reads the input tokens and outputs the parse tree if it is a valid program.
    """
    global token
    token = sys.stdin.read().split('\n')
    del token[-1]
    length = len(token) - 1
    (tree, index), gen = get_tree(parse_generator('Program', 0))
    if index != length:
        raise SyntaxError("ERROR at index: ", index, " and token:", token[index])
    else:
        sys.stdout.write(json.dumps(tree))

if __name__ == "__main__":
    parse()