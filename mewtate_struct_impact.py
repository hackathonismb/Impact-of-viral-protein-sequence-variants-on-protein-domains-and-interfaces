from Bio.PDB import *
import requests

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
        dssp_WT  = DSSP( self.pdb_WT, default_dir+pdb+".pdb", dssp="C:/Users/Sherlyn/Downloads/dssp-2.0.4-win32.exe" )
        self.ss_WT, self.rsa_WT = dssp_WT[( self.mutation[1], self.target.get_id() )][2], dssp_WT[( self.mutation[1], self.target.get_id() )][3]

        if mutation[0] != olc[ r.get_resname() ]:
            return "Given mutation does not match structure information" # or False??
            # validation: wt residue to match input mutation

        else:
        
            # To discuss: generate MUTANT pdb using FoldX here or generate it outside this module and give the filename?
            # I'm assuming a MUT file has been generated (e.g. $pdb + "_" + $mutation + ".pdb" )

            s = PDBParser( QUIET=True ).get_structure( pdb, default_dir+pdb+"_"+mutation+".pdb" )

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
            
            ## Generate Text report (for now)
            print( "%s: %s"%(self.pdb,self.mutation) )
            if any( [x!=False for x in output] ):
                print( "Possibly damaging mutation:", end=" ")
                for x in output:
                    if x != False:
                        print( x+";", end=" " )
                

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
