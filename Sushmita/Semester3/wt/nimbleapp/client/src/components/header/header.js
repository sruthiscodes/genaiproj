import React from 'react';
import {Link} from 'react-router-dom'
import { useCart } from '../../hooks/useCart';
import classes from './header.module.css';
import { useAuth } from '../../hooks/useAuth';

export default function Header(){
    const { user, logout } = useAuth();

    const { cart } = useCart()
    return (
    <header className={classes.header}>
        <div className={classes.container}>
            <a href="/">
                <img src="./logo.png" alt="logo" className={classes.logo}/>
            </a>
            <nav>
                <ul>
                    { user?(
                            <li className={classes.menu_container}>
                            <Link to="/profile">{user.name}</Link>
                            <div className={classes.menu}>
                                <Link to="/profile">Profile</Link>
                                <a onClick={logout}>Logout</a>
                            </div> 
                        </li>
                        ):(
                            <Link to="/login">Login</Link>
                        )}
                        <li>
                            <Link to="/cart">
                                Cart
                                
                            </Link>
                        </li>
                </ul>
            </nav>
        </div>
    </header>
        )
}