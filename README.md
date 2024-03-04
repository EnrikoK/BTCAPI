AdCash Backend Services & API Internship Assignment

Small REST API built in Python using the built in Sqlite3 database, that comes with python, Flask
and SQLAlchemy for ORM. As the API uses the built in Sqlite3 database, no further configuration is
needed for that. Just install the dependencies and run the API. I also wrote some tests although 
I am not so proficient at it.

Install the required packages

```
pip install -r requirements.txt
```


To run the app cd into the folder and run:

```
python run.py
```


If you want to run the unit tests run:

```
python test.py
```


The API has 4 endponts:

[POST] /create-dummies
Creates an unused transaction to the database

Request body example:
```
{
    "amount" : 12.345
}
```

[POST] /create-transaction
Insert amount in EUR to create a new BTC transaction

Request body example:
```
{
    "amount":999.1
}
```
[GET] /show-balance
Returns the balance in BTC and EUR

Response 200 example:
```
{
	"balance_BTC": 2.0,
	"balance_EUR": 114079.058018
}
```

[GET] /all-transactions

Response 200 example:
```
[
	{
		"amount": 2.0,
		"created": "Sun, 03 Mar 2024 19:26:02 GMT",
		"hash": "8538f96e09a543620ca9ac2e0aaed36e93d0f6e0970ec33448b8abbf3d01a1ac",
		"spent": true
	},
	{
		"amount": 1.9575683263521724,
		"created": "Sun, 03 Mar 2024 19:26:16 GMT",
		"hash": "05a86eee3d4440e5421ca4f46f4c3736c0b4bf30ab5dd582a00e328d559a2b53",
		"spent": false
	}
]
```
