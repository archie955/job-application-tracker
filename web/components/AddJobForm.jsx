import { ApplicationStatus } from "../services/enum"
import DropDown from "./Dropdown"

const Input = ({ inp, setInp }) => <input value={inp} onChange={e => setInp(e.target.value)} />

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
        <form 
            onSubmit={handleSubmit}
        >
            <h2>{props.formpurpose}</h2>
            <div className="job-form">
                Job Title: <Input inp={props.title} setInp={props.setTitle} />
                Employer: <Input inp={props.employer} setInp={props.setEmployer} />
                Application Status: <DropDown status={props.status} setStatus={props.setStatus} datatype={ApplicationStatus}/>
                Location: <Input inp={props.location} setInp={props.setLocation} />
                Description: <Input inp={props.description} setInp={props.setDescription} />
            </div>
            <button type="submit">Submit</button>
        </form>
    )
}

export default JobForm