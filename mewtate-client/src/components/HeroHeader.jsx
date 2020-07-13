import React from "react";
import { Container, Typography, makeStyles } from "@material-ui/core";

import logo from "../cat-lion.jpeg";

const useStyles = makeStyles((theme) => ({
  heroContainer: {
    display: "flex",
    marginTop: "5rem",
    marginBottom: "5rem",
    "& img": {
      marginRight: "1rem",
    },
  },
}));

const HeroHeader = () => {
  const classes = useStyles();
  return (
    <Container maxWidth="md" className={classes.heroContainer}>
      <img src={logo} alt="logo" />
      <div>
        <Typography variant="h2" gutterBottom>
          Mewtate
        </Typography>
        <Typography variant="body1" gutterBottom>
          A variant effect predictor for SARS-CoV-2
        </Typography>
      </div>
    </Container>
  );
};

export default HeroHeader;
