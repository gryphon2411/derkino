'use client'
import * as React from 'react';
import { useEffect, useState } from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead'
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';

export default function TitlesPage() {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [data, setData] = useState({ content: [], totalElements: 0 });

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  useEffect(() => {
    fetch(`http://192.168.49.2:32062/api/v1/titles?page=${page}&size=${rowsPerPage}`)
      .then(response => response.json())
      .then(data => setData(data));
  }, [page, rowsPerPage]);

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader aria-label="sticky table">
        <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Year</TableCell>
              <TableCell>Runtime (min)</TableCell>
              <TableCell>Genres</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.content.map((row) => (
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
