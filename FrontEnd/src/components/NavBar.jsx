import React, { useState } from "react";
import { Link } from "react-router-dom";
import { ACCESS_TOKEN } from "../constants";
import "../styles/NavBar.css";

export default function NavBar() {
    const [isOpen, setIsOpen] = useState(false);
    const toggleMenu = () => {
        setIsOpen(!isOpen);
    };
    const isLogin = () => {
        const token = window.localStorage.getItem(ACCESS_TOKEN);
        try {
            if (token) {
                return (
                    <li>
                        <Link to="/logout">Logout</Link>
                    </li>
                );
            } else {
                return (
                    <>
                        <li>
                            <Link to="/login">Login</Link>
                        </li>
                        <li>
                            <Link to="/register">Register</Link>
                        </li>
                    </>
                );
            }
        } catch (err) {
            console.error(err);
        }
    };
    return (
        <>
            <nav>
                <div className="container-navbar">
                    <Link to="/" className="logo-app-navbar">
                        <img src="../../public/IronTrack.ico" alt="Iron Track logo" />
                        Iron Track
                    </Link>
                    <ul className={`nav-links ${isOpen ? "open" : ""}`}>
                        <li>
                            <Link to="/">Home</Link>
                        </li>
                        <li>
                            <Link to="/exercises">Exercises</Link>
                        </li>
                        <li>
                            <Link to="/routines">Routines</Link>
                        </li>
                        {isLogin()}
                    </ul>
                    <div className="hamburger" onClick={toggleMenu}>
                        <span className="bar"></span>
                        <span className="bar"></span>
                        <span className="bar"></span>
                        <span className="bar"></span>
                    </div>
                </div>
            </nav>
        </>
    );
}
