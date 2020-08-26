# Main simulator
import sys
import numpy as np
from scipy.sparse import csr_matrix

from Parser import Parser
from Device import Device
from Circuit import Circuit
from Matrix import Matrix
from Analysis import Analysis

if (len(sys.argv) != 2):
	print("Usage: python %s <name of circuit file>" % (sys.argv[0]))
	exit()
filename = sys.argv[1]
print("\n")

print("PySim - Parsing...")
p = Parser(filename)
p.parse()
p.print()
print("PySim - Parsing done...")
print("\n")

print("PySim - Building circuit...")
nodes = p.nodes
cir = Circuit(nodes)
lastnode = len(nodes)
branches = 0
for card in p.cards:
	branch = cir.addDevice(card, lastnode)
	if (branch):
		lastnode += 1
		branches += 1
cir.print()
print("PySim - Done building circuit...")
print("\n")

print("PySim - Initializing matrix...")
nodes = p.nodes
print("No. of nodes in circuit: %d" % (len(nodes)))
print("No. of branch currents in circuit: %d" % (branches))
size = len(nodes) + branches
m = Matrix(size)
m.print()
print("PySim - matrix initialized...")
print("\n")

print("PySim - Creating devices and stamping matrix...")
print("No. of devices in circuit: %d" % (len(p.cards)))
# cir.stamp(m)
print("PySim - Matrix loaded...")
m.print()
print("\n")

a = Analysis(cir, m)
(b, iter) = a.NewtonRaphson(5)
if (b):
	print("Newton Raphson converged in %d iterations..." %(iter))
else:
	print("Newton Raphson timed out after %d iterations" % (iter))
	
#a.linear_dc()

print("PySim - printing output...")
cir.output(m.x)

a.Transient(stop=20, step=0.1)

		
		