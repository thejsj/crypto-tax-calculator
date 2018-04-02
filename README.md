# Crypto Tax Calculator

```
$ python main.py --file transactions-ltc.csv --base-currency USD
[{'amount': 74.39,
  'buy_price': 32.62,
  'currency': 'LTC',
  'date': datetime.datetime(2017, 6, 12, 0, 0),
  'gain': -311.6940999999998,
  'sell_price': 28.43},
 {'amount': 20.58,
  'buy_price': 28.97,
  'currency': 'LTC',
  'date': datetime.datetime(2017, 6, 12, 0, 0),
  'gain': -11.113199999999981,
  'sell_price': 28.43}]
```

### CSV Format

```
date: String(%m/%d/%Y)
currency_from: Float
currency_to: Float
amount_from: Float
amount_to: Float
price: Float (Only necessary txs not in base currency)
basis/fees: Float (Optional. Denomenated in base currency)
```

## Testing

```
python -m unittest discover .
```
