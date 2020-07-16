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

const FunctionalInfo = () => {
  const { protein, position } = useParams();

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
    (feature) => feature.begin <= position && feature.end >= position
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
              <TableCell>Position</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Description</TableCell>
              <TableCell>Evidence</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredData.map((feature) => (
              <TableRow key={`${feature.begin}${feature.end}${feature.type}`}>
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
