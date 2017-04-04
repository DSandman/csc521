import sys
import pprint
import json

pp = pprint.PrettyPrinter(indent=1, depth=100)

"""
This program executes the quirk program of the given parse tree(that has been jsoned).
with the print will write to the quirk.out file.
"""


class RuntimeError(Exception):
    pass


# start utilities
def lookup_in_scope_stack(name, scope):
    """
    Returns values (including declared functions!) from the scope.
    name - A string value holding the name of a bound variable or function.
    scope - The scope that holds names to value binding for variables and
        functions.
    returns - the value associated with the name in scope.
    """
    if name in scope:
        return scope[name]
    else:
        if "__parent__" in scope:
            print("not found in scope. Looking at __parent__")
            return lookup_in_scope_stack(name, scope["__parent__"])
        else:
            print("ERROR: variable " + name + " was not found in scope stack!")


def get_name_from_ident(tok):
    """Returns the string lexeme associated with an IDENT token, tok.
    """
    print("get_name_from_ident() " + tok)
    colon_index = tok.find(":")
    return tok[colon_index + 1:]


def get_number_from_ident(tok):
    """Returns the float lexeme associated with an NUMBER token, tok.
    """
    print("get_number_from_ident()" + tok)
    colon_index = tok.find(":")
    return float(tok[colon_index + 1:])


def func_by_name(*args):
    """
    Calls a function whos name is given as a parameter. It requires the parse
        tree associated with that point in the grammar traversal and the current
        scope.
    :param args: is interpreted as
        name = args[0] -- the name of the function to call
        pt = args[1] -- the subtree of the parse tree associated with the name
        scope = args[2] -- the scope of the subtree should use
    :return: Pass through the return value of the called function.
    """
    name = args[0]
    pt = args[1]
    scope = args[2]
    return globals()[name](pt, scope)


# end utilities

# <Program> -> <Statement> <Program> | <Statement>
def Program0(pt, scope):
    """
    calls statement and program functions and passes scope and subtree
    :param pt: subtree
    :param scope: scope of the subtree
    :return: calls statement and program functions
    """
    func_by_name(pt[1][0], pt[1], scope)
    func_by_name(pt[2][0], pt[2], scope)


def Program1(pt, scope):
    """
    calls statement function and passes scope and subtree
    :param pt: subtree
    :param scope: scope of the subtree
    :return: calls statement function
    """
    func_by_name(pt[1][0], pt[1], scope)


# <Statement> -> <FunctionDeclaration> | <Assignment> | <Print>
def Statement0(pt, scope):
    """
   calls FunctionDeclaration and passes scope and subtree
   :param pt: subtree
   :param scope: scope of the subtree
   :return: FunctionDeclaration function
    """
    func_by_name(pt[1][0], pt[1], scope)


def Statement1(pt, scope):
    """
    calls Assignment and passes scope and subtree
    :param pt: subtree
    :param scope: scope of the subtree
    :return: Assignment function
    """
    func_by_name(pt[1][0], pt[1], scope)


def Statement2(pt, scope):
    """
     calls Print and passes scope and subtree
     :param pt: subtree
     :param scope: scope of the subtree
     :return: Print function
    """
    func_by_name(pt[1][0], pt[1], scope)


# <FunctionDeclaration> -> FUNCTION <Name> PAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
def FunctionDeclaration0(pt, scope):
    """
    1. Get function name.
    2. Get names of parameters.
    3. Get reference to function body subtree.
    4. In scope, bind the function's name to the following list:
        "foo": [['p1', 'p2', 'p3'], [FunctionBodySubtree]]
        where foo is the function names, p1, p2, p2 are the parameters and
        FunctionBodySubtree represents the partial parse tree that holds the
        FunctionBody0 expansion. This would correspond to the following code:
        function foo(p1, p2, p3) { [the function body] }

    #Bonus: check for return value length at declaration time
    """
    name = func_by_name(pt[2][0], pt[2], scope)[1]
    param = func_by_name(pt[4][0], pt[4], scope)
    body = func_by_name(pt[6][0], pt[6], scope)
    scope[name] = [param, body]


# <FunctionParams> -> <NameList> RPAREN | RPAREN
# should return a list of values
def FunctionParams0(pt, scope):
    """
        calls NameList and passes scope and subtree
      :param pt: subtree
      :param scope: scope of the subtree
      :return: NameList function
    """
    return func_by_name(pt[1][0], pt[1], scope)


def FunctionParams1(pt, scope):
    """
    returns empty array
        :param pt: subtree
        :param scope: scope of the subtree
        :return: empty array
    """
    return []


