import {HomePage} from './pages/HomePage';
import { Provider } from 'react-redux';
import { store } from './app/store/store';
import './app/styles/styles.scss';

function App() {
  return (
    <Provider store={store}>
      <HomePage />
    </Provider>
  );
}

export default App;
