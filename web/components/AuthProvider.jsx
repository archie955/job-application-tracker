import api, { setupInterceptors } from '../services/api'
import { 
    useState,
    createContext,
    useContext,
    useEffect
} from 'react'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        setupInterceptors(() => token,
            (newToken) => setToken(newToken)
        )
    }, [])

    useEffect(() => {
        const refresh = async () => {
            try {
                const response = await api.post("/users/refresh")
                setToken(response.data.access_token)
            } catch {
                setToken(null)
            } finally {
                setLoading(false)
            }
        }

        refresh()
    }, [])


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
    }

    const logout = async () => {
        await api.get("/users/logout")
        setToken(null)
    }

    const register = async (email, password) => {
        await api.post("/users/register", { email, password })
    }

    const getJobs = async () => {
        const response = await api.get("/jobs/get")
        return response.data
    }

    const createJob = async (job) => {
        const response = await api.post("/jobs/create", job)
        return response.data
    }

    const deleteJob = async (id) => {
        await api.delete(`/jobs/delete/${id}`)
    }

    const updateJob = async (id, job) => {
        const response = await api.put(`/jobs/update/${id}`, job)
        return response.data
    }

    const createAssessment = async (job_id, newAssessment) => {
        const response = await api.post(`/jobs/create/${job_id}`, newAssessment)
        return response.data
    }

    const updateAssessment = async (job_id, assessment_id, updatedAssessment) => {
        const response = await api.put(`/jobs/update/${job_id}/${assessment_id}`, updatedAssessment)
        return response.data
    }

    const deleteAssessment = async (job_id, assessment_id) => {
        const response = await api.delete(`/jobs/delete/${job_id}/${assessment_id}`)
        return response.data
    }

    if (loading) {
        return null
    }

    return (
        <AuthContext.Provider value={{ token, login, logout, register, getJobs, createJob, updateJob, deleteJob, createAssessment, updateAssessment, deleteAssessment }}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => useContext(AuthContext)
