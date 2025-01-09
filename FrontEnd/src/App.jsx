import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";
import Home from "./pages/Home";
import Routines from "./pages/Routines";
import Exercises from "./pages/Exercises";
import NavBar from "./components/NavBar";
import ProtectedRoute from "./components/ProtectedRoute";
import "./styles/App.css";

function Logout() {
  window.localStorage.clear();
  return <Navigate to="/login" replace={true} />;
}

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <NavBar />
                <Home />
              </>
            }
          />
          <Route
            path="/login"
            element={
              <>
                <NavBar />
                <Login />
              </>
            }
          />
          <Route
            path="/logout"
            element={
              <>
                <ProtectedRoute>
                  <NavBar />
                  <Logout />
                </ProtectedRoute>
              </>
            }
          />
          <Route
            path="/register"
            element={
              <>
                <NavBar />
                <Register />
              </>
            }
          />
          <Route
            path="*"
            element={
              <>
                <NavBar />
                <NotFound />
              </>
            }
          ></Route>
          <Route
            path="/routines"
            element={
              <>
                <ProtectedRoute>
                  <NavBar />
                  <Routines />
                </ProtectedRoute>
              </>
            }
          ></Route>
          <Route
            path="/exercises"
            element={
              <>
                <ProtectedRoute>
                  <NavBar />
                  <Exercises />
                </ProtectedRoute>
              </>
            }
          ></Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
