#!/usr/bin/python

# ml_visualizer.py - Money laundering operation visualiser.
# Created on : 14 August 2023
# Author     : itsmevjnk
# Created for the SIT103 3.2HD assignment.

import json
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

with open('accounts.json', 'r') as f:
    accts = json.load(f)
    for acc in accts:
        if acc['fraud']:
            G.add_node(acc['num'])

with open('transactions.json', 'r') as f:
    transactions = json.load(f)
    for trans in transactions:
        if 'ML' in trans['fraud']:
            G.add_edge(trans['from'], trans['to'], weight = trans['amount'])

pos = nx.spring_layout(G, seed = 15)
nx.draw_networkx_nodes(G, pos, node_size = 700)
nx.draw_networkx_edges(G, pos, width=6)
nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels)

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.show()