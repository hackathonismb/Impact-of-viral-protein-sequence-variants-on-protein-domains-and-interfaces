from Bio.PDB import *
import requests
import os
from shutil import which 
from sys import exit
import glob
import json
import warnings

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

        s = PDBParser( QUIET=True ).get_structure( "thestructure", pdb)
        self.pdb = pdb
        self.default_dir = default_dir
        
        self.pdb_WT = s[0] # WT model (from SMCRA)
        c = self.pdb_WT[ mutation[1] ]
        r = c[ int( mutation[2:-1] ) ]
        
        self.target   = r
        self.mutation = mutation
        dssp_WT  = DSSP( self.pdb_WT, pdb, dssp="/home/houcemeddine/modules/dssp/bin/dssp-2.0.4-linux-i386" )

        self.ss_WT, self.rsa_WT = dssp_WT[( self.mutation[1], self.target.get_id() )][2], dssp_WT[( self.mutation[1], self.target.get_id() )][3]


        if mutation[0] != olc[ r.get_resname() ]:
            return "Given mutation does not match structure information" # or False??
            # validation: wt residue to match input mutation

        else:
            # To discuss: generate MUTANT pdb using FoldX here or generate it outside this module and give the filename?
            # I'm assuming a MUT file has been generated (e.g. $pdb + "_" + $mutation + ".pdb" )

            path_to_mut_structure = os.path.dirname(os.path.abspath(pdb))+'/'+os.path.basename(pdb).replace('.pdb','_Repair_1.pdb')

            s = PDBParser( QUIET=True ).get_structure( "mutant", path_to_mut_structure )
        
            self.pdb_MUT = s[0] # MUT model
            c = self.pdb_MUT[ mutation[1] ]
            r = c[ int( mutation[2:-1] ) ]

            self.mutres = r
            dssp_MUT  = DSSP( self.pdb_MUT, path_to_mut_structure, dssp="/home/houcemeddine/modules/dssp/bin/dssp-2.0.4-linux-i386" )
            self.ss_MUT, self.rsa_MUT = dssp_MUT[( self.mutation[1], self.mutres.get_id() )][2], dssp_MUT[( self.mutation[1], self.mutres.get_id() )][3]

            ## Steps to assess structural impact to be finalized here

            output = { "disulfide_breakage":mewtate_struct_impact.disulfide_breakage( self ),
                       "buried_Pro_introduced": mewtate_struct_impact.buried_Pro_introduced( self ),
                       "buried_glycine_replaced": mewtate_struct_impact.buried_glycine_replaced( self ),
                       "buried_hydrophilic_introduced": mewtate_struct_impact.buried_hydrophilic_introduced( self ),
                       "buried_charge_introduced": mewtate_struct_impact.buried_charge_introduced( self ),
                       "buried_charge_switch": mewtate_struct_impact.buried_charge_switch( self ),
                       "sec_struct_change": mewtate_struct_impact.sec_struct_change( self ),
                       "buried_charge_replaced": mewtate_struct_impact.buried_charge_replaced( self ),
                       "buried_exposed_switch": mewtate_struct_impact.buried_exposed_switch( self ),
                       "gly_bend": mewtate_struct_impact.gly_bend( self ),
                       "buried_hydrophilic_introduced": mewtate_struct_impact.buried_hydrophilic_introduced( self ) }
            
            ## Generate Text report (for now)
            print( "%s: %s"%(self.pdb,self.mutation) )
            if any( [x!=False for x in output.values()] ):
                print( "Possibly damaging mutation:", end=" ")
                output["decision"] = "Possibly damaging mutation"
                for x in output.values():
                    if x != False:
                        print( x+";", end=" " )
        self.output = output 

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
    def __init__(self, pdb, wt_res, mut_res, position, chain, mode = "single" ):
        if os.path.exists(pdb) : 
            self.pdb = pdb
            self.container_folder = os.path.dirname(os.path.abspath(self.pdb))
            self.basename = os.path.basename(self.pdb)
            self.wt_res = wt_res
            self.mut_res = mut_res
            self.position = position
            self.chain = chain
            self.mode = mode

        else: 
            raise FileNotFoundError("File does not exist")
        repaired_pdb = os.path.splitext(self.basename)[0]+"_Repair.pdb"

        # check  if the repaired structure exists in the working folder 
        if os.path.exists(self.container_folder+"/"+repaired_pdb) : 
            self.path_to_repaired_wt_structure = self.container_folder+"/"+repaired_pdb
            print("Repaired structure in {}".format(self.path_to_repaired_wt_structure))
            self.repaired_pdb = repaired_pdb
        else:
            self.repair()
            self.path_to_repaired_wt_structure = self.container_folder+"/"+repaired_pdb
            self.repaired_pdb = repaired_pdb

        # mutating and calculating dG        
        self.mutate()
        self.folding_energy = self.parseOutput()
        print("Folding energy:      {} kcal/mol".format(self.folding_energy))
        
        # binding enery 
        self.mut_structure = os.path.basename(pdb).replace('.pdb','_Repair_1.pdb')
        be = self.bindingEnergy()
        if be!= False: 
            binding_energy = self.parseOutput(mode='binding')
            self.wt_binding_energy = binding_energy[0]
            self.mut_binding_energy = binding_energy[1]
            print("Binding energy mutant WT:      {} kcal/mol".format(self.wt_binding_energy ))
            print("Binding energy mutant mut:      {} kcal/mol".format(self.mut_binding_energy ))
        elif be!= False:
            self.wt_binding_energy = "Not applicable"
            self.mut_binding_energy = "Not applicable"

    
    def repair(self): 
        """
        Repair a pdb structure
        """     
        if which("foldx") == None:
            exit("'foldx' not in PATH")
        # run foldx o repair the structure. For some reason foldx does not recognise a path to dir
        cmd="cd {0} ; foldx --command=RepairPDB --pdb={1}".format(self.container_folder, self.basename)
        os.system(cmd)

    
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


    def mutate(self):
        """
        mutate structre 
        """        
        if self.mode == 'single':
            # write the mutation individual file used by foldX
            expression_mut = self.wt_res+self.chain+str(self.position)+self.mut_res+';\n'
            with open(self.container_folder+"/"+"individual_list.txt", 'w') as mutant_file : 
                mutant_file.write(expression_mut)
     
            cmd_mut = "cd {0}; foldx --command=BuildModel --pdb={1} --mutant-file=individual_list.txt >/dev/null".format(self.container_folder, self.repaired_pdb)
            # run the calculation of the folding energy
            os.system(cmd_mut)
        if self.mode == 'batch':
            pass

    def bindingEnergy(self): 
        parser = PDBParser( QUIET=True )
        structure = parser.get_structure('S',self.pdb )
        if len(structure) >1: 
            raise warnings.warn("Multiple models in PDB, will use only the first")
        structure = structure[0]  # this is the first model of the PDB
        if len(structure) >1 : # pdb file contains more than one chain 
            cmd_binding_wt = "cd {0}; foldx --command=AnalyseComplex --pdb={1} --analyseComplexChains={2} >/dev/null".format(self.container_folder, self.repaired_pdb, self.chain)
            os.system(cmd_binding_wt)
            cmd_binding_mut = "cd {0}; foldx --command=AnalyseComplex --pdb={1} --analyseComplexChains={2} >/dev/null".format(self.container_folder, self.mut_structure, self.chain)
            os.system(cmd_binding_mut)
        else: 
            return False


    def parseOutput(self, mode="folding"): 
        """
        Parses foldx diff file and extract dG
        """
        # binding energy corresponds to index 1 (field 2)
        if mode == "folding":
            foldx_dif_file = "Dif_"+self.basename.replace(".pdb", "")+"_Repair.fxout"
            field_index = 1
            with open(self.container_folder+"/"+foldx_dif_file, 'r') as file: 
                lines = file.readlines()
            data = lines[-1].split()
            total_energy = float(data[field_index])
            return  total_energy
        # binding energy corresponds to index 5 (field 6)
        elif mode == "binding": 
            foldx_dif_file = "Interaction_"+self.basename.replace(".pdb", "")+"_Repair_AC.fxout"
            foldx_dif_file_mut = "Interaction_"+self.basename.replace(".pdb", "")+"_Repair_1_AC.fxout"
            field_index = 5
            if os.path.exists(self.container_folder+"/"+foldx_dif_file_mut) : 
                with open(self.container_folder+"/"+foldx_dif_file_mut, 'r') as mut_files: 
                    lines_mut = mut_files.readlines()
                data_mut = lines_mut[-1].split()

                with open(self.container_folder+"/"+foldx_dif_file, 'r') as file: 
                    lines = file.readlines()
                data = lines[-1].split()
                binding_energy_wt = float(data[field_index])                
                binding_energy_mut = float(data_mut[field_index])
                binding_energy_wt = float(data[field_index])
                print( binding_energy_wt, binding_energy_mut )
                return binding_energy_wt, binding_energy_mut

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


def joinMutations(wt_res, mut_res, position, chain):
    return wt_res+chain+position+mut_res


if __name__ == "__main__":
    par_list = ["Y", "K", "505", "B"]   # this would be the input, because it's not possible to  parse the for "YB505K" correctly
    myfoldx = FoldX("./example/RBD_SARS-CoV-2-hACE2.pdb", par_list[0], par_list[1], par_list[2], par_list[3])
    mutation =  joinMutations( par_list[0], par_list[1], par_list[2], par_list[3] ) 
    mymutation = mewtate_struct_impact("./example/RBD_SARS-CoV-2-hACE2.pdb" , mutation, default_dir="./example/")
    output = mymutation.output
    output["dG_folding"] = myfoldx.folding_energy
    output["dG_binding_wt"] = myfoldx.wt_binding_energy
    output["dG_binding_mut"] = myfoldx.mut_binding_energy
    with open('All_outputs.json', 'w') as fp:
        json.dump(output, fp)




