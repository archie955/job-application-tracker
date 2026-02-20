import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../components/AuthProvider"
import DisplayJobs from "../components/JobDisplay"




const Home = () => {
    const navigate = useNavigate()
    const { logout, getJobs } = useAuth()

    const [jobs, setJobs] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    const handleLogout = async (e) => {
        e.preventDefault()
        try {
            await logout()
            navigate("/login")
        } catch(err) {
            setError("Unable to logout")
        }
    }

    useEffect(() => {
        const fetchData = async () => {
            try {
                const jobsResponse = await getJobs()
                setJobs(jobsResponse)
                console.log(jobsResponse)
                setLoading(false)
            } catch (err) {
                console.log(err)
                setLoading(false)
            }
        }
        fetchData()
    }, [])

    if (loading) {
        return <h1>Loading...</h1>
    }

    return (
        <div>
            <h1>{error}</h1>
            <h2>Jobs table</h2>
            <DisplayJobs jobs={jobs}/>
            <button type="button" onClick={handleLogout}>Logout</button>
        </div>
    )
}

export default Home