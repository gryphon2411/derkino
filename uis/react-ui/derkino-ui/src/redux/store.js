import { configureStore } from '@reduxjs/toolkit';
import titlesReducer from '@/redux/titlesSlice';

export default configureStore({
  reducer: {
    titles: titlesReducer,
  },
});
