import { configureStore } from '@reduxjs/toolkit';
import titlesReducer from '@/app/titles/slice';

export const store = configureStore({
  reducer: {
    titles: titlesReducer,
  },
});