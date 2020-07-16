import sys
import glob
from scipy.stats import binom_test

# Eduard et al. 2014 https://doi.org/10.1093/bioinformatics/btu499
# usage syntax
# python3 mewtate_hotspot_reg.py 6M0J mutation.txt

# mutation.txt is a tab-separted file containing mutated aminoacid, chain, atom position in decreasing order per line
# to extract start and end residue (suitable for single chain)
# example	
# TYR	A	364
# PHE	A	367
# GLY	A	614	 

# example output p-value and common mutation (if present between user input and PDB structure)
# common_mutation = [('THR', 'E', '333')]
# p-value = 0.015077613248824657


# PDB input and mutation.txt input
pdb_inp = sys.argv[1]
mut_inp = sys.argv[2]

# mutation file processing
mut = open(mut_inp.strip(),"r")
start_res = []
end_res = []
mut_lst = []
for lines in mut:
	line = lines.strip().split()
	aminoacid = line[0]
	chain = line[1]
	atompos = line[2]
	mut_lst.append([aminoacid,chain,atompos])

# PDB file processing
pdb = open(pdb_inp.strip(),"r")
pdb_lst = []
for lines in pdb:
	if lines.startswith('ATOM'):
		line = lines.strip().split()
		if line[2] == 'CA':
			aminoacid = line[3]
			chain = line[4]
			atompos = line[5]
			pdb_lst.append([aminoacid,chain,atompos])

# PDB chain extracted from the input file
chain=(mut_lst[0][1])

chain_var = chain

def my_func():
    global chain_var
    get_chain()

PL_chain=[]
for chain in pdb_lst:
	if chain[1] == chain_var:
		PL_chain.append(chain)		

# PL = total length of the protein in PDB		
PL = len(PL_chain)

# common mutation between user supplied mutations and mutations already present in the pdb 

pdb_tuple = [tuple(x) for x in pdb_lst]
mut_tuple = [tuple(y) for y in mut_lst]
common_mut = set(pdb_tuple) & set(mut_tuple)
print("common_mutation =",list(common_mut))

# start and end residues  extracted from user mutation.txt file
start_res = (mut_lst[0][2])
end_res = (mut_lst[-1][2])

# RL = total length of the region
RL = (int(end_res))-(int(start_res))

# RM = total mutations in the region
RM = len(mut_lst)

# PM = total mutations in the protein from the database (known or predicted mutations of protein, database linking to mewtate work in progress), example PM = 100
PM = 100

p_val = binom_test(RM, PM, RL/PL, alternative = 'greater')
print("p-value =", p_val)

