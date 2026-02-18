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
            action={"Login"}
            />
        <button type="button" onClick={switchToCreate}>Create Account?</button>
        </div>
    )
}

export default Login