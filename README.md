# Mewtate - Impact of viral protein sequence variants on protein domains and interfaces

## Tool to evaluate impact of a mutation
* Come up with a simple SNPs variants mutations structural analysis

* Application to ACE2 polymorphism vs. SARS-CoV-2 binding
  * After the identification of an interaction network between 2 sets of residues (general/flexible case) 2 cases can be considered 
    * A mutation disrupts the network << understand the disruptions using a change of residue side chain corresponding to a mutation (for example P>F) sampling rotamers and corresponding clashes/Hbonds etc formed/broken (with local optimization possible)
    * Use coevolving mutations to evolve an interface given a change from one species to another or  a species polymorphism on one protein, adapting its partner
      * Application between bat/pangolin.civet/human in the couple ACE2/SARS-CoV
### Scope of the study
* To predict the effect of point mutations on 3D protein structure
* To identify hotspot mutation region by clustering mutations
#### Mewtate Workflow
