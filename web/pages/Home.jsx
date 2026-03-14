import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../components/AuthProvider"
import DisplayJobs from "../components/JobDisplay"
import { ApplicationStatus, AssessmentType, FormType } from "../services/enum"
import JobForm from "../components/AddJobForm"
import AssessmentForm from "../components/AddAssessmentForm"




const Home = () => {
    const navigate = useNavigate()
    const { logout, getJobs, createJob, updateJob, deleteJob, createAssessment, updateAssessment, deleteAssessment } = useAuth()

    const [jobs, setJobs] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("")

    const [title, setTitle] = useState("")
    const [employer, setEmployer] = useState("")
    const [status, setStatus] = useState(ApplicationStatus.Not_Applied)
    const [description, setDescription] = useState("")
    const [location, setLocation] = useState("")

    const [editingJobId, setEditingJobId] = useState(null)

    const [jobOrAssessment, setJobOrAssessment] = useState(FormType.Job)

    const [jobAssessmentId, setJobAssessmentId] = useState(null)
    const [editingAssessmentId, setEditingAssessmentId] = useState(null)

    const [type, setType] = useState(AssessmentType.Online_Assessment)
    const [completed, setCompleted] = useState(false)


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
        setEditingAssessmentId(null)
        setJobAssessmentId(null)
        setJobOrAssessment(FormType.Job)
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
        resetForm()
        setJobOrAssessment(FormType.Job)
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

    const switchToNewAssessment = (job) => {
        resetForm()
        setJobOrAssessment(FormType.Assessment)
        setEditingAssessmentId(null)
        setDescription("")
        setJobAssessmentId(job.id)
        setType(AssessmentType.Online_Assessment)
        setCompleted(false)
    }

    const handleCreateAssessment = async (newAssessment) => {
        const updatedJob = await createAssessment(jobAssessmentId, newAssessment)
        setJobs(prev =>
            prev.map(j => j.id === updatedJob.id ? updatedJob : j)
        )
        resetForm()
    }

    const switchToEditAssessment = (assessment) => {
        setJobOrAssessment(FormType.Assessment)
        setEditingAssessmentId(assessment.id)
        setJobAssessmentId(assessment.job_id)
        setType(assessment.type)
        setDescription(assessment.description)
        setCompleted(assessment.completed)
    }

    const handleEditAssessment = async (assessment) => {
        if (editingAssessmentId === null || jobAssessmentId === null) return
        const updatedJob = await updateAssessment(jobAssessmentId, editingAssessmentId, assessment)
        setJobs(prev =>
            prev.map(j => j.id === updatedJob.id ? updatedJob : j)
        )
        resetForm()
    }

    const handleDeleteAssessment = async (assessment) => {
        const updatedJob = await deleteAssessment(assessment.job_id, assessment.id)
        setJobs(prev =>
            prev.map(j => j.id === updatedJob.id ? updatedJob : j)
        )
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
    }, [])

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
                        handleCreateAssessment={switchToNewAssessment}
                        handleEditAssessment={switchToEditAssessment}
                        handleDeleteAssessment={handleDeleteAssessment}
                    />
                </div>

                <div className="form-section">
                    {(jobOrAssessment === FormType.Job) && 
                        <JobForm
                            title={title} setTitle={setTitle}
                            employer={employer} setEmployer={setEmployer}
                            location={location} setLocation={setLocation}
                            description={description} setDescription={setDescription}
                            status={status} setStatus={setStatus} 
                            submitFunction={editingJobId !== null ? handleUpdateJob : handleCreateJob}
                            formpurpose={editingJobId !== null ? "Edit job" : "Add a new job"}
                        />
                    }
                    {(jobOrAssessment === FormType.Assessment) &&
                        <AssessmentForm
                            type={type} setType={setType}
                            completed={completed} setCompleted={setCompleted}
                            description={description} setDescription={setDescription}
                            submitFunction={editingAssessmentId !== null ? handleEditAssessment : handleCreateAssessment}
                            formpurpose={editingAssessmentId !== null ? "Edit Assessment" : "Add a new assessment"}
                        />
                    }

                    {(editingJobId || (jobOrAssessment === FormType.Assessment)) && 
                        <button
                            className="secondary-btn"
                            onClick={resetForm}
                        >
                            Reset Form
                        </button>
                    }
                </div>
            </div>
        </div>
    )
}

export default Home