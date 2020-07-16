import React from "react";
import { useParams } from "react-router";
import useApi from "../hooks/UseApi";
import { Typography } from "@material-ui/core";

const PredictionInfo = () => {
  const { pdb, chain, position, variant } = useParams();

  const data = {
    pdb: "6VXX",
    mutation: "EA191H",
    foldx: 3.2,
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
        Impact
      </Typography>
      {impact.map((impact) => (
        <p key={impact}>{impact}</p>
      ))}
      <Typography variant="h6" gutterBottom>
        FoldX
      </Typography>
      {foldx}
    </>
  );
};

export default PredictionInfo;
