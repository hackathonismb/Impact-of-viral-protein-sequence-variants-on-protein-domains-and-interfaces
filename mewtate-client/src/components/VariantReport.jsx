import React from "react";
import FunctionalInfo from "./FunctionalInfo";
import { Container, Typography } from "@material-ui/core";
import useApi from "../hooks/UseApi";
import { useParams } from "react-router";

const VariantReport = () => {
  const { protein, position, variant } = useParams();

  const { data } = useApi(
    `https://www.ebi.ac.uk/pdbe/api/mappings/best_structures/${protein}`
  );

  if (!data) {
    return <div>Loading...</div>;
  }

  const pdbId = Object.values(data)[0][0].pdb_id;

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom>
        Information for {protein} variant {variant} at position {position}
      </Typography>
      <FunctionalInfo protein={protein} position={position} />
      <iframe
        title="IcN3D"
        src={`https://www.ncbi.nlm.nih.gov/Structure/icn3d/full.html?pdbid=${pdbId}&width=300&height=300&showcommand=0&mobilemenu=1&showtitle=0`}
        width="320"
        height="320"
      ></iframe>
    </Container>
  );
};

export default VariantReport;
