import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

export const fetchTitles = createAsyncThunk(
  'titles/fetchTitles',
  async (_, { getState, requestId }) => {
    const { currentRequestId, page, rowsPerPage } = getState().titles;
    
    if (requestId !== currentRequestId) {
      // Prevents duplicated fetches due to fast consecutive calls
      return;
    }

    const response = await fetch(`http://192.168.49.2:32062/api/v1/titles?page=${page}&size=${rowsPerPage}`);
    const data = await response.json();
    return data;
  }
);

const titlesSlice = createSlice({
  name: 'titles',
  initialState: { 
    status: 'idle', 
    currentRequestId: null,
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
      state.content = [];
      state.page = 0;
      state.rowsPerPage = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTitles.pending, (state, action) => {
        if (state.status !== 'loading') {
          state.status = 'loading';
          state.currentRequestId = action.meta.requestId;
        }
      })
      .addCase(fetchTitles.fulfilled, (state, action) => {
        if (state.status === 'loading' && state.currentRequestId === action.meta.requestId) {
          state.status = 'succeeded';
          state.content = [...state.content, ...action.payload.content];
          state.currentRequestId = null;
        }
      })
      .addCase(fetchTitles.rejected, (state, action) => {
        if (state.status === 'loading' && state.currentRequestId === action.meta.requestId) {
          state.status = 'failed';
          state.error = action.error.message;
          state.currentRequestId = null;
        }
      });
  },
});

export const { setPage, setRowsPerPage } = titlesSlice.actions;

export default titlesSlice.reducer;