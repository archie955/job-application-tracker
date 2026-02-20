const DisplayJobs = ({ jobs }) => {
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
                </tr>
            </thead>
            <tbody>
                {jobs.map(jobnet => 
                    <tr key={jobnet.job.id}>
                        <th>{jobnet.job.title}</th>
                        <th>{jobnet.job.employer}</th>
                        <th>{jobnet.job.location}</th>
                        <th>{jobnet.job.status}</th>
                        <th>{jobnet.job.deadline ? job.deadline : "None"}</th>
                        <th>{jobnet.assessments ? jobnet.assessments.length : 0}</th>
                    </tr>
                )}
            </tbody>
        </table>
    )
}

export default DisplayJobs