#!/usr/bin/python

# to_cypher.py - Utility for interpreting account and transaction information into Cypher data insertion queries.
# Created on : 21 August 2023
# Author     : itsmevjnk
# Created for the SIT103 3.2HD assignment.

import json

with open('bank_cy_data.cypher', 'w') as fo:
    with open('accounts.json', 'r') as fi:
        accts = json.load(fi)
        print(f'Writing account information ({len(accts)}).')
        for acc in accts:
            fo.write(f"CREATE (ac:Account {{num: {acc['num']}, name: '{acc['name']}'}}) MERGE (p:Phone {{phone: '{acc['phone']}'}}) MERGE (e:Email {{email: '{acc['email']}'}}) MERGE (ad:Address {{addr: '{acc['address']}'}}) CREATE (ac)-[:HAS]->(p), (ac)-[:HAS]->(e), (ac)-[:HAS]->(ad);\n")
    
    fo.write('\n')

    with open('transactions.json', 'r') as fi:
        transactions = json.load(fi)
        print(f'Writing transactions ({len(transactions)}).')
        for trans in transactions:
            if trans['amount'] > 0:
                fo.write(f"MATCH (ac_from:Account) WHERE ac_from.num = {trans['from']} MATCH (ac_to:Account) WHERE ac_to.num = {trans['to']} CREATE (ac_from)-[t:SENDS {{num: {trans['num']}, timestamp: {trans['timestamp']}, amount: {trans['amount']}}}]->(ac_to);\n")
    
