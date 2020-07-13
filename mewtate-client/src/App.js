import React from "react";
import SearchInput from "./components/SearchInput";
import { AppBar, Toolbar, Typography } from "@material-ui/core";
import HeroHeader from "./components/HeroHeader";

function App() {
  const onSearchInputSubmit = (protein, positon, variant) => {
    console.log(protein, positon, variant);
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h5">Mewtate!</Typography>
        </Toolbar>
      </AppBar>
      <HeroHeader />
      <SearchInput onSearchInputSubmit={onSearchInputSubmit} />
    </>
  );
}

export default App;
