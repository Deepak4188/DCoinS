from datetime import datetime
from hashlib import sha256
from json import dumps

# Defining The Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.createBlock(nonce = 1, previousHash = '0'*64) # Creating the Genesis Block


    def createBlock(self, nonce, previousHash):
        block = {
            'index': len(self.chain)+1,
            'nonce': nonce,
            'previousHash':previousHash,
            'timestamp': datetime.now()
        }
        self.chain.append(block)
        return block


    def getPreviousBlock(self):
        return self.chain[-1]


    def proofOfWork(self, previousNonce):
        nonce = 1
        while True: # finding nonce that satisfies the 4 starting zeroes condition of hash 
            hash = sha256(str(nonce**2 - previousNonce**2).encode()).hexdigest()
            if hash[:4] == '0000':
                break
            nonce += 1
        return nonce


    def getHash(self, block): # finds the hash for a block
        encodedBlock = dumps(block, sort_keys=True, default=str).encode()
        return sha256(encodedBlock).hexdigest()


    def isChainValid(self, chain):
        blockIndex = 1
        while blockIndex < len(chain):

            block = chain[blockIndex]
            previousBlock = chain[blockIndex-1]
            if block['previousHash'] != self.getHash(previousBlock): # Checking value of previous Hash with value of Hash of previous Block
                return False
            
            nonce = block['nonce']
            previousNonce = previousBlock['nonce']
            hash = sha256(str(nonce**2-previousNonce**2).encode()).hexdigest()
            if hash[:4] != '0000': # Checking whether the hash is valid or not i.e. starts with 0000 
                return False
    
            blockIndex += 1
        return True