from django.http import JsonResponse
from .models import Blockchain
# Creating The Blockchain
blockchain = Blockchain()

def mineBlock(request):
    previousBlock = blockchain.getPreviousBlock()
    previousNonce = previousBlock['nonce']
    nonce = blockchain.proofOfWork(previousNonce)
    previousHash = blockchain.getHash(previousBlock)
    block = blockchain.createBlock(nonce, previousHash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'nonce':block['nonce'],
                'timestamp':block['timestamp'],
                'previousHash':block['previousHash']
                }
    return JsonResponse(response)


def getChain(request):
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)
                }
    return JsonResponse(response)


def isChainValid(request):
    valid = blockchain.isChainValid(blockchain.chain)
    if valid:
        return JsonResponse({'message':'All GOOD! Blockchain is valid...'})
    return JsonResponse({'message':'SECURITY! Blockchain is hacked...'})