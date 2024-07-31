"use client"
import { usePathname } from 'next/navigation';
import { useSelector, useDispatch } from 'react-redux';
import { useEffect } from 'react';
import { CircularProgress } from '@mui/material';
import { fetchTitle, setTitle, fetchFacts } from '@/app/titles/[id]/slice';

export default function TitlePage() {
  const pathname = usePathname();
  const id = pathname.split('/').pop();

  const dispatch = useDispatch();
  const title = useSelector((state) => state.title.title);
  const titles = useSelector((state) => state.titles.content);
  const facts = useSelector((state) => state.title.facts);

  useEffect(() => {
    if (title && title.id !== id) {
      dispatch(setTitle(null));
    }

    if (!title) {
      const foundTitle = titles.find((title) => title.id === id);
      if (foundTitle) {
        dispatch(setTitle(foundTitle));
      } else {
        dispatch(fetchTitle({ id }));
      }
    }

    if (!facts) {
      dispatch(fetchFacts({ id }));
    }
  }, [dispatch, id, title, titles, facts]);

  if (!title) {
    return <CircularProgress />;
  }

  return (
    <div>
      <h1>{title.primaryTitle}</h1>
      <p>Type: {title.titleType}</p>
      <p>Original Title: {title.originalTitle}</p>
      <p>Is Adult: {title.isAdult ? 'Yes' : 'No'}</p>
      <p>Start Year: {title.startYear}</p>
      <p>End Year: {title.endYear}</p>
      <p>Runtime Minutes: {title.runtimeMinutes}</p>
      <p>Genres: {title.genres.join(', ')}</p>
      <p style={{ whiteSpace: 'pre-wrap' }}>Facts: {facts}</p>
    </div>
  );
}