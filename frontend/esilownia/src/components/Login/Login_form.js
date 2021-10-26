import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import 'bootstrap/dist/css/bootstrap.min.css';
import axiosInstance from '../Axios/axios';
import {useHistory, Link} from "react-router-dom";


function Login_form() {

    const history = useHistory();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
  
    function validateForm() {
      return email.length > 0 && password.length > 0;
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(email);
        console.log(password);

        axiosInstance
            .post(`auth/token/`, {
                grant_type: 'password',
                username: email,
                password: password,
                client_id: 'TUz2wd25Z9hfRbOUr9z3CFEKAc42hJrjsz57sMt6',
                client_secret:
                    'QpMCaevBW6VRJ42wtJ1Cgqitz0aVuBMJRQFgULMTGYievg572RVlcQoTD6xtaVf4mL6K38Df6tcazzfsxMfaDTEjzbH343kFCItJfJKEa2bcjL0ukufLOsfQCAFx3hTR',
            })
            .then((res) => {
                console.log(res)
                console.log(res.data)
                localStorage.setItem('access_token', res.data.access_token);
                localStorage.setItem('refresh_token', res.data.refresh_token);

                console.log("Token acc: " + localStorage.getItem('access_token'))
                console.log("Token ref: " + localStorage.getItem('refresh_token'))


                history.push('/dashboard');
                window.location.reload();
            });
    };

  return (
    <div className="login_form">
      <Form onSubmit={handleSubmit}>
        <Form.Group size="lg" controlId="email">
          <Form.Label>Email</Form.Label>
          <Form.Control
            autoFocus
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Form.Group>
        <Form.Group size="lg" controlId="password">
          <Form.Label>Haslo</Form.Label>
          <Form.Control
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Group>
        <Button onClick={handleSubmit} block size="lg" className="btn btn-lg" id="btn-login" type="submit" disabled={!validateForm()}>
          Zaloguj
        </Button>
        Nie masz konta? <Link to="/register">Zarejestruj się!</Link>
      </Form>
    </div>
  );
}

export default Login_form;