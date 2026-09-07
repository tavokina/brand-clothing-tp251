import {HomePage} from './pages/HomePage';
import { Provider } from 'react-redux';
import { store } from './app/store/store';
import './App.css';

function App() {
  return (
    <Provider store={store}>
      <HomePage />
    </Provider>
  );
}

export default App;
