import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { BASE_URL } from '@/http/api';
import { setError } from '@/app/slice';

export const fetchTitle = createAsyncThunk(
  'title/fetchTitle',
  async ({id}, { getState, requestId, dispatch }) => {
    const { currentRequestId } = getState().title;
    
    // Prevents duplicated fetches due to fast consecutive calls
    if (requestId !== currentRequestId) {
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/title/${id}`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error);
      }

      return data;
    } catch (error) {
      dispatch(setError(error.message));
      
      throw error;
    }
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