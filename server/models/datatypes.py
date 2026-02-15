from enum import Enum


class AssessmentType(str, Enum):
    ONLINE_ASSESSMENT = "online_assessment"
    INTERVIEW = "interview"
    ASSESSMENT_CENTRE = "assessment_centre"


class ApplicationStatus(str, Enum):
    NOT_APPLIED = "not_applied"
    APPLIED = "applied"
    REJECTED = "rejected"
    SUCCESSFUL = "successful"

