import csv
import pprint
import sys
from datetime import datetime
import json
import argparse
import functools

def map_single_entry (entry, base_currency):
  entry['date'] = datetime.strptime(entry['date'], '%m/%d/%Y')
  entry['amount_from'] = float(entry['amount_from']) # Should throw error (Nothing in life is free)
  entry['amount_to'] = float(entry['amount_to']) # Should be handled
  entry['currency_to'] = entry['currency_to'].upper()
  entry['currency_from'] = entry['currency_from'].upper()
  if entry.has_key('basis'):
    entry['basis'] = float(entry['basis'])
  elif entry.has_key('fees'):
    entry['basis'] = float(entry['fees'])
  else:
    entry['basis'] = 0.0
  if entry['currency_to'] == base_currency:
    # We want to revert the order then there is no base currency
    entry['price'] = entry['amount_to'] / entry['amount_from']
  elif entry['currency_from'] == base_currency:
    entry['price'] = entry['amount_from'] / entry['amount_to']
  else:
    if not entry.has_key('price'):
        raise Exception("NO PRICE FOR NON BASE CURRENCY")
    entry['price'] = float(entry['price'])
  return entry

def get_entries(filename, base_currency):

  file = open(filename, 'rb')
  entries = list(csv.DictReader(file))
  entries = map(functools.partial(map_single_entry, base_currency=base_currency), entries)
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

def get_sales(taxable_entries, amounts):
    first_entry = taxable_entries.pop()
    sales = add_taxable_sale(first_entry, taxable_entries, amounts, [])
    return sales[::-1] # Reverse list

def add_taxable_sale(entry, entries, amounts, sales):
    if (entry == None and len(entries) == 0):
        return sales
    # Find the last amount + calculate price diff
    last_amount = amounts[entry['currency_from']][-1].copy() # LIFO
    new_sale = {
        'sell_date': entry['date'],
        'buy_price': last_amount['price'],
        'buy_date': last_amount['date'],
        'sell_price': entry['price'],
        'currency': entry['currency_from'],
        }
    # If amount is the same as entry
    if last_amount['amount'] == entry['amount_from'] or last_amount['amount'] < entry['amount_from']:
        amounts[entry['currency_from']].pop()
        new_sale['amount'] = last_amount['amount']
    else:
        amounts[entry['currency_from']][-1]['amount'] -= entry['amount_from']
        new_sale['amount'] = entry['amount_from']
    new_sale['net_proceeds'] = (new_sale['amount'] * new_sale['sell_price']) - entry['basis']
    new_sale['cost'] = new_sale['amount'] * new_sale['buy_price']
    new_sale['gain'] = new_sale['net_proceeds'] - new_sale['cost']

    sales.append(new_sale)

    # change the entry
    if last_amount['amount'] == entry['amount_from'] or last_amount['amount'] > entry['amount_from']:
        if (len(entries) == 0):
            return sales
        entry = entries.pop()
    else:
        entry['amount_from'] -= last_amount['amount']

    return add_taxable_sale(entry, entries, amounts, sales)

def get_taxable_entries(entries, base_currency):
  return filter(lambda x : x['currency_from'] != base_currency, entries)

def analyze_taxable_sales (filename, base_currency="USD"):
  entries = get_entries(filename, base_currency)
  amounts = get_currency_amounts(entries)
  taxable_entries = get_taxable_entries(entries, base_currency)
  return get_sales(taxable_entries, amounts)

def main():
  parser = argparse.ArgumentParser(description='Calculate gains from transactions')
  parser.add_argument('--file',
                   help='Filename for csv')
  parser.add_argument('--base-currency', default="USD",
                   help='Base currency (Default "USD")')
  parser.add_argument('--format', default="pprint",
                   help='Output format (pprint, table, csv)')
  args = parser.parse_args()

  sales = analyze_taxable_sales(args.file, args.base_currency)
  if args.format == 'pprint':
    pprint.pprint(sales)
  elif args.format == 'table':
    from tabulate import tabulate
    print tabulate(sales, tablefmt="plain", headers="keys")
  elif args.format == 'csv':
    keys = sales[0].keys()
    dict_writer = csv.DictWriter(sys.stdout, keys)
    dict_writer.writeheader()
    dict_writer.writerows(sales)
  else:
    raise Exception("Unrecognized --format passed")

if __name__== "__main__":
  main()
