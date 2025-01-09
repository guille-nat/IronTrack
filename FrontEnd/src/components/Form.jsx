import React, { useState, useCallback } from "react";
import { useNavigate,Link } from 'react-router-dom'
import { ACCESS_TOKEN, REFRESH_TOKEN, API_URL } from "../constants";
import LoadingIndicator from "./LoadingIndicator";
import api from "../logic/apiService";

function Form({ root, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [passwordView, setPasswordView] = useState(false);
    const [userdata, setUserdata] = useState({
        email: "",
        first_name: "",
        last_name: "",
        profile: {
            nationality: "",
            birthday: ""
        }
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate()

    const name = method === "login" ? "Login" : "Register";

    const handleInputs = useCallback((e) => {
        const { name, value } = e.target;
        setUserdata((prevState) => {
            if (["nationality", "birthday"].includes(name)) {
                return {
                    ...prevState,
                    profile: {
                        ...prevState.profile,
                        [name]: value
                    }
                };
            } else {
                return {
                    ...prevState,
                    [name]: value
                };
            }
        });
    }, []);

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();
        const dataToSubmit = {
            username,
            password,
            ...userdata
        };
        try {

            if (method === "login") {
                const response = await api.post("/token/", { username, password })
                window.localStorage.setItem(ACCESS_TOKEN, response.data.access);
                window.localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
                navigate('/')
            } else {
                const response = await api.post("/users/", dataToSubmit)
                console.log(response);
                navigate('/login');
            }
        } catch (err) {
            console.log(err);
        } finally {
            setLoading(false);
        }
    };

    const handlePasswordViewDown = useCallback(() => {
        setPasswordView(true);
    }, []);

    const handlePasswordViewUp = useCallback(() => {
        setPasswordView(false);
    }, []);

    const formRegister = () => {
        return (
            <>
                <div className="form-login-register-input-container">
                    <input
                        className="form-login-register-input"
                        type="email"
                        name="email"
                        value={userdata.email}
                        placeholder="Email"
                        onChange={handleInputs}
                    />
                </div>

                <div className="form-login-register-input-container">
                    <input
                        className="form-login-register-input"
                        type="text"
                        name="first_name"
                        value={userdata.first_name}
                        placeholder="First Name"
                        onChange={handleInputs}
                    />
                </div>

                <div className="form-login-register-input-container">
                    <input
                        className="form-login-register-input"
                        type="text"
                        name="last_name"
                        value={userdata.last_name}
                        placeholder="Last Name"
                        onChange={handleInputs}
                    />
                </div>

                <div className="form-login-register-input-container">
                    <input
                        className="form-login-register-input"
                        type="date"
                        name="birthday"
                        value={userdata.profile.birthday}
                        placeholder="Birthday"
                        onChange={handleInputs}
                    />
                </div>

                <div className="form-login-register-input-container">
                    <input
                        className="form-login-register-input"
                        type="text"
                        name="nationality"
                        value={userdata.profile.nationality}
                        placeholder="Nationality"
                        onChange={handleInputs}
                    />
                </div>

            </>
        );
    };

    return (
        <>
            <div className="container-login-register">
                
                    <form className='form-login-register' onSubmit={handleSubmit}>
                        <span className="title-form-login-register">{name}</span>
                        
                        <div className="form-login-register-input-container">
                            <input
                                className="form-login-register-input"
                                type="text"
                                name="username"
                                value={username}
                                placeholder="Username"
                                autoComplete="off"
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>
                        <div className="form-login-register-input-container">
                            <input
                                className="form-login-register-input"
                                id="password-form-login-register"
                                type={`${passwordView === true ? "text" : "password"}`}
                                name="password"
                                value={password}
                                placeholder="Password"
                                autoComplete="off"
                                onChange={(e) => setPassword(e.target.value)}
                            />
                            <button
                                className="button-view-p-form-login-register"
                                type="button"
                                onMouseDown={handlePasswordViewDown}
                                onMouseUp={handlePasswordViewUp}
                            >
                                {passwordView === true ? (
                                    <svg
                                        width="20px"
                                        height="20px"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        xmlns="http://www.w3.org/2000/svg"
                                        stroke="#ffffff"
                                    >
                                        <g id="SVGRepo_bgCarrier" strokeWidth="0" />
                                        <g
                                            id="SVGRepo_tracerCarrier"
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                        />
                                        <g id="SVGRepo_iconCarrier">
                                            <path
                                                d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12"
                                                stroke="#ffffff"
                                                strokeWidth="2"
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                            />
                                            <path
                                                d="M1 12C1 12 5 20 12 20C19 20 23 12 23 12"
                                                stroke="#ffffff"
                                                strokeWidth="2"
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                            />
                                            <circle
                                                cx="12"
                                                cy="12"
                                                r="3"
                                                stroke="#ffffff"
                                                strokeWidth="2"
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                            />
                                        </g>
                                    </svg>
                                ) : (
                                    <svg
                                        width="20px"
                                        height="20px"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        xmlns="http://www.w3.org/2000/svg"
                                        stroke="#ffffff"
                                    >
                                        <g id="SVGRepo_bgCarrier" strokeWidth="0" />
                                        <g
                                            id="SVGRepo_tracerCarrier"
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                        />
                                        <g id="SVGRepo_iconCarrier">
                                            <path
                                                d="M2 2L22 22"
                                                stroke="#ffffff"
                                                strokeWidth="2"
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                            />
                                            <path
                                                d="M6.71277 6.7226C3.66479 8.79527 2 12 2 12C2 12 5.63636 19 12 19C14.0503 19 15.8174 18.2734 17.2711 17.2884M11 5.05822C11.3254 5.02013 11.6588 5 12 5C18.3636 5 22 12 22 12C22 12 21.3082 13.3317 20 14.8335"
                                                stroke="#ffffff"
                                                strokeWidth="2"
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                            />
                                            <path
                                                d="M14 14.2362C13.4692 14.7112 12.7684 15.0001 12 15.0001C10.3431 15.0001 9 13.657 9 12.0001C9 11.1764 9.33193 10.4303 9.86932 9.88818"
                                                stroke="#ffffff"
                                                strokeWidth="2"
                                                strokeLinecap="round"
                                                strokeLinejoin="round"
                                            />
                                        </g>
                                    </svg>
                                )}
                            </button>
                        </div>
                        {name === "Register" ? formRegister() : null}
                        <div className="buttons-form-login-register">
                            <button className="btn-form-login-register" type="submit">{name === "Register" ? "Register" : "Login"}</button>
                            <Link className="link-form-login-register" to={`/${name === "Register" ? "login" : "register"}`}>{name === "Register" ? "Login" : "Register"}</Link>
                        </div>
                        <div className="texture-form-login-register"></div>
                        {/*//todo: hacer button de recuperar contraseña */}
                    </form>
                
            </div>
            

            {loading && <LoadingIndicator />}
        </>
    );
}

export default Form;


