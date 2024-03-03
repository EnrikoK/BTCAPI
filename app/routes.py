from flask import jsonify, request,abort
from app import app, db
from app.models import Transactions
import requests

# Lists all transactions from the database
@app.route('/all-transactions', methods=['GET'])
def get_users():
    transactions = Transactions.query.all()
    print(transactions)
    return jsonify([{"hash":t.hash, "spent":t.spent, "amount":t.amount, "created":t.created_at} for t in transactions])

# Creates transactions
@app.route('/create-transaction', methods=['POST'])
def create_transaction():
    if(request.is_json):
        try:
            amount = request.get_json()['amount']
            
            # Get the exchange rate 
            get_exchange = requests.get('http://api-cryptopia.adca.sh/v1/prices/ticker').json()
            exchange_rate = float(get_exchange ['data'][0]['value'])
            
            #Check if the transaction is more than 0.00001 BTC
            amount_BTC = amount/exchange_rate
            if(amount_BTC < 0.00001): return jsonify({"message":"All transactions must be more than 0.00001 BTC in value"}), 400
            
            #Get all unused transactions
            transactions = Transactions.query.filter(Transactions.spent == False).order_by(Transactions.amount.desc()).all()
            
            #Use Greedy selection from transactions list
            #Subtract from the amount_BTC variable until transaction is covered or exeeded
            used_transactions = []
            
            for elem in transactions:
                if(amount_BTC <= 0):
                    break
                amount_BTC -= elem.amount
                used_transactions.append(elem)
            
            #chekc if the transaction sum is covered before confirming the used transactions
            if(amount_BTC > 0):
                return jsonify({"message":"Out of funds"}), 400
            else:
                for elem in used_transactions:
                    elem.spent = True
                if(amount_BTC != 0):
                    leftover = Transactions(abs(amount_BTC))
                    db.session.add(leftover)

                db.session.commit()
            
            return jsonify({"message":"success"}), 200

        except:
            return jsonify({"message":"Something went wrong..."}), 500
    else:
        return jsonify({"message":"Bad request"}), 400

# Shows the balance of un-used transactions in EUR and BTC
@app.route('/show-balance', methods=['GET'])
def show_balance():
    try:
        free_transactions = Transactions.query.filter(Transactions.spent == False).all()
        BTC_balance = 0
        for elem in free_transactions:
            BTC_balance += elem.amount
        
        get_exchange  = requests.get('http://api-cryptopia.adca.sh/v1/prices/ticker').json()
        exchange_rate = float(get_exchange ['data'][0]['value'])

        return jsonify({"balance_BTC":BTC_balance, "balance_EUR":BTC_balance*exchange_rate}), 200
    except:
        return jsonify({"message":"Something went wrong with the request, try again later."}), 500


#Endpoint to quickly create dummie values for the wallet database
@app.route('/create-dummies', methods=['POST'])
def create_dummies():
    if(request.is_json):
        new_transaction = Transactions(request.get_json()['amount'])
        db.session.add(new_transaction)
        db.session.commit()
        return '', 200
    else:
        abort(400)