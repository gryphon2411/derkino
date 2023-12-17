import { configureStore } from '@reduxjs/toolkit';
import titlesReducer from '@/app/titles/slice';
import titleReducer from '@/app/titles/[id]/slice'

export const store = configureStore({
  reducer: {
    titles: titlesReducer,
    title: titleReducer
  },
});