from manticore.ethereum import ManticoreEVM
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
}
"""
m = ManticoreEVM()

# user_account = m.create_account(balance=1000)
# user_sol_account = m.solidity_create_contract(contract_src, owner=user_account)
contract_account = m.create_account(balance=1000)
contract_sol_account = m.solidity_create_contract(contract_src, owner=contract_account)

print("balance {}".format(m.get_balance(contract_account)))

contract_sol_account.withdraw(m.make_symbolic_value())

for state_id in m._running_state_ids:
    print("balance {}".format(m.get_balance(contract_account,state_id)))
    print("pc {}".format(m.load(state_id)._platform.current_vm))