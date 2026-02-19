const DisplayJobs = ({ jobs }) => {
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
                {jobs.map(jobnet => {
                    <tr>
                        <th>{jobnet.job.title}</th>
                        <th>{jobnet.job.employer}</th>
                        <th>{jobnet.job.location}</th>
                        <th>{jobnet.job.status}</th>
                        <th>{jobnet.job.deadline ? job.deadline : "None"}</th>
                        <th>{jobnet.assessments.length}</th>
                    </tr>
                })}
            </tbody>
        </table>
    )
}

export default DisplayJobs