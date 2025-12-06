#   
#   We define the in-degree matrix based on the vectors \vec{kin}^n = (kin^en;kin^in)
#   representing the excitatory and inhibitory in-degrees on nodes of type n\in\{e,i\}:
#       Kin = (\vec{kin}^e, \vec{kin}^i)
#             [[kin^ee,kin^ei],[kin^ie,kin^ii]],
#   where kin^ee represents the number of excitatory inputs each excitatory node has
#         kin^ei represents the number of excitatory inputs each inhibitory node has
#         kin^ie represents the number of inhibitory inputs each excitatory node has
#         kin^ii represents the number of inhibitory inputs each inhibitory node has
#   Similarly, the out-degree matrix is given by
#       Kout = (\vec{kout}^e, \vec{kout}^i)
#              [[kout^ee,kout^ie],[kout^ei,kout^ii]]
#   except that Kout is transposed to maintain the pattern (definition): kout^ie is
#   the number of excitatory targets each inhibitory node has and kout^ei is the number
#   of inhibitory targets each excitatory node has
#
#   By the Fulkerson-Chen-Anstee Theorem (1960s)...
#   We have 4 arc types {ee,ei,ie,ii} and to produce a corresponding need to add constraint
#   on the flow conservation for each type [cf. Chung & Lu 2002, https://link.springer.com/article/10.1007/PL00012580,
#   Bollobás et al. 2007, https://doi.org/10.1002/rsa.20168]:
#       ee: \sum_{n\in e} kin^en = \sum_{n\in e} kout^ne = mee
#       ei: \sum_{n\in i} kin^en = \sum_{n\in e} kout^ni = mei
#       ei: \sum_{n\in e} kin^in = \sum_{n\in i} kout^ne = mie
#       ii: \sum_{n\in i} kin^in = \sum_{n\in i} kout^ni = mii
#   where mnn is the total number of edges.
#
#   Algorithm: Multi-Type Directed Configuration Model
#   
#   Adjacency matrix has block structure: M = [[Mee,Mei],[Mie,Mii]]
#   Step 1: Generate each block separately using directed configuration model
#   
#   Or just use NEMtropy: Vallarano et al. 2021 (https://github.com/nicoloval/NEMtropy)
#   \rvwg2025

from gcbm_lib import *

e1 = Node(3,0)
e2 = Node(5,0)

e3 = Node(3,0.1)
Node.iterate(e3,10)

print([e.taur for e in Node.get_all_instances()])

print(len(Node.get_all_instances()))

eNodes = NodeFactory.create_nodes("eNode", 2, 0.5, 8)
print(len(eNode.get_all_instances()))
print(Node.get_states(eNodes))
print(eNode.batch_iterate())
print(eNode.batch_iterate())
print(eNode.batch_iterate())

iNodes = NodeFactory.create_nodes("iNode", 3, 0.5, 2)
print(len(iNode.get_all_instances()))
print(Node.get_states(iNodes))
print(iNode.batch_iterate())
print(iNode.batch_iterate())
print(iNode.batch_iterate())

print(Node.get_indices(iNodes))
print(Node.get_indices(eNodes))
N = eNode.count+iNode.count
print(N)

print(type(eNodes))
Nodes = eNodes + iNodes
print(Node.get_indices(Nodes))
print(Node.get_types(Nodes))

Kin = [[1,0],[0,0]]
Kout = [[1,1],[1,0]]

Net = Network(10, Nodes)
Net.generate_connections(Kin, Kout)