# <FunctionBody> -> <Program> <Return> | <Return>
def FunctionBody0(pt, scope):
    """
    returns subtrees of FunctionBody
    :param pt: subtree
    :param scope: scope of the subtree
    :return: subtrees of FunctionBody
    """
    print(pt[2])
    return [pt[1], pt[2]]


def FunctionBody1(pt, scope):
    """
    returns subtree of FunctionBody
    :param pt: subtree
    :param scope: scope of the subtree
    :return: subtree of FunctionBody
    """
    return pt[1]


# <Return> -> RETURN <ParameterList>
def Return0(pt, scope):
    """
    calls ParameterList
    :param pt: subtree
    :param scope: scope of the subtree
    :return: ParameterList function
    """
    return func_by_name(pt[2][0], pt[2], scope)


# <Assignment> -> <SingleAssignment> | <MultipleAssignment>
def Assignment0(pt, scope):
    """
    calls SingleAssignment
    :param pt: subtree
    :param scope: scope of the subtree
    :return: SingleAssignment function
    """
    return func_by_name(pt[1][0], pt[1], scope)


def Assignment1(pt, scope):
    """
    calls MultipleAssignment
    :param pt: subtree
    :param scope: scope of the subtree
    :return: MultipleAssignment function
    """
    return func_by_name(pt[1][0], pt[1], scope)


# <SingleAssignment> -> VAR <Name> ASSIGN <Expression>
def SingleAssignment0(pt, scope):
    # 1. Get name of the variable.
    # 2. Get value of <Expression>
    # 3. Bind name to value in scope.
    # Bonus: error if the name already exists in scope -- no rebinding
    name = func_by_name(pt[2][0], pt[2], scope)[1]
    value = func_by_name(pt[4][0], pt[4], scope)
    if isinstance(value, list):
        raise RuntimeError("ERROR assignment length doesnt match")
    else:
        if name in scope:
            raise RuntimeError("ERROR", name, "is already assigned")
        else:
            scope[name] = value


# <MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
def MultipleAssignment0(pt, scope):
    # 1. Get list of variable names
    # 2. Get the values returned from the fuction call
    # Bonus: error if any name already exists in scope -- no rebinding
    # Bonus: error if the number of variable names does not match the number of values
    names = func_by_name(pt[2][0], pt[2], scope)
    values = func_by_name(pt[4][0], pt[4], scope)
    if len(names) == len(values):
        for n, v in zip(names, values):
            if n in scope:
                raise RuntimeError("ERROR", n, "is already assigned")
            else:
                scope[n] = v
    else:
        raise RuntimeError("ERROR assignment length doesnt match")


# <Print> -> PRINT <Expression>
def Print0(pt, scope):
    """
    prints Expression value to output file
    :param pt: subtree
    :param scope: scope of the subtree
    """
    global output
    res = str(func_by_name(pt[2][0], pt[2], scope))
    if isinstance(res, list):
        res = res[0]
    output.write(res + '\n')


# <NameList> -> <Name> COMMA <NameList> | <Name>
def NameList0(pt, scope):
    """
    returns an array of names
    :param pt: subtree
    :param scope: scope of the subtree
    :return the list of names
    """
    param_name = func_by_name(pt[1][0], pt[1], scope)[1]
    return [param_name] + func_by_name(pt[3][0], pt[3], scope)


def NameList1(pt, scope):
    """
    returns a single names
    :param pt: subtree
    :param scope: scope of the subtree
    :return a name
    """
    # getting the [1] of the return value for name as it returns a [val, name]
    return [func_by_name(pt[1][0], pt[1], scope)[1]]


# <ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>
# should return a a list of values.
def ParameterList0(pt, scope):
    """
    returns an array of parameters
    :param pt: subtree
    :param scope: scope of the subtree
    :return array of parameters
    """
    param_name = func_by_name(pt[1][0], pt[1], scope)
    return [param_name] + func_by_name(pt[3][0], pt[3], scope)


def ParameterList1(pt, scope):
    """
   returns a single parameter
   :param pt: subtree
   :param scope: scope of the subtree
   :return a parameter
   """
    return [func_by_name(pt[1][0], pt[1], scope)]


# <Parameter> -> <Expression> | <Name>
def Parameter0(pt, scope):
    """
    :param pt:
    :param scope:
    :return:
    """
    return func_by_name(pt[1][0], pt[1], scope)


def Parameter1(pt, scope):
    # pull value out of [value,name]
    return func_by_name(pt[1][0], pt[1], scope)[0]


# <Expression> -> <Term> ADD <Expression> | <Term> SUB <Expression> | <Term>
def Expression0(pt, scope):
    # <Term> ADD <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value + right_value


def Expression1(pt, scope):
    # <Term> SUB <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value - right_value


