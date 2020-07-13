import React from "react";
import FunctionalInfo from "./FunctionalInfo";
import { Container, Typography } from "@material-ui/core";

const VariantReport = (props) => {
  const { protein, position, variant } = props;
  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom>
        Information for {protein} variant {variant} at position {position}
      </Typography>
      <FunctionalInfo {...props} />
    </Container>
  );
};

export default VariantReport;
