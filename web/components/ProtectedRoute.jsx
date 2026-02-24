import { Navigate } from "react-router-dom"
import { useAuth } from "./AuthProvider"

const ProtectedRoute = ({ children }) => {
    const { token } = useAuth()
    if (!token) return <Navigate to="/login" />
    return children
}

export default ProtectedRoute