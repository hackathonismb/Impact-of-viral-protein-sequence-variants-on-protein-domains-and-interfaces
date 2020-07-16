import React from "react";
import { useParams } from "react-router";
import useApi from "../hooks/UseApi";
import { Typography, makeStyles } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  foldx: {
    backgroundColor: "#020A96",
    color: "#FFF",
    width: "6rem",
    height: "6rem",
    lineHeight: "6rem",
    fontSize: "1.5rem",
    borderRadius: "6rem",
    textAlign: "center",
  },
}));

const PredictionInfo = () => {
  const { pdb, chain, position, variant } = useParams();

  const classes = useStyles();

  const data = {
    pdb: "6VXX",
    mutation: "EA191H",
    foldx: "+3.2",
    impact: ["Charge switch from negative to positive"],
  };

  // const { data } = useApi(
  //   `http://localhost:5000/${pdb}/N${chain}${position}${variant}`
  // );

  // if (!data) {
  //   return null;
  // }

  const { impact, foldx } = data;

  return (
    <>
      <Typography variant="h5" gutterBottom>
        Prediction
      </Typography>
      <Typography variant="h6" gutterBottom>
        Structural impact
      </Typography>
      {impact.map((impact) => (
        <p key={impact}>{impact}</p>
      ))}
      <Typography variant="h6" gutterBottom>
        Energy change
      </Typography>
      <div className={classes.foldx}>{foldx}</div>
    </>
  );
};

export default PredictionInfo;
