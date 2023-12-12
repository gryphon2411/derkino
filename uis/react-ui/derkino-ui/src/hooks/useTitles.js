import useSWR from 'swr'
import { useState } from 'react';

const fetcher = url => fetch(url).then(res => res.json());

export default function useTitles() {
  const [page, setPage] = useState(0);
  const [size, setSize] = useState(10);

  const { data, error } = useSWR(`http://192.168.49.2:32062/api/v1/titles?page=${page}&size=${size}`, fetcher);

  return {
    titles: data ? data.content : null,
    isLoading: !error && !data,
    isError: error,
    setPage,
    setSize,
    size,
    page
  }
}
