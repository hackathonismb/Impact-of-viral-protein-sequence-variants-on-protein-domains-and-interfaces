import React from "react";
import FunctionalInfo from "./FunctionalInfo";
import {
  Container,
  Typography,
  Grid,
  Paper,
  makeStyles,
} from "@material-ui/core";
import { useParams } from "react-router";
import PredictionInfo from "./PredictionInfo";
import useApi from "../hooks/UseApi";

const useStyles = makeStyles((theme) => ({
  root: {
    marginTop: "2rem",
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: "left",
    color: theme.palette.text.primary,
  },
  colouredText: {
    color: "red",
  },
}));

const VariantReport = () => {
  const { protein, position, variant, pdb, chain } = useParams();

  const classes = useStyles();
  const { data } = useApi(
    `https://www.ebi.ac.uk/pdbe/api/mappings/best_structures/${protein}`
  );

  if (!data) {
    return null;
  }

  const positions = Object.values(data)[0].find(
    (item) => item.pdb_id === pdb && item.chain_id === chain
  );

  return (
    <Container maxWidth="md" className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper className={classes.paper}>
            <Typography variant="h4" gutterBottom>
              Change <span className={classes.colouredText}>{variant}</span> at
              position {position}{" "}
              <small>
                {pdb}:{chain} ({protein})
              </small>
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper className={classes.paper}>
            <FunctionalInfo positions={positions} />
          </Paper>
        </Grid>
        <Grid item xs={6}>
          <Paper className={classes.paper}>
            <PredictionInfo />
          </Paper>
        </Grid>
        <Grid item xs={6}>
          <Paper className={classes.paper}>
            <Typography variant="h5" gutterBottom>
              Structure
            </Typography>
            <iframe
              title="IcN3D"
              src={`https://www.ncbi.nlm.nih.gov/Structure/icn3d/full.html?pdbid=${pdb}&width=300&height=300&showcommand=0&mobilemenu=1&showtitle=0`}
              width="320"
              height="320"
            ></iframe>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default VariantReport;
