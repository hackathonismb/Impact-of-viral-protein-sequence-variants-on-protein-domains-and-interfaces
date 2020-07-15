![Mewtate logo](https://github.com/hackathonismb/Impact-of-viral-protein-sequence-variants-on-protein-domains-and-interfaces/blob/master/mewtate-client/src/mewtate-logo.svg)
# Mewtate - Impact of viral protein sequence variants on protein domains and interfaces
#### Project Contributors: Houcemeddine Othman, Sachendra Kumar, Sherlyn Jemimah, Philippe Youkharibache, Xavier Watkins 
## Motivation
Tool to evaluate impact of a mutation
* Come up with a simple SNPs variants mutations structural analysis

* Application to ACE2 polymorphism vs. SARS-CoV-2 binding
  * After the identification of an interaction network between 2 sets of residues (general/flexible case) 2 cases can be considered 
    * A mutation disrupts the network << understand the disruptions using a change of residue side chain corresponding to a mutation (for example P>F) sampling rotamers and corresponding clashes/Hbonds etc formed/broken (with local optimization possible)
    * Use coevolving mutations to evolve an interface given a change from one species to another or  a species polymorphism on one protein, adapting its partner
      * Application between bat/pangolin.civet/human in the couple ACE2/SARS-CoV
### What does Mewtate do?

Mewtate is a tool to predict the effect of single amino acid substitution (point mutation) on 3D protein structures. It also allows user to identify mutation hotspot regions by calculating statistically significant cluster of mutations on a 3D protein structure.

### Mewtate Workflow

Mewatate assess structural changes such as disulfide breakage, seconday structure change, and many more structural features upon point mutation in a protein structure. This tools also calculate the change free energy due point mutation and its effect on interaction between protein complexes using FoldX. In addition, user can identify mutation hotspot region by calculating internal distribution of mutations for structurally important region compared with other regions of same proteins using statistical approach. Mewtate allows user to prioritize mutations for experimental validation. 

![data logo](https://github.com/hackathonismb/Impact-of-viral-protein-sequence-variants-on-protein-domains-and-interfaces/blob/master/docs/data.png)
### How to use Mewtate?

![client logo](https://github.com/hackathonismb/Impact-of-viral-protein-sequence-variants-on-protein-domains-and-interfaces/blob/master/docs/client.png)
### Validation
In our preliminary studies, we have used ACE2/SARS-CoV to validate our results. We would extend our study other 3D protein structures. We will add more features to improve the functionality of mewtate.

### References
1. Ittisoponpisan et al. 2019 https://doi.org/10.1016/j.jmb.2019.04.009
2. Miller max acc: Miller et al. 1987 https://doi.org/10.1016/0022-2836(87)90038-6
3. Wilke: Tien et al. 2013 https://doi.org/10.1371/journal.pone.0080635
4. Eduard et al. 2014 https://doi.org/10.1093/bioinformatics/btu499
5. FoldX : http://foldxsuite.crg.eu/
