import { useState } from 'react'
import React from 'react'
import AssessmentTable from './AssessmentTable'

const DisplayJobs = ({ jobs, handleEditJob, handleDeleteJob, handleCreateAssessment, handleDeleteAssessment, handleEditAssessment }) => {
    const [expandedJobId, setExpandedJobId] = useState(null)

    const toggleExpand = (id) => {
        setExpandedJobId(expandedJobId === id ? null : id)
    }

    if (jobs.length === 0) {
        return <h2>You have no jobs</h2>
    }

    return (
        <table className="jobs-table" title="Jobs">
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
                {jobs.map(job => (
                    <React.Fragment key={job.id}>
                        <tr
                            key={job.id}
                            className="job-row"
                            onClick={() => toggleExpand(job.id)}
                        >
                            <td>{job.title}</td>
                            <td>{job.employer}</td>
                            <td>{job.location}</td>
                            <td>{job.status}</td>
                            <td>{job.deadline ? job.deadline : "None"}</td>
                            <td>{job.assessments ? job.assessments.length : 0}</td>

                            <td>
                                <button type="button"
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        handleEditJob(job)
                                    }}
                                >
                                    Update
                                </button>
                            </td>

                            <td>
                                <button type="button"
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        handleDeleteJob(job)
                                    }}
                                >
                                    Delete
                                </button>
                            </td>
                            <td>
                                <button type="button"
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        handleCreateAssessment(job)
                                    }}
                                >
                                    Create new assessment
                                </button>
                            </td>
                        </tr>

                        {expandedJobId === job.id && (
                            <div>
                                {job.description}
                                <AssessmentTable
                                    job={job} 
                                    handleEditAssessment={handleEditAssessment}
                                    handleDeleteAssessment={handleDeleteAssessment}
                                />
                            </div>
                        )}
                    </React.Fragment>
                ))}
            </tbody>
        </table>
    )
}

export default DisplayJobs