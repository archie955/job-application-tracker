import { AssessmentType } from "../services/enum"
import DropDown from "./Dropdown"

const Input = ({ inp, setInp }) => <input value={inp} onChange={e => setInp(e.target.value)} />

const AssessmentForm = (props) => {
    const handleSubmit = (e) => {
        e.preventDefault()

        const newAssessment = {
            type: props.type,
            description: props.description,
            completed: props.completed,
        }
        console.log(newAssessment)
        props.submitFunction(newAssessment)
    }
    return (
        <form 
            onSubmit={handleSubmit}
        >
            <h2>{props.formpurpose}</h2>
            <div className="job-form">
                Assessment Type: <DropDown status={props.type} setStatus={props.setType} datatype={AssessmentType}/>
                Description: <Input inp={props.description} setInp={props.setDescription} />
                Completed: <input type="checkbox" onChange={e => props.setCompleted(e.target.checked)} checked={props.completed} />
            </div>
            <button type="submit">Submit</button>
        </form>
    )
}

export default AssessmentForm