import React from 'react';
import { Link } from 'react-router-dom';
function NavBar(){

    return(
    <>
        <nav className="navbar">
            <ul>
                <li>
                    <Link to="/">Home</Link>
                </li>
                <li>
                    <Link to="/exercise">Exercise</Link>
                </li>
                <li>
                    <Link to="/routine">Routine</Link>
                </li>
                <li>
                    <Link to="/logout">Logout</Link>
                </li>
            </ul>
            
        </nav>
    </>
    );
}
export default NavBar