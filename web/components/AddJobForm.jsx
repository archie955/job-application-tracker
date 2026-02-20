import ApplicationStatus from "../services/enum"

const Input = ({ inp, setInp }) => <input value={inp} onChange={e => setInp(e.target.value)} />

const DropDown = ({ status, setStatus}) => {
    const handleChange = (e) => {
        setStatus(e.target.value)
    }
    return (
        <select name="dropdown" value={status} onChange={handleChange}>
            <option value={ApplicationStatus.Not_Applied}>Not Applied</option>
            <option value={ApplicationStatus.Applied}>Applied</option>
            <option value={ApplicationStatus.Interview}>Interview</option>
            <option value={ApplicationStatus.Rejected}>Rejected</option>
            <option value={ApplicationStatus.Successful}>Successful</option>
        </select>
    )
}

const JobForm = (props) => {
    const handleSubmit = (e) => {
        e.preventDefault()

        const newJob = {
            employer: props.employer,
            title: props.title,
            status: props.status,
            description: props.description,
            location: props.location,
        }
        console.log(newJob)
        props.submitFunction(newJob)
    }
    return (
        <form onSubmit={handleSubmit}>
            <h2>Add a new job</h2>
            <div>
                Job Title: <Input inp={props.title} setInp={props.setTitle} />
                Employer: <Input inp={props.employer} setInp={props.setEmployer} />
                Application Status: <DropDown status={props.status} setStatus={props.setStatus}/>
                Location: <Input inp={props.location} setInp={props.setLocation} />
                Description: <Input inp={props.description} setInp={props.setDescription} />
            </div>
            <button type="submit">Submit</button>
        </form>
    )
}

export default JobForm