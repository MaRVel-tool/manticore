
# parser_LtlParser_parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND EXIST FALSE FORALL LPAREN NEGATION NEXT OR PROPOSTITION RPAREN TRUE UNTILexpression : expression UNTIL expression\n                      | NEXT expression\n                      | expression OR expression\n                      | expression AND expression\n                      | NEGATION expression\n                      | EXIST expression\n                      | FORALL expression\n                      | LPAREN expression RPAREN\n                      | PROPOSTITION\n                      | FALSE\n                      | TRUE'
    
_lr_action_items = {'NEXT':([0,2,3,4,5,6,10,11,12,],[2,2,2,2,2,2,2,2,2,]),'NEGATION':([0,2,3,4,5,6,10,11,12,],[3,3,3,3,3,3,3,3,3,]),'EXIST':([0,2,3,4,5,6,10,11,12,],[4,4,4,4,4,4,4,4,4,]),'FORALL':([0,2,3,4,5,6,10,11,12,],[5,5,5,5,5,5,5,5,5,]),'LPAREN':([0,2,3,4,5,6,10,11,12,],[6,6,6,6,6,6,6,6,6,]),'PROPOSTITION':([0,2,3,4,5,6,10,11,12,],[7,7,7,7,7,7,7,7,7,]),'FALSE':([0,2,3,4,5,6,10,11,12,],[8,8,8,8,8,8,8,8,8,]),'TRUE':([0,2,3,4,5,6,10,11,12,],[9,9,9,9,9,9,9,9,9,]),'$end':([1,7,8,9,13,14,15,16,18,19,20,21,],[0,-9,-10,-11,-2,-5,-6,-7,-1,-3,-4,-8,]),'UNTIL':([1,7,8,9,13,14,15,16,17,18,19,20,21,],[10,-9,-10,-11,10,10,10,10,10,10,10,10,-8,]),'OR':([1,7,8,9,13,14,15,16,17,18,19,20,21,],[11,-9,-10,-11,11,11,11,11,11,11,11,11,-8,]),'AND':([1,7,8,9,13,14,15,16,17,18,19,20,21,],[12,-9,-10,-11,12,12,12,12,12,12,12,12,-8,]),'RPAREN':([7,8,9,13,14,15,16,17,18,19,20,21,],[-9,-10,-11,-2,-5,-6,-7,21,-1,-3,-4,-8,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,2,3,4,5,6,10,11,12,],[1,13,14,15,16,17,18,19,20,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> expression UNTIL expression','expression',3,'p_expression','LtlParser.py',71),
  ('expression -> NEXT expression','expression',2,'p_expression','LtlParser.py',72),
  ('expression -> expression OR expression','expression',3,'p_expression','LtlParser.py',73),
  ('expression -> expression AND expression','expression',3,'p_expression','LtlParser.py',74),
  ('expression -> NEGATION expression','expression',2,'p_expression','LtlParser.py',75),
  ('expression -> EXIST expression','expression',2,'p_expression','LtlParser.py',76),
  ('expression -> FORALL expression','expression',2,'p_expression','LtlParser.py',77),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression','LtlParser.py',78),
  ('expression -> PROPOSTITION','expression',1,'p_expression','LtlParser.py',79),
  ('expression -> FALSE','expression',1,'p_expression','LtlParser.py',80),
  ('expression -> TRUE','expression',1,'p_expression','LtlParser.py',81),
]
