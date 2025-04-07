import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import "./Signup.css";

const Signup = () => {
  const [role, setRole] = useState(null); // 'doctor' or 'patient'
  const [formData, setFormData] = useState({
    username: "", // 🔹 Changed 'name' to 'username' (matches backend)
    email: "",
    password: "",
    hospital: "", // Only for doctors
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const endpoint = "http://127.0.0.1:8000/register/";

    // Only include hospital if the user is a doctor
    const data = {
      ...formData,
      role: role,
      hospital: role === "doctor" ? formData.hospital : null
    };


    // Log the data to check what is being sent
    console.log("Sending data:", data);

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Registration failed");
      }

      // Reset form after success
      setFormData({ username: "", email: "", password: "", hospital: "" });
      setRole(null);
      navigate("/"); // Redirect user to home page
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      {!role ? (
        <div className="register-options">
          <motion.button
            className="btn-primary"
            whileHover={{ scale: 1.05 }}
            onClick={() => setRole("patient")}
          >
            Register as Patient
          </motion.button>
          <motion.button
            className="btn-outline"
            whileHover={{ scale: 1.05 }}
            onClick={() => setRole("doctor")}
          >
            Register as Doctor
          </motion.button>
        </div>
      ) : (
        <motion.form
          className="register-form"
          onSubmit={handleSubmit}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <h2>Register as {role === "doctor" ? "Doctor" : "Patient"}</h2>

          {error && <p className="error-message">{error}</p>} {/* 🔹 Error display */}

          <input
            type="text"
            name="username" // 🔹 Changed from 'name' to 'username' (backend match)
            placeholder="Full Name"
            value={formData.username}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email Address"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          {role === "doctor" && (
            <input
              type="text"
              name="hospital"
              placeholder="Currently working at"
              value={formData.hospital}
              onChange={handleChange}
              required
            />
          )}
          <motion.button
            type="submit"
            className="btn-primary"
            whileHover={{ scale: 1.05 }}
            disabled={loading} // 🔹 Disable button when loading
          >
            {loading ? "Registering..." : "Register"} {/* 🔹 Show loading state */}
          </motion.button>
          <motion.button
            className="btn-outline"
            whileHover={{ scale: 1.05 }}
            onClick={() => setRole(null)}
            type="button"
          >
            Back
          </motion.button>
        </motion.form>
      )}
    </div>
  );
};

export default Signup;
