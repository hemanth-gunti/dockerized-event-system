import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Events from "./pages/Events";
import MyEnrollments from "./pages/MyEnrollments";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/events" element={<Events />} />
      <Route path="/me" element={<MyEnrollments />} />
    </Routes>
  );
}

export default App;
