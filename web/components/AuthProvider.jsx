import api, { setAuthToken } from '../services/api'
import { 
    useState,
    createContext,
    useContext
} from 'react'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(null)

    const login = async (email, password) => {
        const formData = new URLSearchParams()
        formData.append("username", email)
        formData.append("password", password)
        const response = await api.post("/users/login",
            formData,
            {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            }
        )
        const accessToken = response.data.access_token
        
        setToken(accessToken)
        setAuthToken(accessToken)
    }

    const logout = async () => {
        await api.get("/users/logout")
        setToken(null)
        setAuthToken(null)
    }

    const register = async (email, password) => {
        await api.post("/users/register", { email, password })
    }

    const refreshToken = async () => {
        const response = await api.post("/users/refresh")
        setToken(response.data.access_token)
    }

    const getJobs = async () => {
        const jobs = await api.get("/jobs/get")
        return jobs
    }

    const createJob = async (data) => {
        const response = await api.post("/jobs/create")
        return response
    }

    return (
        <AuthContext.Provider value={{ token, login, logout, register, refreshToken, getJobs, createJob }}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => useContext(AuthContext)
