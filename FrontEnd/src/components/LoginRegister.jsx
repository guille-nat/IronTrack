import React,{useState} from 'react';
import { loginUser,getUser } from '../logic/apiService';
// import { useNavigate } from 'react-router-dom';
import '../styles/LoginRegister.css'

function LoginRegister({ csrfToken }) {
    const [loginData, setLoginData] = useState({
        username: "",
        password: ""
    });
    const [errors, setErrors] = useState({});
    const [passwordVisible, setPasswordVisible] = useState(false);
    const [userData, setUserData] = useState({});

    const cleanForm = () => {
        setLoginData({
            username: "",
            password: ""
        });
    };

    const sendLogin = async (e) => {
        e.preventDefault();
        const newError = {};

        try {
            // Pasa el token CSRF a loginUser
            const data = await loginUser(loginData.username, loginData.password, csrfToken);
            if (data.detail === 'Success') {
                cleanForm();
                console.log('ok');
            } else {
                alert("Credenciales incorrectas");
            }
        } catch (err) {
            newError.err = err;
            setErrors(newError);
            console.log("Error en la petición: ", newError);
        }
    };
    
    const getUserProfile = async () =>{
        const newErrors = {}
        try{
            const profileResponse = await getUser();
            if (profileResponse.ok) {
                const profileData = await profileResponse.json();
                setUserData(profileData.results[0]);
                console.log(userData)
            } else {
                newErrors.dataUser = "Ocurrió un error al obtener el perfil del usuario";
                setErrors(newErrors);
            }
        }catch(err){
            newErrors.err = `Ocurrió un error al obtener el usuario ${err}`;
            setErrors(newErrors);
        }
    }

    const renderUserProfile = ()=>{
        if (!userData) return null;  // Asegúrate de que hay datos antes de intentar renderizar
        return (
            <li>
                <br />
                <span>Username: </span>{userData.username}<br />
                <span>Email: </span>{userData.email}<br />
                <span>First Name: </span>{userData.first_name}<br />
                <span>Last Name: </span>{userData.last_name}<br />
            </li>
        );
    }
    const onChangeInput = (e) =>{
        setLoginData({
            ... loginData,
            [e.target.name]:e.target.value
        });

        setErrors({
            ...errors,
            [e.target.name]: ""
        });
    } 


    return(
        <>
        <div className="content-login">
            <h1>Login</h1>
            <form onSubmit={sendLogin}>
                <div className="content-form">
                    <label htmlFor="username">Username</label>
                    <input 
                    type="text" 
                    name="username" id="username"
                    value={loginData.username}
                    required
                    onChange={onChangeInput}/>
                </div>
                <div className="content-form">
                    <label htmlFor="password">Password</label>
                    <input 
                    type={passwordVisible ? "text" : "password"} 
                    id="password" name="password"
                    value={loginData.password}
                    required
                    onChange={onChangeInput}/>

                    <button onClick={ (e)=>{ 
                            e.preventDefault();
                        setPasswordVisible(!passwordVisible);
                        }
                        }>view password</button>
                </div>
                <div className="content-form">
                    <button type="submit">Iniciar Sesión</button>
                </div>

            </form>
            
        </div>
        <div><button onClick={getUserProfile}>Obtener Perfil</button></div>
        <div className="users-info">
                
            <h1>Profile</h1>
            <ul>{userData && renderUserProfile()}</ul>
                
        </div>
        </>
    );
}
export default LoginRegister;