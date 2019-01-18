import ply.lex as lex
import ply.yacc as yacc


# s = "((-('p71')) || (true U ('p96')))"
# s="('r' U ('p1' U X ('p2' U ('p3')))) && ((('p1' U (('p2' U 'p4') U ('q' && 'r')))) U 'r')"
# s="(-(true U -((-'p1') || (X (true U 'p2'))))) && (-(true U -((-'p2') || (X (true U 'p1')))))"

class Parser(object):
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = {}
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[
                1] + "_" + self.__class__.__name__
        except:
            modname = "parser" + "_" + self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        # print self.debugfile, self.tabmodule

        # Build the lexer and parser
        print("init LTL PARSER")
        self.lexer = lex.lex(module=self, debug=self.debug)
        self.parser = yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)


class LtlParser(Parser):
    class parse_node(object):
        pass
    def __init__(self):
        super(LtlParser, self ).__init__()

    tokens = (
        'UNTIL','NEGATION', 'AND', 'OR',
        'NEXT','EXIST','FORALL','PROPOSTITION', 'TRUE', 'FALSE',
        'LPAREN','RPAREN',
        )

    # Tokens
    t_UNTIL           = r'U|W'
    t_NEGATION        = r'-'
    t_NEXT            = r'X'
    t_EXIST           = r'E'
    t_FORALL          = r'A'
    t_AND             = r'&&'
    t_OR              = r'\|\|'
    t_LPAREN          = r'\('
    t_RPAREN          = r'\)'
    t_TRUE            = r'true'
    t_FALSE           = r'false'
    t_PROPOSTITION    = r'\'[a-zA-Z0-9\_\(\)\=\>\<]+\''

    # Ignored characters
    t_ignore = " \t"

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Parsing rules
    def p_expression(self, p):
        '''expression : expression UNTIL expression
                      | NEXT expression
                      | expression OR expression
                      | expression AND expression
                      | NEGATION expression
                      | EXIST expression
                      | FORALL expression
                      | LPAREN expression RPAREN
                      | PROPOSTITION
                      | FALSE
                      | TRUE'''
        p[0] = self.parse_node()
        if len(p) == 2:
            p[0].type = "LEAF"
            p[0].str = p[1]
        elif p[1] == "(":
            p[0] = p[2]
        elif p[1] == "A":
            # todo in CTL
            p[0].z3_str = p[2]
        elif p[1] == "E":
            # todo in CTL
            p[0].z3_str = p[2]
        elif p[1] == "-":
            p[0].type = "NOT"
            p[0].child = p[2]
        elif p[1] == "X":
            p[0].type = "NEXT"
            p[0].child = p[2]
        elif p[2] == "&&":
            p[0].type = "AND"
            p[0].left = p[1]
            p[0].right = p[3]
        elif p[2] == "||":
            p[0].type = "OR"
            p[0].left = p[1]
            p[0].right = p[3]
        else:
            p[0].type = "UNTIL"
            p[0].left = p[1]
            p[0].right =p[3]

    def p_error(self, p):
        print("Syntax error at '%s'" % p.value)


