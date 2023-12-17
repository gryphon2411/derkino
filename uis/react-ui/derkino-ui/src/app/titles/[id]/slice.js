import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

export const fetchTitle = createAsyncThunk(
  'title/fetchTitle',
  async ({id}, { getState, requestId }) => {
    const { currentRequestId } = getState().title;
    
    if (requestId !== currentRequestId) {
      // Prevents duplicated fetches due to fast consecutive calls
      return;
    }

    const response = await fetch(`http://192.168.49.2:32062/api/v1/titles/${id}`);
    const data = await response.json();
    return data;
  }
);

const titleSlice = createSlice({
  name: 'title',
  initialState: { 
    status: 'idle', 
    currentRequestId: null,
    error: null,
    title: null
  },
  reducers: { 
    setTitle: (state, action) => {
      state.title = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTitle.pending, (state, action) => {
        if (state.status !== 'loading') {
          state.status = 'loading';
          state.currentRequestId = action.meta.requestId;
        }
      })
      .addCase(fetchTitle.fulfilled, (state, action) => {
        if (state.status === 'loading' && state.currentRequestId === action.meta.requestId) {
          state.status = 'succeeded';
          state.title = action.payload;
          state.currentRequestId = null;
        }
      })
      .addCase(fetchTitle.rejected, (state, action) => {
        if (state.status === 'loading' && state.currentRequestId === action.meta.requestId) {
          state.status = 'failed';
          state.error = action.error.message;
          state.currentRequestId = null;
        }
      });
  },
});

export const { setTitle } = titleSlice.actions;

export default titleSlice.reducer;