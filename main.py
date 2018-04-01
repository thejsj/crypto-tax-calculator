import csv
import pprint
from datetime import datetime
import json

def get_entries():
  entries = []
  with open('transactions-ltc.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        if (row[0] == "Date"):
            continue
        entries.append({
            'date': datetime.strptime(row[0], '%m/%d/%Y'),
            'currency_from': row[1],
            'currency_to': row[2],
            'amount_from': float(row[4] or 0),
            'amount_to': float(row[5] or 0),
            'price': float(row[6] or 0),
            'price_usd': float(row[7] or 0),
            'fees': float(row[8] or 0),
            'fees_usd': float(row[9] or 0),
            'taxable': row[12]
        })
  entries.sort(key=lambda x: x['date'])
  return entries

def get_currency_amounts(entries):
  amounts = {}
  for entry in entries:
    # Make sure key exists
    if not amounts.has_key(entry['currency_to']):
      amounts[entry['currency_to']] = []
    if not (entry['amount_to'] == 0) and not (entry['price'] == 0):
        amounts[entry['currency_to']].append({
            'amount': entry['amount_to'],
            'price': entry['price'],
            'date': entry['date']
        })
  return amounts

def get_taxable_entries(entries):
  return filter(lambda x : x['taxable'] == 'TRUE', entries)

def get_taxable_sales(taxable_entries, amounts):
    first_entry = taxable_entries.pop()
    sales = add_taxable_sale(first_entry, taxable_entries, amounts, [])
    return sales

def add_taxable_sale(entry, entries, amounts, sales):
    print "Entry"
    pprint.pprint(entry)
    if (entry == None and len(entries) == 0):
        return sales
    # Find the last amount + calculate price diff
    last_amount = amounts[entry['currency_from']][-1].copy() # LIFO
    new_sale = {
        'date': entry['date'],
        'buy_price': last_amount['price'],
        'sell_price': entry['price'],
        'currency': entry['currency_from'],
        }
    # If amount is the same as entry
    if last_amount['amount'] == entry['amount_from'] or last_amount['amount'] < entry['amount_from']:
        print "Case 1"
        amounts[entry['currency_from']].pop()
        new_sale['amount'] = last_amount['amount']
    else:
        print "Case 2"
        amounts[entry['currency_from']][-1]['amount'] -= entry['amount_from']
        new_sale['amount'] = entry['amount_from']
    new_sale['gain'] = new_sale['amount'] * (new_sale['sell_price'] - new_sale['buy_price'])

    sales.append(new_sale)

    # change the entry
    if last_amount['amount'] == entry['amount_from'] or last_amount['amount'] > entry['amount_from']:
        if (len(entries) == 0):
            return sales
        entry = entries.pop()
    else:
        entry['amount_from'] -= last_amount['amount']

    return add_taxable_sale(entry, entries, amounts, sales)

def main():
  entries = get_entries()
  amounts = get_currency_amounts(entries)
  pprint.pprint(amounts)
  taxable_entries = get_taxable_entries(entries)
  pprint.pprint(taxable_entries)
  taxable_sales = get_taxable_sales(taxable_entries, amounts)
  pprint.pprint(taxable_sales)

if __name__== "__main__":
  main()
