from Bio.PDB import *
import requests
import os
from shutil import which 
from sys import exit
import glob
import json
import warnings
import argparse

# Missense3D paper: Ittisoponpisan et al. 2019 https://doi.org/10.1016/j.jmb.2019.04.009

# one-letter-code
olc = { 'ALA':'A', 'CYS':'C', 'ASP':'D', 'GLU':'E', 'PHE':'F', 'GLY':'G', 'HIS':'H', 'ILE':'I', 'LYS':'K', 'LEU':'L',
        'MET':'M', 'ASN':'N', 'PRO':'P', 'GLN':'Q', 'ARG':'R', 'SER':'S', 'THR':'T', 'VAL':'V', 'TRP':'W', 'TYR':'Y', }

# residue groups
hydrophobic = 'ACFILMVW'
hydrophilic = 'DEHKNQR'
neutral     = 'GPSTY'
positive    = 'HKR'
negative    = 'DE'

# DSSP sec_structure code
ssc = { 'H': 'Alpha helix', 'B': 'Beta bridge', 'E': 'Strand', 'G': '3-10 helix', 'I': 'Pi helix', 'T': 'Turn', 'S': 'Bend', '-':'None', 'C':'Coil' }

# Maximal ASA of amino acids
residue_max_acc = { 
    # Miller max acc: Miller et al. 1987 https://doi.org/10.1016/0022-2836(87)90038-6 
    # Wilke: Tien et al. 2013 https://doi.org/10.1371/journal.pone.0080635 
    # Sander: Sander & Rost 1994 https://doi.org/10.1002/prot.340200303 
    "Miller": { 
        "ALA": 113.0, "ARG": 241.0, "ASN": 158.0, "ASP": 151.0, "CYS": 140.0, "GLN": 189.0, "GLU": 183.0, "GLY": 85.0, "HIS": 194.0, "ILE": 182.0, 
        "LEU": 180.0, "LYS": 211.0, "MET": 204.0, "PHE": 218.0, "PRO": 143.0, "SER": 122.0, "THR": 146.0, "TRP": 259.0, "TYR": 229.0, "VAL": 160.0,     },     
    "Wilke": { 
        "ALA": 129.0, "ARG": 274.0, "ASN": 195.0, "ASP": 193.0, "CYS": 167.0, "GLN": 225.0, "GLU": 223.0, "GLY": 104.0, "HIS": 224.0, "ILE": 197.0,
        "LEU": 201.0, "LYS": 236.0, "MET": 224.0, "PHE": 240.0, "PRO": 159.0, "SER": 155.0, "THR": 172.0, "TRP": 285.0, "TYR": 263.0, "VAL": 174.0,     }, 
    "Sander": { 
        "ALA": 106.0, "ARG": 248.0, "ASN": 157.0, "ASP": 163.0, "CYS": 135.0, "GLN": 198.0, "GLU": 194.0, "GLY": 84.0, "HIS": 184.0, "ILE": 169.0,
        "LEU": 164.0, "LYS": 205.0, "MET": 188.0, "PHE": 197.0, "PRO": 136.0, "SER": 130.0, "THR": 142.0, "TRP": 227.0, "TYR": 222.0, "VAL": 142.0,     }, 
} 

