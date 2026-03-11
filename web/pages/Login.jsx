import { useState } from "react"
import { useNavigate } from "react-router-dom"
import LoginForm from "../components/LoginForm"
import { useAuth } from "../components/AuthProvider"

const Login = () => {
    const { login } = useAuth()
    const navigate = useNavigate()

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [showPassword, setShowPassword] = useState(false)
    const [error, setError] = useState("")

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            await login(email, password)
            navigate("/home")
        } catch (err) {
            setError("Invalid credentials")
        }
    }

    const switchToCreate = () => {
        navigate("/")
    }

    const changeShowPassword = () => {
        setShowPassword(!showPassword)
    }

    return (
        <div className="auth-page">
            <div className="auth-card">
                {error && <div className="error">{error}</div>}

                <LoginForm
                    onSubmit={handleSubmit}
                    email={email}
                    setEmail={setEmail}
                    password={password}
                    setPassword={setPassword}
                    showPassword={showPassword}
                    togglePassword={changeShowPassword}
                    action="Login"
                />

                <p className="auth-switch">
                    Don't have an account?
                    <button onClick={switchToCreate}>
                        Register
                    </button>
                </p>
            </div>
        </div>
    )
}

export default Login