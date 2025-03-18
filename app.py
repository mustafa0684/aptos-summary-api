from flask import Flask, request, jsonify
import requests  # For API calls
import openai  # For AI summarization
import json  # For formatting transaction data

# Set your API Key (Replace with actual Move AI or OpenAI API Key)
openai.api_key = "your-move-ai-or-openai-key"

app = Flask(__name__)

def fetch_transactions(wallet_address):
    """
    Fetches the latest transactions for a given Aptos wallet address.
    """
    url = f"https://fullnode.mainnet.aptoslabs.com/v1/accounts/{wallet_address}/transactions"
    
    response = requests.get(url)  # Make an API request
    
    if response.status_code == 200:
        transactions = response.json()
        if transactions:
            return transactions  # Return transactions if available
        else:
            return {"message": "No transactions found for this wallet."}
    else:
        return {"error": f"Failed to fetch transactions. Status Code: {response.status_code}"}

def summarize_transaction(transaction):
    """
    Summarizes a raw Aptos blockchain transaction using AI.
    """
    prompt = f"Summarize this Aptos blockchain transaction in simple English:\n\n{json.dumps(transaction, indent=2)}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message["content"]
    
    except Exception as e:
        return f"Error in AI Summarization: {str(e)}"

@app.route("/summary", methods=["GET"])
def get_summary():
    wallet_address = request.args.get("wallet")
    
    if not wallet_address:
        return jsonify({"error": "No wallet address provided"}), 400
    
    transactions = fetch_transactions(wallet_address)
    
    if "error" in transactions:
        return jsonify(transactions), 500
    
    summaries = [summarize_transaction(txn) for txn in transactions[:5]]  # Limit to 5 transactions
    
    return jsonify({"wallet": wallet_address, "summaries": summaries})

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
