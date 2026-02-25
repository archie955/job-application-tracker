const DisplayJobs = ({ jobs, handleEditJob, handleDeleteJob }) => {
    if (jobs.length === 0) {
        return <h2>You have no jobs</h2>
    }
    return (
        <table title="Jobs">
            <thead>
                <tr>
                    <th>Job Title</th>
                    <th>Employer</th>
                    <th>Location</th>
                    <th>Status</th>
                    <th>Deadline</th>
                    <th>Number of assessments</th>
                    <th>Update</th>
                    <th>Delete</th>
                </tr>
            </thead>
            <tbody>
                {jobs.map(job => 
                    <tr key={job.id}>
                        <th>{job.title}</th>
                        <th>{job.employer}</th>
                        <th>{job.location}</th>
                        <th>{job.status}</th>
                        <th>{job.deadline ? job.deadline : "None"}</th>
                        <th>{job.assessments ? job.assessments.length : 0}</th>
                        <th>
                            <button type="button" onClick={() => handleEditJob(job)}>Update</button>
                        </th>
                        <th>
                            <button type="button" onClick={() => handleDeleteJob(job)}>Delete</button>
                        </th>
                    </tr>
                )}
            </tbody>
        </table>
    )
}

export default DisplayJobs