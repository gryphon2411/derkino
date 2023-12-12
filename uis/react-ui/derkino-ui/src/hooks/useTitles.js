import useSWR from 'swr'

const fetcher = url => fetch(url).then(res => res.json());

export default function useTitles() {
  const { data, error } = useSWR('http://192.168.49.2:32062/api/v1/titles?page=0&size=2', fetcher);

  return {
    titles: data ? data.content : null,
    isLoading: !error && !data,
    isError: error
  }
}
