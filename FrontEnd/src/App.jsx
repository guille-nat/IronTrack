import React,{useState, useEffect} from 'react';
import LoginRegister from './components/LoginRegister';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import NavBar from './components/NavBar';
import Home from './components/Home';
import Routines from './components/Routines';
import Exercises from './components/Exercises';
import './styles/App.css';

function App() {
  const [isLogin, setIsLogin] = useState(false);
  const [csrfToken, setCsrfToken] = useState('');

  // Obtener el token CSRF al cargar la página
  useEffect(() => {
    const getCsrfToken = async () => {
      const response = await fetch('http://127.0.0.1:8000/api/csrf/', {
        method: 'GET',
        credentials: 'include',  // Asegúrate de que las cookies se envíen
      });
      const data = await response.json();
      setCsrfToken(data.csrfToken); // Guarda el token CSRF en el estado
    };
    getCsrfToken();
  }, []);

  const viewContent = () => {
    if (isLogin) {
      return (
      <BrowserRouter>
        <NavBar/>
        <Routes>
          <Route  path="/" element={<Home/>}/>
          <Route path="/exercise" element={<Exercises/>}/>
          <Route path="/routine" element={<Routines/>}/>
          <Route path="/logout"/> 
        </Routes>
      </BrowserRouter>
      );
    } else {
      return <LoginRegister csrfToken={csrfToken} />;  // Pasa el token CSRF a LoginRegister
    }
  };

  return (
    <>
      <div className='main-content'>{viewContent()}</div>
    </>
  );
}

export default App;
