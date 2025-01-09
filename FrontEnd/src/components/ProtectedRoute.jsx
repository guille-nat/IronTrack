import React,{ useState, useEffect }  from "react";
import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants'
import api from "../logic/apiService"
import LoadingIndicator from "./LoadingIndicator";

function ProtectedRoute({ children }) {
    const [isAuthenticated, setIsAuthenticated] = useState(null);

    useEffect(() => {
        auth().catch(() => setIsAuthenticated(false));
    }, []);

    const refreshToken = async () => {
        const refresh = window.localStorage.getItem(REFRESH_TOKEN);
        try {
            const response = await api.post("/token/refresh/", { refresh: refresh, });
            if (response.status === 200) {
                window.localStorage.setItem(ACCESS_TOKEN, response.data.access);
                setIsAuthenticated(true);
            } else {
                window.localStorage.removeItem(ACCESS_TOKEN);
                window.localStorage.removeItem(REFRESH_TOKEN);
                setIsAuthenticated(false);
            }
        } catch (err) {
            console.error(err);
            window.localStorage.removeItem(ACCESS_TOKEN);
            window.localStorage.removeItem(REFRESH_TOKEN);
            setIsAuthenticated(false);
        };
    };

    const auth = async () => {
        const token = window.localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
            return setIsAuthenticated(false);
        }
        const decoded = jwtDecode(token);
        const tokenExpired = decoded.exp;
        const currentTime = Date.now() / 1000;

        if (tokenExpired < currentTime) {
            await refreshToken();
        } else {
            setIsAuthenticated(true);
        }
    };

    if (isAuthenticated === null) {
        return <LoadingIndicator/>;
    }
    return isAuthenticated ? children : <Navigate to="/login" replace={true}/>;
}
export default ProtectedRoute;

