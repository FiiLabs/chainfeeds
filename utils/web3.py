from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/your-project-id'))

contract_address = '0x1234567890123456789012345678901234567890' # 合约地址
contract_abi = [...] # 合约ABI

contract = w3.eth.contract(address=contract_address, abi=contract_abi) # 加载合约对象

result = contract.functions.method_name(param1, param2).call() # 调用合约方法

print(result) # 处理返回结果