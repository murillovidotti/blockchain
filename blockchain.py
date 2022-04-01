import datetime #hora/hora de cada bloco criado
import hashlib #produção de Hashs
import json #fazer leitura dos hashs
from flask import Flask, jsonify #fazer os requests e exibir os resultados

#criação do bloco genesis

class Blockchain:

    def __init__(self):
        self.chain = [] #criação de lista
        self.create_block(proof = 1, previous_hash = '0')

    def create_block(self, proof, previous_hash): #criar o bloco com base no anterior
        block = {'index': len(self.chain) + 1, #criar dicionario
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)#inclusão do bloco 
        return block

    def get_previous_block(self): #retornar o bloco anterior
        return self.chain[-1]

    def proof_of_work(self, previous_proof): #configuraçoes de mineração 
        new_proof = 1
        check_proof = False #checkar se prova é correta (se não for ele é criado new proof até achar a solução do problema "proof")
        while check_proof is False: 
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() #produzir o hash
            if hash_operation[:4] == '0000': #nivel de dificuldade de mineração
                check_proof = True #checkar se resolve o proof
            else:
                new_proof += 1 #criar um novo hash
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode() #gerar o bloco com sting "traduzir"
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):#verificar se o proof  é valido 
        previous_block = chain[0] #indice do bloco anterior
        block_index = 1 #indice do bloco atual
        while block_index < len(chain): #passar por todos os blocos
            block = chain[block_index] 
            if block['previous_hash'] != self.hash(previous_block): #verificar se o hash atual é o igual o hash anterior
                return False
            previous_proof = previous_block['proof'] # proof do bloco anterior
            proof = block['proof'] # proof do bloco atual
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000': # verificar se o hash é valido
                return False
            previous_block = block
            block_index += 1
        return True


app = Flask(__name__)


blockchain = Blockchain() #estanciar a blockchain


@app.route('/mine_block', methods = ['GET'])#minerar o bloco
def mine_block():
    previous_block = blockchain.get_previous_block() #estanciar o bloco anterior
    previous_proof = previous_block['proof'] #receber o bloco anterior
    proof = blockchain.proof_of_work(previous_proof) #proof do bloco atual
    previous_hash = blockchain.hash(previous_block) # bloco atual para mineracao
    block = blockchain.create_block(proof, previous_hash) #criação do bloco
    response = {'message': 'Voce acabou de minerar um bloco!', 
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200 # está requisição esta bem sucedida 


@app.route('/get_chain', methods = ['GET']) #retornar todo o bloco
def get_chain():
    response = {'chain': blockchain.chain, #dicionario
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is_valid', methods = ['GET']) #verificar o bloco é valido
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : ' Blockchain  valido '}
    else:
        response = {'message' : ' Blockchain nao e valido '}
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)
