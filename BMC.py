from manticore.ethereum import ManticoreEVM
from GameTree import GameTree
from manticore.exceptions import EthereumError


from manticore.ethereum.abi import ABI

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

m = ManticoreEVM()

# object decides how to traverse the game tree
class BMC(object):
    def __init__(self, manticore=None):
        # user_account = m.create_account(balance=1000)
        # user_sol_account = m.solidity_create_contract(contract_src, owner=user_account)
        self.m = manticore
        self.contract_account = self.m.create_account(balance=1000)
        self.malicious_account = self.m.create_account(balance=1000)
        self.contract_sol_account = self.m.solidity_create_contract(contract_src, owner=contract_account)
        self.contract_sol_account._EVMContract__init_hashes()
        self.root = GameTree(self.m,contract_sol_account)
        self.symbolic_vars = {}
        self.gen_z3_var.z3_var_counter = 0
        self.z3_func = {}

    def create_new_var(self, var_type):
        if not symbolic_vars.get(var_type):
            symbolic_vars[var_type] = 0
        symbolic_vars[var_type] += 1
        var = m.make_symbolic_value(name = var_type+str(symbolic_vars[var_type]))
        return var

    # traverse the tree
    def DFS(self):
        for fun_name, entries in root.get_functions().items():
            if len(entries) > 1:
                sig = entries[0].signature[len(name):]
                raise EthereumError(
                    f'Function: `{name}` has multiple signatures but `signature` is not '
                    f'defined! Example: `account.{name}(..., signature="{sig}")`\n'
                    f'Known signatures: {[entry.signature[len(name):] for entry in self._hashes[name]]}')
            print(fun_name, entries[0].signature)
            variables_type = entries[0].signature.split("(")[1].replace(")","").split(",")
            argv = []
            for var_type in variables_type:
                var = create_new_var(var_type)
                argv.append(var)

            tx_data = ABI.function_call(str(entries[0].signature), *argv)

            m.transaction(caller=malicious_account,
                        address=root.contract.address,
                        value=0,
                        data=tx_data,
                        gas=0xffffffffffff)

    def create_z3_property(p_node, z3_vars):
        # p_node: parsing node
        # z3_vars: variables inheritate from the parent node
        if p_node.type == "LEAF":
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
            return Not(create_z3_property(p_node.child, z3_vars))
        elif p_node.type == "AND":
            return And(create_z3_property(p_node.left, z3_vars), create_z3_property(p_node.right, z3_vars))
        elif p_node.type == "OR":
            return Or(create_z3_property(p_node.left, z3_vars), create_z3_property(p_node.right, z3_vars))
        elif p_node.type == "NEXT":
            # z3_vars[0] = z3_vars[0] + 1
            old_var = z3_vars[0]
            z3_vars[0] = gen_z3_var()
            return Exists(z3_vars[0], And(z3_vars[0] == old_var + 1, create_z3_property(p_node.child, z3_vars)))
        elif p_node.type == "UNTIL":
            if z3_vars == []:
                z3_vars = [0,gen_z3_var(),gen_z3_var()]
            if len(z3_vars) == 1:
                z3_vars = [z3_vars[0],gen_z3_var(),gen_z3_var()]
            print (p_node, z3_vars)
            left_vars = [z3_vars[2]]
            right_vars = [z3_vars[1]]
            return Exists(z3_vars[1], 
                       And(
                           And(
                               z3_vars[1]>=z3_vars[0],
                               create_z3_property(p_node.right, right_vars)
                           ),
                           ForAll(
                               z3_vars[2],
                               Implies(
                                   And(
                                       z3_vars[0] <= z3_vars[2],
                                       z3_vars[2] < z3_vars[1],
                                   ),
                                   create_z3_property(p_node.left, left_vars)
                               )
                           )
                       )
                   )

    def gen_z3_var(self):
        gen_z3_var.z3_var_counter += 1
        return Int("var"+str(gen_z3_var.z3_var_counter))

