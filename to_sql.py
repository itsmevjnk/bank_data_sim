#!/usr/bin/python

# to_sql.py - Utility for interpreting account and transaction information into SQL data insertion queries.
# Created on : 14 August 2023
# Author     : itsmevjnk
# Created for the SIT103 3.2HD assignment.

import json

with open('bank_sql_data.sql', 'w') as fo:
    with open('accounts.json', 'r') as fi:
        accts = json.load(fi)
        print(f'Writing account information ({len(accts)}).')
        for acc in accts:
            fo.write(f"INSERT INTO ACCOUNTS VALUES({acc['num']}, '{acc['name']}', '{acc['email']}', '{acc['phone']}', '{acc['address']}');\n")
    
    fo.write('\n')

    with open('transactions.json', 'r') as fi:
        transactions = json.load(fi)
        print(f'Writing transactions ({len(transactions)}).')
        for trans in transactions:
            if trans['amount'] > 0:
                fo.write(f"INSERT INTO TRANSACTIONS VALUES({trans['num']}, {trans['timestamp']}, {trans['from']}, {trans['to']}, {trans['amount']});\n")

    fo.write('\nCOMMIT;\n')
