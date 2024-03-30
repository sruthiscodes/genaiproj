import React from 'react';
import { Routes, Route } from 'react-router-dom';
import AuthRoute from './components/AuthRoute/AuthRoute';
import CartPage from './pages/Cart/CartPage';
import CheckoutPage from './pages/Checkout/CheckoutPage';
import FoodPage from './pages/foodpage/FoodPage';
import HomePage from './pages/home/homepage';
import LoginPage from './pages/Login/LoginPage';
import ProfilePage from './pages/Profile/ProfilePage';
import RegisterPage from './pages/Register/RegisterPage';

export default function AppRoutes(){
    return(
            <Routes>
                <Route path="/" element={<HomePage/>}/>
                <Route path="/search/:searchTerm" element={<HomePage/>}/>
                <Route path="/tag/:tag" element={<HomePage/>}/>
                <Route path="/food/:id" element={<FoodPage/>}/>
                <Route path="/cart" element={<CartPage/>}/>
                <Route path="/login" element={<LoginPage/>}/>
                <Route path="/register" element={<RegisterPage/>}/>
                <Route path="/checkout" element={<AuthRoute>
                    <CheckoutPage/>
                </AuthRoute>}/>
                <Route path="/profile" element={<AuthRoute>
                    <ProfilePage/>
                </AuthRoute>}/>
            </Routes>
    );
}