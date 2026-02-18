import api from '../services/api'
import { 
    useState,
    createContext,
    useContext
} from 'react'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(null)

    const login = async (email, password) => {
        const response = await api.post("/users/login", { email, password })
        setToken(response.data.access_token)
    }

    const register = async (email, password) => {
        await api.post("/users/register", { email, password })
    }

    const refreshToken = async () => {
        const response = await api.post("/users/refresh")
        setToken(response.data.access_token)
    }

    return (
        <AuthContext.Provider value={{ token, login, register, refreshToken }}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => useContext(AuthContext)
