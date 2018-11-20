from manticore.ethereum import ManticoreEVM
from GameTree import GameTree
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

def create_new_var(var_type):
    if not symbolic_vars.get(var_type):
        symbolic_vars[var_type] = 0
    symbolic_vars[var_type] += 1
    var = m.make_symbolic_value(name = var_type+str(symbolic_vars[var_type]))


m = ManticoreEVM()
# user_account = m.create_account(balance=1000)
# user_sol_account = m.solidity_create_contract(contract_src, owner=user_account)
contract_account = m.create_account(balance=1000)
malicious_account = m.create_account(balance=1000)
contract_sol_account = m.solidity_create_contract(contract_src, owner=contract_account)
contract_sol_account._EVMContract__init_hashes()

root = GameTree(m,contract_sol_account)

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





# for state_id in m._running_state_ids:
#     print("balance {}".format(m.get_balance(contract_account,state_id)))
#     print("pc {}".format(m.load(state_id)._platform.current_vm))