class mewtate_struct_impact():

    """Methods to assess structural impact of the mutation."""

    def __init__( self, pdb, mutation, default_dir="path/to/pdbdir/" ): # mutation example: NE479K, where E is the pdb chain

        # retrieve pdb if required

        s = PDBParser( QUIET=True ).get_structure( pdb, default_dir+pdb+".pdb" )

        self.pdb = pdb
        self.default_dir = default_dir

        self.pdb_WT = s[0] # WT model (from SMCRA)
        c = self.pdb_WT[ mutation[1] ]
        r = c[ int( mutation[2:-1] ) ]

        self.target   = r
        self.mutation = mutation
        dssp_WT  = DSSP( self.pdb_WT, default_dir+pdb+".pdb", dssp="/home/houcemeddine/modules/dssp/bin/dssp-2.0.4-linux-i386" )
        self.ss_WT, self.rsa_WT = dssp_WT[( self.mutation[1], self.target.get_id() )][2], dssp_WT[( self.mutation[1], self.target.get_id() )][3]

        if mutation[0] != olc[ r.get_resname() ]:
            return "Given mutation does not match structure information" # or False??
            # validation: wt residue to match input mutation

        else:
        
            # To discuss: generate MUTANT pdb using FoldX here or generate it outside this module and give the filename?
            # I'm assuming a MUT file has been generated (e.g. $pdb + "_" + $mutation + ".pdb" )

            s = PDBParser( QUIET=True ).get_structure( pdb, default_dir+"/"+pdb+"_"+mutation+".pdb" )

            self.pdb_MUT = s[0] # MUT model
            c = self.pdb_MUT[ mutation[1] ]
            r = c[ int( mutation[2:-1] ) ]

            self.mutres = r
            dssp_MUT  = DSSP( self.pdb_MUT, default_dir+pdb+"_"+mutation+".pdb", dssp="C:/Users/Sherlyn/Downloads/dssp-2.0.4-win32.exe" )
            self.ss_MUT, self.rsa_MUT = dssp_MUT[( self.mutation[1], self.mutres.get_id() )][2], dssp_MUT[( self.mutation[1], self.mutres.get_id() )][3]


            ## Steps to assess structural impact to be finalized here

            output = [ mewtate_struct_impact.disulfide_breakage( self ),
                       mewtate_struct_impact.buried_Pro_introduced( self ),
                       mewtate_struct_impact.buried_glycine_replaced( self ),
                       mewtate_struct_impact.buried_hydrophilic_introduced( self ),
                       mewtate_struct_impact.buried_charge_introduced( self ),
                       mewtate_struct_impact.buried_charge_switch( self ),
                       mewtate_struct_impact.sec_struct_change( self ),
                       mewtate_struct_impact.buried_charge_replaced( self ),
                       mewtate_struct_impact.buried_exposed_switch( self ),
                       mewtate_struct_impact.gly_bend( self ),
                       mewtate_struct_impact.buried_hydrophilic_introduced( self ) ]
        
            ## Output -> json
            output = [ x for x in output if x!=False ]
            self.out = json.dumps( { 'pdb':self.pdb, 'mutation':self.mutation, 'foldx': 3.2, 'impact':output } )
               

    def disulfide_breakage( self ):      
        if self.mutation[0] == 'C':
            # check for presence of nearby CYS
            for res in self.pdb_WT[mutation[1]]: # model[chain]
                if res.get_resname() == 'CYS':
                    if res['SG'] - self.target['SG'] <= 3.3: # maximum S–S length is 3.3 Å
                        return "Disulfide breakage" #OR True 
        else:
            return False

    def buried_Pro_introduced( self ):
        if self.rsa_WT < 0.09 and self.mutation[-1]=='P':
            return "Buried Pro introduced" #OR True
        else:
            return False


    def buried_glycine_replaced( self ):
        if self.target.get_resname() == 'GLY' and self.rsa_WT < 0.09:
            return "Buried Gly replaced" #OR True
        else:
            return False
        

    def buried_hydrophilic_introduced( self ):
        if self.mutation[0] in hydrophobic and self.mutation[-1] in hydrophilic and self.rsa_WT < 0.09:
            return "Buried hydrophilic %s introduced"%self.mutres.get_resname() #OR True
        else:
            return False


    def buried_charge_introduced( self ):
        if self.mutation[0] not in positive+negative and self.mutation[-1] in positive+negative and self.rsa_WT < 0.09:
            return "Buried charge %s introduced"%self.mutres.get_resname() #OR True
        else:
            return False


    def buried_charge_switch( self ):
        if self.rsa_WT < 0.09:
            if self.mutation[0] in positive and  self.mutation[-1] in negative:
                return "Charge switch from positive to negative" #OR True
            elif self.mutation[0] in negative and  self.mutation[-1] in positive:
                return "Charge switch from negative to positive" #OR True
            else:
                return False
        else:
            return False


    def sec_struct_change( self ):
        if self.ss_WT != self.ss_MUT:    
            return "Change in secondary structure" #OR True
        else:
            return False


    def buried_charge_replaced( self ):
        if self.mutation[0] in positive+negative and self.mutation[-1] not in positive+negative and self.rsa_WT < 0.09:
            return "Buried charge %s replaced"%self.target.get_resname() #OR True
        else:
            return False


    def buried_exposed_switch( self ):
        if self.rsa_WT < 0.09 and self.rsa_MUT >= 0.09:
            return "Buried residue is exposed" #OR True
        elif self.rsa_WT >= 0.09 and self.rsa_MUT < 0.09:
            return "Exposed residue is buried" #OR True
        else:
            return False


    def gly_bend( self ):
        if self.mutation[0] == 'G' and self.ss_WT == 'S':
            return "Gly in bend replaced" #OR True
        else:
            return False


    def buried_hydrophilic_introduced( self ):
        if self.mutation[0] in hydrophilic and  self.mutation[-1] in hydrophobic and self.rsa_WT > 0.09:
            return "Buried hydrophilic %s introduced"%self.mutres.get_resname() #OR True
        else:
            return False


    ## UTILITIES

    def retrievepdb( self ):
        response = requests.get( "https://files.rcsb.org/download/" + self.pdb + ".pdb" )
        with open( self.default_dir + self.pdb + '.pdb', 'w' ) as q:
            q.write( response.text )


