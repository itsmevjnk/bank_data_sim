#!/usr/bin/python

# simulator.py - Bank data generator/simulator
# Created on : 14 August 2023
# Author     : itsmevjnk
# Created for the SIT103 3.2HD assignment.

import random
import string
import json
import math

def generate_string(n = 10):
    return ''.join(random.choices(string.ascii_lowercase, k = n))

def generate_phone():
    return '0' + ''.join(random.choices(string.digits, k = 9))

def dump_json(obj, fname):
    with open(fname, 'w') as f:
        json.dump(obj, f, indent = 4)

n_accts = int(input('Number of accounts to create: '))

n_accts_fraud = int(input('Number of fraudulent accounts: '))
accts_fraud = random.sample(range(n_accts), n_accts_fraud)

n_fraudster = int(input('Number of fraudsters behind such fraudulent accounts: '))
fraudsters = [
    {
        'email': generate_string() + '@' + generate_string(5) + '.com',
        'phone': generate_phone(),
        'address': generate_string(20)
    } for i in range(n_fraudster)
]
dump_json(fraudsters, 'fraudsters.json')

accts = [] # List of account details
acct_nums = set(range(n_accts)) # List of account numbers
for a_num in acct_nums:
    acct = {
        'num': a_num,
        'fraud': (a_num in accts_fraud),
        'name': generate_string(),
        'email': generate_string() + '@' + generate_string(5) + '.com',
        'phone': generate_phone(),
        'address': generate_string(20)
    }
    if acct['fraud']:
        # fraudulent account, choose a fraudster and use their email, address or phone (or both)
        fraudster = random.choice(fraudsters)
        common = random.randint(1, 7) # 1 to 7 inclusive, will be mapped out as bit
        if common & 0b001: acct['email'] = fraudster['email']
        if common & 0b010: acct['phone'] = fraudster['phone']
        if common & 0b100: acct['address'] = fraudster['address']
    
    accts.append(acct)
dump_json(accts, 'accounts.json')

m_limit = int(input('Money threshold to trigger warning signal: '))

t_max = int(input('Maximum timestamp of transactions (in arbitrary unit): '))

trans = [] # list of transactions

n_trans_norm = int(input('Number of normal transactions: '))
for i in range(n_trans_norm):
    a_from = random.choice(list(acct_nums))
    a_to = random.choice(list(acct_nums - {a_from}))
    t_trans = random.randint(0, t_max)
    m_trans = round(random.uniform(0.1, 0.5) * m_limit, 2)
    trans.append({
        'num': len(trans),
        'timestamp': t_trans,
        'from': a_from,
        'to': a_to,
        'amount': m_trans,
        'fraud': 'None'
    })

n_accts_victim = int(input('Number of accounts that are victims of account theft: '))
for a_from in random.sample(acct_nums, n_accts_victim):
    t_from = random.randint(0, t_max)
    for i in range(random.randint(5, 10)):
        a_to = random.choice(accts_fraud)
        t_trans = random.randint(t_from, min(t_max, int(t_from + 0.001 * t_max)))
        m_trans = round(random.uniform(0.8, 1.2) * m_limit, 2)
        trans.append({
            'num': len(trans),
            'timestamp': t_trans,
            'from': a_from,
            'to': a_to,
            'amount': m_trans,
            'fraud': 'Theft'
        })

n_ml_source = int(input('Number of money laundering source accounts: '))
accts_ml_source = random.sample(accts_fraud, n_ml_source)

n_ml_target = int(input('Number of money laundering target accounts: '))
accts_ml_target = random.sample(set(accts_fraud) - set(accts_ml_source), n_ml_target)

accts_ml_inter = set(accts_fraud) - set(accts_ml_source) - set(accts_ml_target)

m_ml_vol = int(input('Amount of money needing to be laundered: '))

n_shuffle = int(input('Minimum number of shuffle passes between intermediary accounts: '))

accts_ml_inter_bal = {
    n: random.uniform(0.01, 0.1) * m_limit for n in accts_ml_inter # for keeping track of money transferred across intermediary accounts
}

# dispense money from source
for a_from in accts_ml_source:
    t_trans = 0
    m_total = m_ml_vol / n_ml_source
    a_inter = random.sample(accts_ml_inter, max(2, math.ceil(m_total / m_limit)))
    for a_to in a_inter:
        t_trans += random.randint(0, 0.01 * t_max)
        m_trans = round(m_total / len(a_inter), 2)
        accts_ml_inter_bal[a_to] += m_trans
        trans.append({
            'num': len(trans),
            'timestamp': t_trans,
            'from': a_from,
            'to': a_to,
            'amount': m_trans,
            'fraud': 'ML Source'
        })
dump_json(accts_ml_inter_bal, 'ml_inter_0.json')

# shuffle money between intermediary accounts
shuffle_pass = 1
shuffle_more = False
while True:
    for a_from in accts_ml_inter:
        if shuffle_more and accts_ml_inter_bal[a_from] < m_limit: continue # our focus is now to share money out of larger accounts
        for a_to in accts_ml_inter:
            if accts_ml_inter_bal[a_from] < 0.001 * m_limit: break # only continue if there is still money
            if accts_ml_inter_bal[a_to] >= 2 * m_limit: continue # do not send more money into accounts with lots of money
            t_trans = random.randint(0, t_max)
            m_trans = round(random.uniform(0.1, min(accts_ml_inter_bal[a_from] / m_limit, 0.2)) * accts_ml_inter_bal[a_from], 2)
            if (accts_ml_inter_bal[a_from] - m_trans <= 0.001 * m_limit and accts_ml_inter_bal[a_from] < m_limit): m_trans = round(accts_ml_inter_bal[a_from], 2) # dump all the money
            accts_ml_inter_bal[a_from] -= m_trans; accts_ml_inter_bal[a_to] += m_trans
            trans.append({
                'num': len(trans),
                'timestamp': t_trans,
                'from': a_from,
                'to': a_to,
                'amount': m_trans,
                'fraud': f'ML Inter {shuffle_pass}'
            })
            if accts_ml_inter_bal[a_from] < 0:
                print(f'{a_from} -({m_trans})-> {a_to} and now only has {accts_ml_inter_bal[a_from]}')
    dump_json(accts_ml_inter_bal, f'ml_inter_{shuffle_pass}.json')
    
    shuffle_pass += 1
    if shuffle_pass <= n_shuffle: continue # continue shuffling

    # check if we need to shuffle more
    shuffle_more = False
    for a_num in accts_ml_inter:
        if accts_ml_inter_bal[a_num] >= m_limit:
            shuffle_more = True
            break
    
    if shuffle_more:
        print('Shuffling one more time.')
        continue
    else: break

# dump money to target accounts
acct_iterator = 0
t_trans = int(0.8 * t_max)
for a_from, m_trans in accts_ml_inter_bal.items():
    if m_trans == 0: continue # empty accounts already
    a_to = accts_ml_target[acct_iterator // len(accts_ml_inter_bal)]
    t_trans += random.randint(0, 0.01 * t_max)
    acct_iterator += 1
    trans.append({
        'num': len(trans),
        'timestamp': t_trans,
        'from': a_from,
        'to': a_to,
        'amount': round(m_trans, 2),
        'fraud': 'ML Target'
    })

dump_json(trans, 'transactions.json')