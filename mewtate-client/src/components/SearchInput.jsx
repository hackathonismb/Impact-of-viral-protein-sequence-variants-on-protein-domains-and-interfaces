import React, { useState } from "react";
import TextField from "@material-ui/core/TextField";
import {
  Button,
  makeStyles,
  Container,
  Card,
  CardContent,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
} from "@material-ui/core";
import { useHistory } from "react-router";
import PDBInput from "./PDBInput";
import ProteinsJSON from "../data/proteins.json";

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
      width: "25ch",
    },
  },
  smallTextField: {
    width: "4rem",
  },
}));

const SearchInput = ({ onSearchInputSubmit }) => {
  // P0DTC2
  const [protein, setProtein] = useState("");
  const [position, setPosition] = useState(0);
  const [pdbId, setPdbId] = useState("");
  const [variant, setVariant] = useState("");

  const history = useHistory();

  const onSubmit = (e) => {
    e.preventDefault();
    const pdb = pdbId.split("-");
    history.push(`/${protein}/${pdb[0]}/${pdb[1]}/${position}/${variant}`);
  };

  const classes = useStyles();
  return (
    <Container maxWidth="md">
      <Card variant="outlined">
        <CardContent>
          <form
            noValidate
            autoComplete="off"
            className={classes.root}
            onSubmit={(e) => onSubmit(e)}
          >
            <FormControl>
              <InputLabel>Protein</InputLabel>
              <Select
                value={protein}
                onChange={(e) => setProtein(e.target.value)}
              >
                {ProteinsJSON.map((item) => (
                  <MenuItem value={item.accession} key={item.accession}>
                    {`${item.accession} ${item.proteinName}`}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl>
              <InputLabel>Structure</InputLabel>

              <PDBInput accession={protein} pdbId={pdbId} setPdbId={setPdbId} />
            </FormControl>
            <TextField
              label="Residue"
              type="number"
              value={position}
              className={classes.smallTextField}
              onChange={(e) => setPosition(e.target.value)}
              disabled={!pdbId}
            />
            <TextField
              label="Change"
              value={variant}
              className={classes.smallTextField}
              onChange={(e) => setVariant(e.target.value)}
              inputProps={{ maxLength: 1 }}
              disabled={!pdbId}
            />
            <Button
              type="submit"
              variant="contained"
              disabled={!protein || !pdbId || !variant || !position}
            >
              Mewtate!
            </Button>
          </form>
        </CardContent>
      </Card>
    </Container>
  );
};

export default SearchInput;
