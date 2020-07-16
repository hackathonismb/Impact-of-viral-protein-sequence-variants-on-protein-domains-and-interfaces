import React from "react";
import { Select, MenuItem } from "@material-ui/core";
import { v1 } from "uuid";
import useApi from "../hooks/UseApi";

const PDBInput = ({ accession, pdbId, setPdbId }) => {
  const { data } = useApi(
    `https://www.ebi.ac.uk/pdbe/api/mappings/best_structures/${accession}`
  );

  if (!data) {
    return <Select value={pdbId} disabled />;
  }

  const handleSelect = (e) => {
    const value = e.target.value;
    setPdbId(e.target.value);
  };

  console.log(data);

  return (
    <Select value={pdbId} onChange={(e) => handleSelect(e)}>
      {Object.values(data)[0].map((item) => (
        <MenuItem value={`${item.pdb_id}-${item.chain_id}`} key={v1()}>
          {`${item.pdb_id} Chain:${item.chain_id} (${item.unp_start}-${item.unp_end})`}
        </MenuItem>
      ))}
    </Select>
  );
};

export default PDBInput;
