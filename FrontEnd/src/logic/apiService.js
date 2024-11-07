export const loginUser = async (username, password, csrfToken) => {
    const response = await fetch('http://127.0.0.1:8000/login/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,  // Agrega el token CSRF en las cabeceras
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include',  // Asegúrate de incluir las cookies
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Authentication failed!");
    }

    return response.json(); // Devuelve la respuesta del backend (datos del token, etc.)
};


export const getUser = async () => {
    const userResponse = await fetch('http://127.0.0.1:8000/api/users/', {
        method:'GET',
                headers:{
                    'Content-Type':'application/json',
        },
        credentials: 'include',
    });
    return userResponse;
};

