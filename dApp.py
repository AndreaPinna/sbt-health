# Copyright 2024 Andrea Pinna - Università di Cagliari
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from web3 import Web3
import json
import contractInteraction.metaTransaction as metaTransaction


### SEPOLIA ####
# RPC SEPOLIA SLOW
#w3 = Web3(Web3.HTTPProvider('https://endpoints.omniatech.io/v1/eth/sepolia/public'))
# RPC SEPOLIA FAST
#w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia-rpc.publicnode.com'))

# Contract address in SEPOLIA
#contractAddress = "0x1190C9230ba110f39998E5c2E04c13f2E0Bd6743"

### POLYGON ####
# RPC POLYGON
w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com/'))
# Contract in POLYGON
contractAddress = "0x055eC04AebD1B5B48925b17B0e90E789A9e9AC31"

# ABI reading
with open("sbt.json", "r") as file:
    contractABI = json.load(file)
contractInstance = w3.eth.contract(address=contractAddress, abi=contractABI)

# Connection test: The contract function name() must return  "SoulBoundVaccine": the name stored in the contract
print(contractInstance.functions.name().call())

# Certificate reading
def get_certificates(address_to):
    certificates =  contractInstance.functions.getCertificates(address_to).call()
    return (certificates)

def get_titleOf(vaccine_id):
    vaccine_name = contractInstance.functions.titleOf(vaccine_id).call()
    return (vaccine_name)



# Writing mode
# Load account from encrypted json file
#with open("private_keys/owner", "r") as file: #SEPOLIA
with open("private_keys/polygon", "r") as file: #POLYGON
    data = json.load(file)
recoveredPK = w3.eth.account.decrypt(data, 'PASSWORD')
owner = w3.eth.account.from_key(recoveredPK)
print(owner.address)

# SBT MINT (vaccination certificate)
def create_certificate(address_to, vaccine):
    receipt = metaTransaction.metaTransaction(w3,owner,contractInstance,0, 'safeMint',
                                          address_to, "", vaccine)
    return (receipt)

# SBT Burning
def burn(vaccine):
    receipt = metaTransaction.metaTransaction(w3,owner,contractInstance,0, 'burn',
                                         vaccine)
    return (receipt)
