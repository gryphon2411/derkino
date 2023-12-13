'use client'
import * as React from 'react';
import { useTitles } from './hooks';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead'
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';

export default function TitlesPage() {
  const {
    titles,
    titlesStatus,
    titlesError,
    page,
    rowsPerPage,
    handleChangePage,
    handleChangeRowsPerPage,
  } = useTitles();

  if (titlesStatus === 'loading') {
    return <div>Loading...</div>;
  } else if (titlesStatus === 'failed') {
    return <div>Error: {titlesError}</div>;
  }

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader aria-label="sticky table">
        <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Start Year</TableCell>
              <TableCell>Genres</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {titles.map((row) => (
              <TableRow key={row.id}>
                <TableCell component="th" scope="row">{row.primaryTitle}</TableCell>
                <TableCell>{row.titleType}</TableCell>
                <TableCell>{row.startYear}</TableCell>
                <TableCell>{row.genres.join(', ')}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        count={-1}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
}
