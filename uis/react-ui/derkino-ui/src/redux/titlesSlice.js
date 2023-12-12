import { createSlice } from '@reduxjs/toolkit';

export const titlesSlice = createSlice({
  name: 'titles',
  initialState: [],
  reducers: {
    setTitles: (state, action) => {
      return action.payload;
    },
  },
});

export const { setTitles } = titlesSlice.actions;

export default titlesSlice.reducer;
