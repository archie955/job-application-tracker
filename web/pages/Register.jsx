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
            navigate("/login")
        } catch (err) {
            setError("Invalid credentials")
        }
    }

    const switchToLogin = () => {
        navigate("/login")
    }

    const changeShowPassword = () => {
        setShowPassword(!showPassword)
    }

    return (
        <div>
        <h2>{error}</h2>
        <LoginForm
            loginFunction={handleSubmit}
            email={email}
            setEmail={setEmail}
            password={password}
            setPassword={setPassword}
            showPassword={showPassword}
            setShowPassword={changeShowPassword}
            action={"Register"}
            />
        <button type="button" onClick={switchToLogin}>Login?</button>
        </div>
    )
}

export default Register