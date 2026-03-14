import { useState } from "react"
import { useNavigate } from "react-router-dom"
import LoginForm from "../components/LoginForm"
import { useAuth } from "../components/AuthProvider"

const Register = () => {
    const { register } = useAuth()
    const navigate = useNavigate()

    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [showPassword, setShowPassword] = useState(false)
    const [error, setError] = useState("")

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            await register(email, password)
            navigate("")
        } catch (err) {
            setError("Invalid credentials")
        }
    }

    const switchToLogin = () => {
        navigate("")
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
                    action="Register"
                />
                
                <p className="auth-switch">
                    Already have an account?
                    <button onClick={switchToLogin}>
                        Login
                    </button>
                </p>
            </div>
        </div>
    )
}

export default Register