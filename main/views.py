from django.http import JsonResponse
from .models import Blockchain
from uuid import uuid4
import json

# Creating the node address
nodeAddress = str(uuid4()).replace("-", "")

# Creating The Blockchain
blockchain = Blockchain()

# Mining a new block and adding it to blockchain
def mineBlock(request):
    previousBlock = blockchain.getPreviousBlock()
    previousNonce = previousBlock['nonce']
    nonce = blockchain.proofOfWork(previousNonce)
    transactions = blockchain.addTransactions(sender=nodeAddress, receiver="Deepak", amount=1)
    previousHash = blockchain.getHash(previousBlock)
    block = blockchain.createBlock(nonce, previousHash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'nonce':block['nonce'],
                'transactions': block['transactions'],
                'timestamp':block['timestamp'],
                'previousHash':block['previousHash']
                }
    return JsonResponse(response)


# Getting the full blockchain
def getChain(request):
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)
                }
    return JsonResponse(response)


# Checking whether the blockchain is valid or not
def isChainValid(request):
    valid = blockchain.isChainValid(blockchain.chain)
    if valid:
        return JsonResponse({'message':'All GOOD! Blockchain is valid...'})
    return JsonResponse({'message':'SECURITY! Blockchain is hacked...'})


# Adding a new transaction to the blockchain
def addTransactions(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        transactionsKeys = ['sender', 'receiver', 'amount']
        if not all(key in json_data for key in transactionsKeys):
            return "Some elements of transactions are missing..."
        index = blockchain.addTransactions(sender=json_data['sender'], receiver=json_data['receiver'], amount=json_data['amount'])
        return JsonResponse({'message': f"This transaction will be added to Block #{index}"})


# Connecting the new nodes in our network
def connectNode(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        nodes = json_data['nodes']
        if nodes is None:
            return "No new node to connect..."
        for node in nodes:
            blockchain.addNode(node)
        return JsonResponse({'message': "All the nodes are now connected.\nThe DCoinS Blockchain now contains the following nodes:", 'total_nodes': list(blockchain.nodes)})


# Replacing the chain by the longest one if needed
def replaceChain(request):
    isChainReplaced = blockchain.replaceChain()
    if isChainReplaced:
        response = {'message': 'The nodes had different chains,  so the chain was replaced by the longest one...', 'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the longest one.', 'actual_chain': blockchain.chain}
    return JsonResponse(response)