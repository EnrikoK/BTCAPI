import unittest
from app import app, db
import json
import requests

class TestAPI(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    
    def test_createdummies(self):
        payload = {"amount":10}
        resp = self.app.post('/create-dummies',data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code,200)

    def test_createdummies_bad_json(self):
        payload = {"amount":"value"}
        resp = self.app.post('/create-dummies',data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code,400)

    def test_createdummies_neg_amount(self):
        payload = {"amount":-100}
        resp = self.app.post('/create-dummies',data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code,400)


    def test_get_all_transactions(self):
        payload = {"amount":10}
        self.app.post('/create-dummies',data=json.dumps(payload), content_type='application/json')
        resp = self.app.get('/all-transactions')
        self.assertEqual(resp.status_code,200)
        self.assertEqual(json.loads(resp.data)[0]['amount'],10.0)

    def test_create_transaction(self):
        #BTC to insert to the database for testing
        payload1 = {"amount":10}
        #Amount in EUR for transaction
        payload2 = {"amount":999}

        self.app.post('/create-dummies',data=json.dumps(payload1), content_type='application/json')
        #Testing the transaction
        resp = self.app.post('/create-transaction',data=json.dumps(payload2), content_type='application/json')
        self.assertEqual(json.loads(resp.data)['message'],"success")
        self.assertEqual(resp.status_code,200)
        

    def test_create_transaction_no_funds(self):
        #BTC to insert to the database for testing
        payload1 = {"amount":1}
        #Amount in EUR for transaction
        payload2 = {"amount":99999999}

        self.app.post('/create-dummies',data=json.dumps(payload1), content_type='application/json')
        #Testing the transaction
        resp = self.app.post('/create-transaction',data=json.dumps(payload2), content_type='application/json')
        self.assertEqual(json.loads(resp.data)['message'],"Out of funds")
        self.assertEqual(resp.status_code,400)
        

    def test_create_tranasction_bad_input(self):
        #BTC to insert to the database for testing
        payload1 = {"amount":1}
        #Amount in EUR for transaction
        payload2 = {"amount":"bad value"}

        self.app.post('/create-dummies',data=json.dumps(payload1), content_type='application/json')
        #Testing the transaction
        resp = self.app.post('/create-transaction',data=json.dumps(payload2), content_type='application/json')
        self.assertEqual(json.loads(resp.data)['message'],"The amount must be a floating point number")
        self.assertEqual(resp.status_code,400)
        
    def test_create_transaction_neg_value(self):
        #BTC to insert to the database for testing
        payload1 = {"amount":1}
        #Amount in EUR for transaction
        payload2 = {"amount":-5000}

        self.app.post('/create-dummies',data=json.dumps(payload1), content_type='application/json')
        #Testing the transaction
        resp = self.app.post('/create-transaction',data=json.dumps(payload2), content_type='application/json')
        self.assertEqual(resp.status_code,400)
        

    def test_get_balance(self):
        #BTC to insert to the database for testing
        payload = {"amount":1.5}

        self.app.post('/create-dummies',data=json.dumps(payload), content_type='application/json')

        resp = self.app.get('/show-balance')
        #Get the exchange rate
        get_exchange = requests.get('http://api-cryptopia.adca.sh/v1/prices/ticker').json()
        exchange_rate = float(get_exchange ['data'][0]['value'])

        self.assertEqual(resp.status_code,200)
        # Exchange rate can change mid request
        self.assertAlmostEqual(json.loads(resp.data)['balance_EUR'],1.5*exchange_rate)
        self.assertEqual(json.loads(resp.data)['balance_BTC'],1.5)


    def tearDown(self) -> None:
        with app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()