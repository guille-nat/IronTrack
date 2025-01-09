import React from "react";
import Form from "../components/Form"

function Login(){
    return <Form root="/api/token/" method="login" />
}
export default Login;