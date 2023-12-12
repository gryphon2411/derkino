import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

export const fetchTitles = createAsyncThunk(
  'titles/fetchTitles',
  async ({ page, rowsPerPage }) => {
    const response = await fetch(`http://192.168.49.2:32062/api/v1/titles?page=${page}&size=${rowsPerPage}`);
    const data = await response.json();
    return data;
  }
);

const titlesSlice = createSlice({
  name: 'titles',
  initialState: { 
    status: 'idle', 
    error: null,
    content: [],
    page: 0,
    rowsPerPage: 10,
  },
  reducers: {
    setPage: (state, action) => {
      state.page = action.payload;
    },
    setRowsPerPage: (state, action) => {
      state.rowsPerPage = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTitles.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchTitles.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.content = action.payload.content;
      })
      .addCase(fetchTitles.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  },
});

export const { setPage, setRowsPerPage } = titlesSlice.actions;

export default titlesSlice.reducer;