# Crypto Tax Calculator

Calculate your cryptocurrency gains from a CSV with all transactions.

Provides all the fields needed to input into TurboTax.

### Usage

```
$ python main.py --help
usage: main.py [-h] [--file FILE] [--base-currency BASE_CURRENCY]
               [--format FORMAT]

Calculate gains from transactions

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           Filename for csv
  --base-currency BASE_CURRENCY
                        Base currency (Default "USD")
  --format FORMAT       Output format (pprint, table, csv)
```

### Sample Output

```
$ python main.py --file test/2.csv  --base-currency USD --format table
  cost    net_proceeds  sell_date              buy_price    sell_price  currency      amount  buy_date               gain
   100             200  2017-01-03 00:00:00           10            20  LTC               10  2017-01-01 00:00:00     100
    25             100  2017-01-03 00:00:00            5            20  LTC                5  2017-01-02 00:00:00      75
    25             150  2017-01-04 00:00:00            5            30  LTC                5  2017-01-02 00:00:00     125
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
