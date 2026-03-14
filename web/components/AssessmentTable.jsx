const AssessmentTable = ({ job, handleEditAssessment, handleDeleteAssessment }) => {
    const assessments = job.assessments || []
    if (assessments.length === 0) {
        return (
            <tr className="assessment-row">
                <td colSpan="9">No Assessments</td>
            </tr>
        )
    }

    return (
        <tr className="assessment-row">
            <td colSpan="9">
                <table className="assessment-table">
                    <thead>
                        <tr>
                            <th>Assessment Type</th>
                            <th>Deadline</th>
                            <th>Completed</th>
                            <th>Description</th>
                            <th></th>
                            <th></th>
                        </tr>
                    </thead>

                    <tbody>
                        {assessments.map(assessment => (
                            <tr key={assessment.id} className="job-row">
                                <td>{assessment.type}</td>
                                <td>{assessment.deadline}</td>
                                <td>{assessment.completed ? "✅" : "❌"}</td>
                                <td>{assessment.description}</td>

                                <td>
                                    <button
                                        type="button"
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            handleEditAssessment(assessment)
                                        }}
                                    >
                                        Update
                                    </button>
                                </td>

                                <td>
                                    <button
                                        type="button"
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