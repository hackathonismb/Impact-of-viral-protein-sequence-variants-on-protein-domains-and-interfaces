import React from "react";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import useApi from "../hooks/UseApi";
import { useParams } from "react-router";
import { Typography } from "@material-ui/core";

const FunctionalInfo = (positions) => {
  const { protein, chain, position } = useParams();

  const getUniProtPosition = (pos) => pos + positions.positions.unp_start - 1;
  const getPDBPosition = (pos) => pos - positions.positions.unp_start + 1;

  const { data, isLoading, isError } = useApi(
    `https://www.ebi.ac.uk/proteins/api/features/${protein}?format=json`
  );

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isError) {
    return <div>Error</div>;
  }

  const filteredData = data.features.filter(
    (feature) =>
      feature.begin <= getUniProtPosition(position) &&
      feature.end >= getUniProtPosition(position)
  );

  return (
    <>
      <Typography variant="h5" gutterBottom>
        Function
      </Typography>
      <TableContainer component={Paper}>
        <Table size="small" stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell>Chain {chain} positions</TableCell>
              <TableCell>Sequence position</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Evidence</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredData.map((feature) => (
              <TableRow key={`${feature.begin}${feature.end}${feature.type}`}>
                <TableCell>
                  {getPDBPosition(feature.begin)}-{getPDBPosition(feature.end)}
                </TableCell>
                <TableCell>
                  {feature.begin}-{feature.end}
                </TableCell>
                <TableCell>{feature.type}</TableCell>
                <TableCell>{feature.description}</TableCell>
                <TableCell>
                  {feature.evidences &&
                    feature.evidences.map(
                      (evidence) =>
                        evidence.source && (
                          <a
                            href={evidence.source.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            key={evidence.source.url}
                          >
                            {evidence.source.name}
                          </a>
                        )
                    )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
};

export default FunctionalInfo;
