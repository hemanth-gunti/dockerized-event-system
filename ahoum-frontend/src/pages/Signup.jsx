import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [step, setStep] = useState(1);

  const navigate = useNavigate();

  const signup = async () => {
    try {
      await api.post("signup/", {
        email: email.trim().toLowerCase(),
        password: password,
        role: "seeker"
      });

      alert("OTP sent. Check backend logs.");
      setStep(2);
    } catch (err) {
      console.log(err.response?.data);
      alert(err.response?.data?.detail || "Signup failed");
    }
  };

 const verifyOtp = async () => {
  try {
    await api.post("verify/", {
      email: email.trim().toLowerCase(),
      otp: otp.trim()
    });

    alert("Signup successful! You can now login.");
    navigate("/login");
  } catch (err) {
    console.log("Verify error:", err.response?.data);
    alert(err.response?.data?.detail || "Verification failed");
  }
};


  return (
    <div>
      {step === 1 && (
        <>
          <h2>Signup</h2>
          <input
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
          />
          <br />
          <input
            placeholder="Password"
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
          />
          <br />
          <button onClick={signup}>Signup</button>
        </>
      )}

      {step === 2 && (
        <>
          <h2>Enter OTP</h2>
          <input
            placeholder="Enter OTP"
            value={otp}
            onChange={e => setOtp(e.target.value)}
          />
          <br />
          <button onClick={verifyOtp}>Verify OTP</button>
        </>
      )}
    </div>
  );
}

export default Signup;