class FoldX:
    """docstring for FoldX"""
    def __init__(self, pdb):
        if os.path.exists(pdb) : 
            self.pdb = pdb
        else: 
            raise FileNotFoundError("File does not exist")
    
    def repair(self, override=True): 
        """
        if override = False it will try to find
            a repaired pdb structure with suffix "_Repair.pdb"
        else it will run a repair process by foldx
        """
        self.container_folder = os.path.dirname(os.path.abspath(self.pdb)) 
        self.basename = os.path.basename(self.pdb)
        if override :     
            if which("foldx") == None:
                exit("'foldx' not in PATH")
            # run foldx o repair the structure. For some reason foldx does not recognise a path to dir
            cmd="cd {0} ; foldx --command=RepairPDB --pdb={1}".format(self.container_folder, self.basename)
            print(cmd)
            os.system(cmd)
        else: 
            repaired_pdb = os.path.splitext(self.basename)[0]+"_Repair.pdb"
            if os.path.exists(self.container_folder+"/"+repaired_pdb) : 
                self.path_to_repaired_wt_structure = self.container_folder+"/"+repaired_pdb
                print("Repaired structure in {}".format(self.path_to_repaired_wt_structure))
            else: 
                raise OSError("{0} have no repaired structure ('*_Repair.pdb')  in {1}".format(self.basename, self.container_folder))
    
    def _jsonParse(self, json_file):
        """
        Parses json batch mutation file and return formated
        format for foldx
        """
        print(json_file)
        with open(json_file, 'r') as json_data:
            data = json.load(json_data)
        batch = []
        for series in data["batch"]:
            series_list = []
            for mutation in data["batch"][series]: 
                mut = data["batch"][series][mutation]
                series_list.append(mut["wt_residue"]+mut["chain"]+mut["position"]+mut["mut_residue"])
            batch.append(series_list)
        return batch


    def mutate(self, wt_res, mut_res, position, chain, mode = "single"):
        """
        mutate structre 
        """
        cmd = "cd {0} ; foldx --command=BuildModel --pdb={1} --mutant-file=individual_list_single.txt".format(self.container_folder, self.basename)
        if mode == 'single':
            # write the mutation individual file used by foldX
            expression_mut = wt_res+chain+str(position)+mut_res+';\n'
            with open(self.container_folder+"/"+"individual_list_single.txt", 'w') as mutant_file : 
                mutant_file.write(expression_mut)
                # run the calculation of the folding energy
                os.system(cmd)
        if mode == 'batch':
            pass

class PdbRead:
    def __init__(self,pdb):
        parser = PDBParser( QUIET=True )
        self.structure = parser.get_structure('S',pdb )
  
    def extractChain(self, chain, output): 
        if len(self.structure) >1: 
            raise warnings.warn("Multiple models in PDB, will use only the first")
        self.structure = self.structure[0]  # this is the first model of the PDB
        s = self.structure[chain]
        io = PDBIO()
        io.set_structure(s)
        io.save( output )


#my_structure = PdbRead("./example/RBD_SARS-CoV-2-hACE2.pdb")
#my_structure.extractChain("A", "chainA.pdb")

#myfoldx.mutate(wt_res='T', mut_res='K', position=20, chain='A')
#myfoldx._jsonParse("./example/batch_mutations.json")
#pdb = mewtate_struct_impact("RBD_SARS-CoV-2-hACE2.pdb", "TA20K", default_dir="./example")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=" Usage: ")
    # add long and short argument
    parser.add_argument("-pdb", help="variant file")
    parser.add_argument("-json", help="Path to seq2chain")
    parser.add_argument("-refine", help="1 if you want to repair a stucture")
    args = parser.parse_args()

    myfoldx = FoldX(args.pdb)
    myfoldx.repair(override=True)
