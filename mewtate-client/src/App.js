import React, { useState } from "react";
import SearchInput from "./components/SearchInput";
import { AppBar, Toolbar, Typography } from "@material-ui/core";
import HeroHeader from "./components/HeroHeader";
import VariantReport from "./components/VariantReport";

function App() {
  const [currentSearch, setCurrentSearch] = useState();

  const onSearchInputSubmit = (protein, position, variant) => {
    setCurrentSearch({
      protein: protein,
      position: position,
      variant: variant,
    });
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h5">Mewtate!</Typography>
        </Toolbar>
      </AppBar>
      {!currentSearch && (
        <>
          <HeroHeader />
          <SearchInput onSearchInputSubmit={onSearchInputSubmit} />
        </>
      )}
      {currentSearch && (
        <VariantReport
          protein={currentSearch.protein}
          position={currentSearch.position}
          variant={currentSearch.variant}
        />
      )}
    </>
  );
}

export default App;
