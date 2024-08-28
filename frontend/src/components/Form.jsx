import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN, USERNAME } from "../constants"; // Import USERNAME constant
import "../styles/Form.css";
import LoadingIndicator from "./LoadingIndicator";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [email, setEmail] = useState("");
    const [firstName, setFirstName] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        if (method !== "login" && password !== confirmPassword) {
            alert("Passwords do not match.");
            setLoading(false);
            return;
        }

        try {
            const response = await api.post(route, {
                username,
                password,
                ...(method !== "login" && { password_confirmation: confirmPassword, email, first_name: firstName })
            });

            if (method === "login") {
                // Save tokens and username to localStorage
                localStorage.setItem(ACCESS_TOKEN, response.data.access);
                localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
                localStorage.setItem(USERNAME, username); // Save username
                navigate("/");
            } else {
                navigate("/login");
            }
        } catch (error) {
            console.error('Error during request:', error);
            alert(error.response?.data?.detail || "An error occurred.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>{name}</h1>
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
                required
            />
            <input
                className="form-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
            />
            {method !== "login" && (
                <>
                    <input
                        className="form-input"
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Confirm Password"
                        required
                    />
                    <input
                        className="form-input"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        required
                    />
                    <input
                        className="form-input"
                        type="text"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                        placeholder="First Name"
                        required
                    />
                </>
            )}
            {loading && <LoadingIndicator />}
            <button className="form-button" type="submit" disabled={loading}>
                {name}
            </button>
        </form>
    );
}

export default Form;