def Expression2(pt, scope):
    # <Term>
    return func_by_name(pt[1][0], pt[1], scope)


# <Term> -> <Factor> MULT <Term> | <Factor> DIV <Term> | <Factor>
def Term0(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value * right_value


def Term1(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value / right_value


def Term2(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


# <Factor> -> <SubExpression> EXP <Factor> | <SubExpression> | <FunctionCall> | <Value> EXP <Factor> | <Value>
def Factor0(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value ** right_value


def Factor1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope, scope)


def Factor2(pt, scope):
    # returns multiple values -- use the first by default.
    return func_by_name(pt[1][0], pt[1], scope, scope)


def Factor3(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value ** right_value


def Factor4(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


# <FunctionCall> ->  <Name> LPAREN <FunctionCallParams> COLON <Number> | <Name> LPAREN <FunctionCallParams>
def FunctionCall0(pt, scope):
    """
    This is the most complex part of the interpreter as it involves executing a
    a partial parsetree that is not its direct child.

    1. Get the function name.
    2. Retrieve the stored function information from scope.
    3. Make a new scope with old scope as __parent__
    4. Get the list of parameter values.
    5. Bind parameter names to parameter values in the new function scope.
    6. Run the FunctionBody subtree that is part of the stored function information.
    7. Get the index return number.
    8. Return one value from the list of return values that corresponds to the index number.
    Bonus: Flag an error if the index value is greater than the number of values returned by the function body.
    """
    func, name = func_by_name(pt[1][0], pt[1], scope)
    nscope = {"__parent__": scope}
    pname = func[0]
    pvalue = func_by_name(pt[3][0], pt[3], scope)
    nscope.update(dict(zip(pname, pvalue)))
    body = func[1]
    if isinstance(body[0], str):
        results = func_by_name(body[0], body, nscope)
    else:
        func_by_name(body[0][0], body[0], nscope)
        results = func_by_name(body[1][0], body[1], nscope)
    index = func_by_name(pt[5][0], pt[5], nscope)
    print(int(index))
    # checks if index is a float
    if index == int(index):
        # checks if index is in return array
        if index < len(results) and index >= 0:
            return results[int(index)]
        else:
            raise RuntimeError("index out of bounds")


def FunctionCall1(pt, scope):
    """
    This is the most complex part of the interpreter as it involves executing a
    a partial parsetree that is not its direct child.

    1. Get the function name.
    2. Retrieve the stored function information from scope.
    3. Make a new scope with old scope as __parent__
    4. Get the list of parameter values.
    5. Bind parameter names to parameter values in the new function scope.
    6. Run the FunctionBody subtree that is part of the stored function information.
    7. Return the list of values generated by the <FunctionBody>
    """
    func, name = func_by_name(pt[1][0], pt[1], scope)
    nscope = {"__parent__": scope}
    pname = func[0]
    pvalue = func_by_name(pt[3][0], pt[3], scope)
    nscope.update(dict(zip(pname, pvalue)))
    body = func[1]
    if isinstance(body[0], str):
        results = func_by_name(body[0], body, nscope)
    else:
        func_by_name(body[0][0], body[0], nscope)
        results = func_by_name(body[1][0], body[1], nscope)
    return results


# <FunctionCallParams> ->  <ParameterList> RPAREN | RPAREN
def FunctionCallParams0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


def FunctionCallParams1(pt, scope):
    return []


# <SubExpression> -> LPAREN <Expression> RPAREN
def SubExpression0(pt, scope):
    return func_by_name(pt[2][0], pt[2], scope)


# <Value> -> <Name> | <Number>
def Value0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)[0]


def Value1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


# <Name> -> IDENT | SUB IDENT | ADD IDENT
def Name0(pt, scope):
    name = get_name_from_ident(pt[1])
    return [lookup_in_scope_stack(name, scope), name]


def Name1(pt, scope):
    name = get_name_from_ident(pt[2])
    return [lookup_in_scope_stack(name, scope) * -1, name]


def Name2(pt, scope):
    name = get_name_from_ident(pt[2])
    return [lookup_in_scope_stack(name, scope), name]


# <Number> -> NUMBER | SUB NUMBER | ADD NUMBER
def Number0(pt, scope):
    return get_number_from_ident(pt[1])


def Number1(pt, scope):
    return get_number_from_ident(pt[2]) * -1


def Number2(pt, scope):
    return get_number_from_ident(pt[2])


if __name__ == '__main__':
    # the output file
    global output
    output = open('quirk.out', 'w')
    tree = sys.stdin.read()
    tree1 = json.loads(tree)
    scope = {}
    func_by_name(tree1[0], tree1, scope)
