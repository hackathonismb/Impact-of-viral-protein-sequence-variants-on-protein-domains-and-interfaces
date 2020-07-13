import React from "react";
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";
import { AppBar, Toolbar, Typography, makeStyles } from "@material-ui/core";

import SearchInput from "./components/SearchInput";
import HeroHeader from "./components/HeroHeader";
import VariantReport from "./components/VariantReport";

const useStyles = makeStyles((theme) => ({
  navBar: {
    "& a": {
      color: "#FFF",
      textDecoration: "none",
    },
  },
}));

function App() {
  const classes = useStyles();

  return (
    <Router>
      <AppBar position="static" className={classes.navBar}>
        <Toolbar>
          <Typography variant="h5">
            <Link to="/">Mewtate!</Link>
          </Typography>
        </Toolbar>
      </AppBar>
      <Switch>
        <Route path="/" exact>
          <>
            <HeroHeader />
            <SearchInput />
          </>
        </Route>
        <Route path="/:protein/:position/:variant">
          <VariantReport />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
