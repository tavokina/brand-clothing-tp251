import { Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './app/store/store';
import './app/styles/styles.scss';

import { HomePage } from './pages/HomePage';
import { AdminLayout } from './components/Layout/AdminLayout';
import { AdminProductFormPage } from './pages/AdminProductFormPage';
import { AdminOrdersPage } from './pages/AdminOrdersPage';
import { AccountLayout } from './components/Layout/AccountLayout';
import { AccountPersonalInformationPage } from './pages/AccountPersonalInformationPage';
import { AccountOrdersPage} from './pages/AccountOrdersPage';
import { AccountFavoritesPage } from './pages/AccountFavoritesPage';
import { CatalogPage } from './pages/CatalogPage';
import { CartPage } from './pages/CartPage';
import { CheckoutPage } from './pages/CheckoutPage';
import { PasswordResetPage } from './pages/PasswordResetPage';
import { PasswordForgotPage } from './pages/PasswordForgotPage';
import { AboutPage } from './pages/AboutPage';
import { OrderConfirmationPage } from './pages/OrderConfirmationPage';
import { ProductDetailsPage } from './pages/ProductDetailsPage';
import { NotFoundPage } from './pages/NotFoundPage';
import { SignInPage } from './pages/SignInPage';
import { SignUpPage } from './pages/SignUpPage';
import { AdminProductsPage } from './pages/AdminProductsPage';


function App() {
  return (
    <Provider store={store}>
      <Routes>
        <Route path='/' element={<HomePage />} />
        <Route path='/catalog' element={<CatalogPage />} />
        <Route path='/product/:id' element={<ProductDetailsPage />} />
        <Route path='/cart' element={<CartPage />} />
        <Route path='/checkout' element={<CheckoutPage />} />
        <Route path='/confirmation' element={<OrderConfirmationPage />} />
        <Route path='/about' element={<AboutPage />} />
        <Route path='/forgotpassword' element={<PasswordForgotPage />} />
        <Route path='/resetpassword' element={<PasswordResetPage />} />
        <Route path='/signin' element={<SignInPage />} />
        <Route path='/signup' element={<SignUpPage />} />

        <Route path="/account" element={<AccountLayout />}>
          <Route index element={<AccountPersonalInformationPage />} />
          <Route path="orders" element={<AccountOrdersPage />} />
          <Route path="favorites" element={<AccountFavoritesPage />} />
        </Route>
    
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<AdminProductsPage />} />
          <Route path="products/new" element={<AdminProductFormPage />} />
          <Route path="products/:id" element={<AdminProductFormPage />} />
          <Route path="orders" element={<AdminOrdersPage />} />
        </Route>

        <Route path='*' element={<NotFoundPage />} />
      </Routes>
    </Provider>
  );
}

export default App;
