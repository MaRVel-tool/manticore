from manticore.ethereum import ManticoreEVM
from GameTree import GameTree
from manticore.exceptions import EthereumError
from manticore.ethereum.abi import ABI
from LtlParser import LtlParser
from manticore.GameTree import GameTree
from z3 import *

contract_src="""
pragma solidity ^0.5.0;
contract Bank {
    function withdraw(uint amount) public {
        if(amount < 20){
            msg.sender.call.value(amount)("");
        } else {
            revert();
        }
    }
    function withdraw2(uint amount, uint max) public {
        if(amount < max){
            msg.sender.call.value(amount)("");
        } else {
            revert();
        }
    }
}
"""

# object decides how to traverse the game tree
class BMC(object):
    def __init__(self):
        self.symbolic_vars = {}
        self.z3_var_counter = 0
        self.z3_func = {}
        self.lp = LtlParser()

    def init_manticore(self, manticore=None):
        # user_account = m.create_account(balance=1000)
        # user_sol_account = m.solidity_create_contract(contract_src, owner=user_account)
        self.m = manticore
        self.contract_account = self.m.create_account(balance=1000)
        self.malicious_account = self.m.create_account(balance=1000)
        self.contract = self.m.solidity_create_contract(contract_src, owner=self.contract_account)
        self.m.world.set_balance(self.contract, 1000000000000000000)
        self.contract._EVMContract__init_hashes()
        # self.root = GameTree(parent=None)

    def get_contract_functions(self):
        return self.contract._hashes

    def create_new_var(self, var_type):
        if not self.symbolic_vars.get(var_type):
            self.symbolic_vars[var_type] = 0
        self.symbolic_vars[var_type] += 1
        var = self.m.make_symbolic_value(name = var_type+str(self.symbolic_vars[var_type]))
        return var

    # traverse the tree
    def DFS(self):
        # self.contract.withdraw(self.m.make_symbolic_value())
        #print(m._running_state_ids)

        root = GameTree(self.contract, self.m.initial_state, -1)

        argv = []
        var = self.create_new_var("uint")
        argv.append(var)
        tx_data = ABI.function_call("withdraw(uint256)", *argv)

        self.m.transaction(caller=self.malicious_account,
                    address=self.contract.address,
                    value=0,
                    data=tx_data,
                    gas=0xffffffffffff)
        print("after transaction")
        self.m.finalize()
        print(self.m.workspace)

        root.make_tree()
        root.print_game_tree();

        i=0
        while i < 5:
            print(self.m.get_balance(self.contract,i))
            i += 1

        # print(m._running_state_ids)
        # for state_id in m._running_state_ids:
        #     print("balance {}".format(m.get_balance(self.malicious_account,state_id)))

        # for fun_name, entries in self.get_contract_functions().items():
        #     if len(entries) > 1:
        #         sig = entries[0].signature[len(name):]
        #         raise EthereumError(
        #             f'Function: `{name}` has multiple signatures but `signature` is not '
        #             f'defined! Example: `account.{name}(..., signature="{sig}")`\n'
        #             f'Known signatures: {[entry.signature[len(name):] for entry in self._hashes[name]]}')
        #     variables_type = entries[0].signature.split("(")[1].replace(")","").split(",")
        #     argv = []
        #     for var_type in variables_type:
        #         var = self.create_new_var(var_type)
        #         argv.append(var)

        #     tx_data = ABI.function_call(str(entries[0].signature), *argv)
        #     print("before transaction", str(entries[0].signature))
        #     m.transaction(caller=self.malicious_account,
        #                 address=self.contract.address,
        #                 value=0,
        #                 data=tx_data,
        #                 gas=0xffffffffffff)

    def parse_property(self, property):
        self.prop = property
        self.z3_prop = self.lp.parser.parse(property)

    def create_z3_property(self, p_node, z3_vars):
        # p_node: parsing node
        # z3_vars: variables inheritate from the parent node, a list
        if p_node.type == "LEAF":
            if z3_vars == []:
                z3_vars = [0]
            if p_node.str == "true":
                return True
            elif p_node.str == "false":
                return False
            else:
                func_name = p_node.str.replace("\'","")
                if not self.z3_func.get(func_name):
                    self.z3_func[func_name] = Function(func_name, IntSort(), BoolSort())
                return self.z3_func[p_node.str.replace("\'","")](z3_vars[0])
        elif p_node.type == "NOT":
            return Not(self.create_z3_property(p_node.child, z3_vars))
        elif p_node.type == "AND":
            return And(self.create_z3_property(p_node.left, z3_vars), self.create_z3_property(p_node.right, z3_vars))
        elif p_node.type == "OR":
            return Or(self.create_z3_property(p_node.left, z3_vars), self.create_z3_property(p_node.right, z3_vars))
        elif p_node.type == "NEXT":
            # z3_vars[0] = z3_vars[0] + 1
            old_var = z3_vars[0]
            z3_vars[0] = self.gen_z3_var()
            return Exists(z3_vars[0], And(z3_vars[0] == old_var + 1, self.create_z3_property(p_node.child, z3_vars)))
        elif p_node.type == "UNTIL":
            if z3_vars == []:
                z3_vars = [0,self.gen_z3_var(),self.gen_z3_var()]
            if len(z3_vars) == 1:
                z3_vars = [z3_vars[0],self.gen_z3_var(),self.gen_z3_var()]
            left_vars = [z3_vars[2]]
            right_vars = [z3_vars[1]]
            return Exists(z3_vars[1], 
                       And(
                           And(
                               z3_vars[1]>=z3_vars[0],
                               self.create_z3_property(p_node.right, right_vars)
                           ),
                           ForAll(
                               z3_vars[2],
                               Implies(
                                   And(
                                       z3_vars[0] <= z3_vars[2],
                                       z3_vars[2] < z3_vars[1],
                                   ),
                                   self.create_z3_property(p_node.left, left_vars)
                               )
                           )
                       )
                   )

    def gen_z3_var(self):
        self.z3_var_counter += 1
        return Int("var"+str(self.z3_var_counter))

sampleProperty = "((-('p71')) || (true U ('p96')))"
# sampleProperty = "('r' U ('p1' U X ('p2' U ('p3')))) && ((('p1' U (('p2' U 'p4') U ('q' && 'r')))) U 'r')"

bmc = BMC()
bmc.parse_property(sampleProperty)
m = ManticoreEVM()
print(m._initial_state)
bmc.init_manticore(m)
bmc.create_z3_property(bmc.z3_prop, [])

bmc.DFS()



