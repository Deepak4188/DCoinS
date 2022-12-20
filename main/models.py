from datetime import datetime
from hashlib import sha256
from json import dumps
from urllib.parse import urlparse
import requests

# Defining The Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.createBlock(nonce = 1, previousHash = '0'*64) # Creating the Genesis Block
        self.nodes = set()


    def createBlock(self, nonce, previousHash):
        block = {
            'index': len(self.chain)+1,
            'nonce': nonce,
            'transactions': self.transactions,
            'previousHash':previousHash,
            'timestamp': str(datetime.now())
        }
        self.transactions = []
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

    def addTransactions(self, sender, receiver, amount): # adding transaction in the transactions list
        self.transactions.append({'sender':sender, 'receiver':receiver, 'amount':amount})
        previousBlock = self.getPreviousBlock()
        return previousBlock['index'] + 1 # returning the block index in which transactions are to be inserted

    def addNode(self, address): # adding a new node in the network
        parsedUrl = urlparse(address)
        self.nodes.add(parsedUrl.netloc) # adding the parsed addess of the node in network


    def replaceChain(self): # replacing the chain with the longest valid chain in the network 
        network = self.nodes
        longestChain = None
        maxLength = len(self.chain)
        for node in network:
            response = requests.get(f"http://{node}/getChain").json() # calling getChain method of different nodes
            chain = response['chain']
            length = response['length']
            if length > maxLength and self.isChainValid(chain):
                maxLength = length
                longestChain = chain
        if longestChain:
            self.chain = longestChain
            return True
        return False