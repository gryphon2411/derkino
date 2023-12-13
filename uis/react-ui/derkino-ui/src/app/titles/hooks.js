import { useEffect } from "react";
import { batch, useDispatch, useSelector } from "react-redux";
import { fetchTitles, setPage, setRowsPerPage } from "./slice";

export function useTitles() {
  const dispatch = useDispatch();
  const titles = useSelector((state) => state.titles.content);
  const titlesStatus = useSelector((state) => state.titles.status);
  const titlesError = useSelector((state) => state.titles.error);
  const page = useSelector((state) => state.titles.page);
  const rowsPerPage = useSelector((state) => state.titles.rowsPerPage);

  const handleChangePage = (event, newPage) => {
    dispatch(setPage(newPage));
    dispatch(fetchTitles({ page: newPage, rowsPerPage }));
  };

  const handleChangeRowsPerPage = (event) => {
    const newRowsPerPage = parseInt(event.target.value, 10);
    const newPage = 0;
    dispatch(setRowsPerPage(newRowsPerPage));
    dispatch(setPage(newPage));
    dispatch(fetchTitles({ page: newPage, rowsPerPage: newRowsPerPage }));
  };

  useEffect(() => {
    if (titlesStatus === 'idle') {
      dispatch(fetchTitles({ page, rowsPerPage }));
    }
  }, [dispatch, page, rowsPerPage, titlesStatus]);

  return {
    titles,
    titlesStatus,
    titlesError,
    page,
    rowsPerPage,
    handleChangePage,
    handleChangeRowsPerPage,
  };
}