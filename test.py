from manticore.ethereum import ManticoreEVM
from manticore.GameTree import GameTree
from manticore.exceptions import EthereumError

from manticore.ethereum.abi import ABI


symbolic_vars = {}


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
# user_account = m.create_account(balance=1000)
# user_sol_account = m.solidity_create_contract(contract_src, owner=user_account)
contract_account = m.create_account(balance=1000)
malicious_account = m.create_account(balance=1000)
contract_sol_account = m.solidity_create_contract(contract_src, owner=contract_account)
m.world.set_balance(contract_sol_account, 100000000)
contract_sol_account._EVMContract__init_hashes()

def create_new_var(var_type):
    if not symbolic_vars.get(var_type):
        symbolic_vars[var_type] = 0
    symbolic_vars[var_type] += 1
    var = m.make_symbolic_value(name = var_type+str(symbolic_vars[var_type]))
    return var

state = m.initial_state

root = GameTree(contract_sol_account,state, -1)

# trigger the remote function call by malicious account
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

    print(m._running_state_ids)
    


#m.finalize()



print("=====================================================================================================================")

root.make_tree()
root.print_game_tree();



def parse_game_tree(node):
    if not node.children:
        try:
            print("Leaf Node : " , node.state_id)
            new_state = m._executor._workspace.load_state(node.state_id, delete=False)
            print("account :" , new_state._platform.get_balance(int(contract_account)))
            print("maliciou account :" , new_state._platform.get_balance(int(malicious_account)))
            print("contract account :" , new_state._platform.get_balance(int(contract_sol_account)))
            print("=====================================================================================================================")
        except IOError:
            print("=====================================================================================================================")
        return

    for child in node.children:
        parse_game_tree(child)


parse_game_tree(root.root_node)