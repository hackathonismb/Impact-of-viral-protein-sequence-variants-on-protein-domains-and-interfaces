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

const useStyles = makeStyles((theme) => ({
  root: {
    marginTop: "2rem",
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: "left",
    color: theme.palette.text.primary,
  },
}));

const VariantReport = () => {
  const { protein, position, variant, pdb, chain } = useParams();

  const classes = useStyles();

  return (
    <Container maxWidth="md" className={classes.root}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper className={classes.paper}>
            <Typography variant="h4" gutterBottom>
              {protein} {pdb} {chain} {position}
              {variant}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper className={classes.paper}>
            <FunctionalInfo />
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
