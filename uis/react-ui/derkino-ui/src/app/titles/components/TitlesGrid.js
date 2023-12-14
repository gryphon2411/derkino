import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Grid, CircularProgress } from '@mui/material';
import { fetchTitles, setPage } from '@/app/titles/slice';


export default function TitlesGrid() {
  const dispatch = useDispatch();
  const titles = useSelector((state) => state.titles.content);
  const page = useSelector((state) => state.titles.page);
  const status = useSelector((state) => state.titles.status);
  

  useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchTitles());
    }
  }, [status, dispatch]);

  useEffect(() => {
    window.addEventListener('scroll', handleInfinitScroll);
    return () => window.removeEventListener('scroll', handleInfinitScroll);
  }, []);

  const handleInfinitScroll = () => {
    if (window.innerHeight + document.documentElement.scrollTop !== document.documentElement.offsetHeight) {
      return; 
    }

    dispatch(setPage(page + 1));
    dispatch(fetchTitles());
  };

  return (
    <div>
      <Grid container spacing={3}>
        {titles.map((title, index) => (
          <Grid item key={title.id} xs={12} sm={6} md={4} lg={4}>
            <div>{title.primaryTitle}</div>
            <div>{title.titleType}</div>
            <div>{title.startYear}</div>
            <div>{title.genres.join(', ')}</div>
          </Grid>
        ))}
      </Grid>
      {status === 'loading' && <CircularProgress />}
    </div>
  );
};
