import api from '../services/api'
import { 
    useState,
    createContext,
    useContext
} from 'react'

const AuthContext = createContext()

const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(null)

    const login = async (email, password) => {
        const response = await api.post("/login", { email, password })
        setToken(response.data.access_token)
    }

    const register = async (email, password) => {
        await api.post("/register", { email, password })
    }

    const refreshToken = async () => {
        const response = await api.post("/refresh")
        setToken(response.data.access_token)
    }

    return (
        <AuthContext.Provider value={{ token, login, register, refreshToken }}>
            {children}
        </AuthContext.Provider>
    )
}

const useAuth = () => useContext(AuthContext)

export default { useAuth }