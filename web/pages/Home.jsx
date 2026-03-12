import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../components/AuthProvider"
import DisplayJobs from "../components/JobDisplay"
import ApplicationStatus from "../services/enum"
import JobForm from "../components/AddJobForm"




const Home = () => {
    const navigate = useNavigate()
    const { logout, getJobs, createJob, updateJob, deleteJob } = useAuth()

    const [jobs, setJobs] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    const [title, setTitle] = useState("")
    const [employer, setEmployer] = useState("")
    const [status, setStatus] = useState(ApplicationStatus.Not_Applied)
    const [description, setDescription] = useState("")
    const [location, setLocation] = useState("")

    const [editingJobId, setEditingJobId] = useState(null)


    const handleLogout = async (e) => {
        e.preventDefault()
        try {
            await logout()
            navigate("/login")
        } catch(err) {
            setError("Unable to logout")
        }
    }

    const resetForm = () => {
        setTitle("")
        setEmployer("")
        setStatus(ApplicationStatus.Not_Applied)
        setDescription("")
        setLocation("")
        setEditingJobId(null)
    }

    const handleCreateJob = async (newJob) => {
        const job = await createJob(newJob)
        setJobs(prev => [...prev, job])
        resetForm()
    }

    const handleUpdateJob = async (updatedJob) => {
        if (editingJobId === null) return
        const updated = await updateJob(editingJobId, updatedJob)
        setJobs((prev) => prev.map(job => job.id === editingJobId ? updated : job))
        resetForm()
    }

    const handleEditJob = (job) => {
        setTitle(job.title)
        setEmployer(job.employer)
        setStatus(job.status)
        setDescription(job.description)
        setLocation(job.location)
        setEditingJobId(job.id)
    }

    const handleDeleteJob = async (jobToDelete) => {
        await deleteJob(jobToDelete.id)
        setJobs((prev) => prev.filter(job => job.id !== jobToDelete.id))
        resetForm()
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
    }, [getJobs])

    if (loading) {
        return <h1>Loading...</h1>
    }

    return (
        <div className="home-container">
            <header className="home-header">
                <h1>Job Tracker</h1>

                <button
                    className="secondary-btn"
                    onClick={handleLogout}
                >
                    Logout
                </button>
            </header>

            {error && <div className="error">{error}</div>}

            <div className="home-grid">
                <div className="jobs-section">
                    <h2>Your Applications</h2>

                    <DisplayJobs
                        jobs={jobs}
                        handleEditJob={handleEditJob}
                        handleDeleteJob={handleDeleteJob}
                    />
                </div>

                <div className="form-section">
                    <JobForm
                        title={title} setTitle={setTitle}
                        employer={employer} setEmployer={setEmployer}
                        location={location} setLocation={setLocation}
                        description={description} setDescription={setDescription}
                        status={status} setStatus={setStatus} 
                        submitFunction={editingJobId ? handleUpdateJob : handleCreateJob}
                        formpurpose={editingJobId ? "Edit job" : "Add a new job"}
                    />

                    {editingJobId && 
                        <button
                            className="secondary-btn"
                            onClick={resetForm}
                        >
                            Cancel Edit
                        </button>
                    }
                </div>
            </div>
        </div>
    )
}

export default Home