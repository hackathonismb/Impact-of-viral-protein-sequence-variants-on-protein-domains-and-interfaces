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
} from "@material-ui/core";
import { useHistory } from "react-router";

const useStyles = makeStyles((theme) => ({
  root: {
    "& > *": {
      margin: theme.spacing(1),
      width: "25ch",
    },
  },
}));

const SearchInput = ({ onSearchInputSubmit }) => {
  const [protein] = useState("P0DTC2");
  const [position, setPosition] = useState(0);
  const [variant, setVariant] = useState("");

  const history = useHistory();

  const onSubmit = (e) => {
    e.preventDefault();
    history.push(`/${protein}/${position}/${variant}`);
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
            <TextField label="Protein" value={protein} />
            {/* <Select label="Structure">
              <MenuItem value={10}>Ten</MenuItem>
              <MenuItem value={10}>Ten</MenuItem>
              <MenuItem value={10}>Ten</MenuItem>
              <MenuItem value={10}>Ten</MenuItem>
            </Select> */}
            <TextField
              label="Position"
              type="number"
              value={position}
              onChange={(e) => setPosition(e.target.value)}
            />
            <TextField
              label="Variant"
              value={variant}
              onChange={(e) => setVariant(e.target.value)}
            />
            <Button type="submit" variant="contained">
              Mewtate!
            </Button>
          </form>
        </CardContent>
      </Card>
    </Container>
  );
};

export default SearchInput;
