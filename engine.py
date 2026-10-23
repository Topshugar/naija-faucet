from flask import Flask, request, jsonify
from web3 import Web3
import os

app = Flask(__name__)

# CONFIG — Your Origin
BSC_TESTNET = "https://data-seed-prebsc-1-s1.binance.org:8545/"
TREASURY_PRIVATE_KEY = os.getenv("TREASURY_KEY") # Your wallet with trillions
NAIJA_TOKEN_ADDRESS = "0xYourDeployedNaijaTestBNB" # From Remix
FAUCET_CONTRACT_ADDRESS = "0xYourDeployedNaijaFaucet"

w3 = Web3(Web3.HTTPProvider(BSC_TESTNET))
treasury = w3.eth.account.from_key(TREASURY_PRIVATE_KEY)

# Hidden Engine 1: Auto-Mint when low
def check_and_mint_root():
    balance = get_treasury_balance()
    if balance < 10: # Less than 10 tBNB
        # Mint 1 Trillion to treasury from your origin
        print("Root carving — minting 1T nTBNB underground...")
        mint_trillion(treasury.address, 1)
    return balance

# Hidden Engine 2: Distribute 0.05
def distribute_to_student(student_wallet):
    check_and_mint_root()
    tx = {
        'to': student_wallet,
        'value': w3.to_wei(0.05, 'ether'),
        'gas': 21000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'nonce': w3.eth.get_transaction_count(treasury.address)
    }
    signed = w3.eth.account.sign_transaction(tx, TREASURY_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()

# API — What frontend calls
@app.route('/api/claim', methods=['POST'])
def claim():
    data = request.json
    student_wallet = data['wallet']
    payment_verified = data['paid'] # From Flutterwave webhook

    if not payment_verified:
        return jsonify({"error": "Pay 500 NGN first"}), 400

    tx_hash = distribute_to_student(student_wallet)
    return jsonify({
        "status": "success",
        "message": "0.05 tBNB sent from origin",
        "tx": tx_hash,
        "explorer": f"https://testnet.bscscan.com/tx/{tx_hash}"
    })

if __name__ == '__main__':
    app.run(port=5000)