import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import "./Navbar.css";

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  // Function to handle logout
  const fetchCSRFToken = async () => {
    await fetch("https://703b-115-245-68-163.ngrok-free.app/csrf/", {
      method: "GET",
      credentials: "include",
    });
  };

  const handleLogout = async () => {
    try {
      await fetchCSRFToken(); // ✅ Ensure CSRF token is fetched

      const csrfToken = getCookie("csrftoken");
      console.log("CSRF Token:", csrfToken); // Debugging

      const response = await fetch("https://703b-115-245-68-163.ngrok-free.app/logout/", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
      });

      if (response.ok) {
        localStorage.removeItem("user");
        localStorage.removeItem("token");
        setUser(null);
        navigate("/login");
        window.location.reload();
      } else {
        console.error("Logout failed:", await response.text());
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };



  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  return (
    <motion.header
      className="navbar"
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      <div className="container">
        {/* Logo */}
        <Link to="/" className="logo">
          <motion.span
            className="logo-icon"
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            C
          </motion.span>
          <motion.span
            className="logo-text"
            initial={{ x: -50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            CURA
          </motion.span>
        </Link>

        {/* Desktop Navigation */}
        <nav className={`nav-links ${isMenuOpen ? "nav-open" : ""}`}>
          {["Home", "Providers", "AI Consultation", "Appointments"].map(
            (item, index) => (
              <motion.div
                key={index}
                whileHover={{ scale: 1.1, color: "#50BFA5" }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <Link
                  to={`/${item.toLowerCase().replace(/\s+/g, "-")}`}
                  className="nav-item"
                >
                  {item}
                </Link>
              </motion.div>
            )
          )}
        </nav>

        {/* Auth Buttons */}
        <div className="auth-buttons">
          {user ? (
            <>
              <motion.div className="welcome-msg">Welcome, {user.name}</motion.div>
              <motion.button
                onClick={handleLogout}
                className="btn-logout"
                whileHover={{ scale: 1.1 }}
              >
                Logout
              </motion.button>
            </>
          ) : (
            <>
              <motion.div whileHover={{ scale: 1.05 }}>
                <Link to="/login" className="btn-outline">
                  Log in
                </Link>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }}>
                <Link to="/signup" className="btn-primary">
                  Sign up
                </Link>
              </motion.div>
            </>
          )}
        </div>

        {/* Mobile Menu Toggle Button */}
        <button className="menu-toggle" onClick={toggleMenu} aria-label="Toggle menu">
          {isMenuOpen ? "✖" : "☰"}
        </button>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            className="mobile-menu"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <div className="mobile-nav">
              {["Home", "Providers", "AI Consultation", "Appointments"].map(
                (item, index) => (
                  <Link
                    key={index}
                    to={`/${item.toLowerCase().replace(/\s+/g, "-")}`}
                    className="mobile-nav-item"
                    onClick={toggleMenu}
                  >
                    {item}
                  </Link>
                )
              )}
              {user ? (
                <button onClick={handleLogout} className="btn-primary mobile-btn">
                  Logout
                </button>
              ) : (
                <>
                  <Link to="/login" className="btn-outline mobile-btn" onClick={toggleMenu}>
                    Log in
                  </Link>
                  <Link to="/signup" className="btn-primary mobile-btn" onClick={toggleMenu}>
                    Sign up
                  </Link>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.header>
  );
};

export default Navbar;
