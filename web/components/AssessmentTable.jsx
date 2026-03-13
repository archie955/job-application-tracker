const AssessmentTable = ({ job, handleEditAssessment, handleDeleteAssessment }) => {
    const assessments = job.assessments ? job.assessments : [{id: null, type: null, deadline: null, completed: null, decription: null}]
    return (
        <tr className="assessment-row">
            <td colspan="8">

                <table className="assessment-table">
                    <thead>
                        <tr>
                            <th>Assessment Type</th>
                            <th>Deadline</th>
                            <th>Completed</th>
                            <th>Description</th>
                        </tr>
                    </thead>

                    <tbody>
                        {assessments.map(assessment => (
                            <tr
                                key={assessment.id}
                                className="job-row"
                                onClick={() => console.log("pressed row!")}
                            >
                                <td>{assessment.type}</td>
                                <td>{assessment.deadline}</td>
                                <td>{assessment.completed ? "✅" : "❌"}</td>
                                <td>{assessment.description}</td>
                                <td>
                                    <button type="button"
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            handleEditAssessment(assessment)
                                        }}
                                    >
                                        Update
                                    </button>
                                </td>
                                <td>
                                    <button type="button"
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            handleDeleteAssessment(assessment)
                                        }}
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </td>
        </tr>
    )
}

export default AssessmentTable