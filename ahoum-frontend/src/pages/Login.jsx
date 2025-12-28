import { useState } from "react";
import api from "../api/api";
import { useNavigate } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const login = async () => {
    try {
      const res = await api.post("login/", {
        email: email,
        password: password
      });

      // 🔥 Store tokens correctly
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);

      navigate("/events");
    } catch (err) {
      console.log("Login error:", err.response?.data);
      alert(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <div style={{ padding: "30px", color: "white" }}>
      <h2>Login</h2>

      <input
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
      /><br/>

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      /><br/>

      <button onClick={login}>Login</button><br/>
      <a href="/signup">Signup</a>
    </div>
  );
}

export default Login;
