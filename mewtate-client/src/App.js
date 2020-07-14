import React from "react";
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";
import { AppBar, Toolbar, Typography, makeStyles } from "@material-ui/core";

import SearchInput from "./components/SearchInput";
import HeroHeader from "./components/HeroHeader";
import VariantReport from "./components/VariantReport";

import Logo from "./mewtate-logo.svg";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  logo: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

function App() {
  const classes = useStyles();

  return (
    <Router>
      <AppBar position="static" className={classes.root}>
        <Toolbar>
          <Link to="/">
            <img src={Logo} alt="logo" height="32" className={classes.logo} />
          </Link>
          <Typography variant="h5" className={classes.title}>
            MEWTATE
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
