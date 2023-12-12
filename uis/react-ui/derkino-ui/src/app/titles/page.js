'use client';
import * as React from 'react';
import { useDispatch } from 'react-redux';
import { setTitles } from '@/redux/titlesSlice';
import useTitles from '@/hooks/useTitles';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination'
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

export default function TitlesPage() {
  const dispatch = useDispatch();
  const { titles, isLoading, isError, setPage, setSize, size, page } = useTitles();

  React.useEffect(() => {
    if (titles) {
      dispatch(setTitles(titles.content));
    }
  }, [titles, dispatch]);

  if (isLoading) return 'Loading...';
  if (isError) return 'An error has occurred.';

  return (
    <Container>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Typography variant="body1" gutterBottom>
          Titles Page
        </Typography>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Title</TableCell>
                <TableCell align="right">Year</TableCell>
                <TableCell align="right">Runtime (min)</TableCell>
                <TableCell align="right">Genres</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {titles.map((title) => (
                <TableRow
                  key={title.id}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {title.primaryTitle}
                  </TableCell>
                  <TableCell align="right">{title.startYear}</TableCell>
                  <TableCell align="right">{title.runtimeMinutes}</TableCell>
                  <TableCell align="right">{title.genres.join(', ')}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <TablePagination
            component="div"
            count={-1}
            rowsPerPage={size}
            page={page}
            onPageChange={(event, newPage) => setPage(newPage)}
            onRowsPerPageChange={(event) => setSize(parseInt(event.target.value, 10))}
          />
        </TableContainer>
      </Box>
    </Container>
  );
}
