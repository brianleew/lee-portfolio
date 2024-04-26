package edu.tntech.csc2310.dashboard;

public class SubjectCreditHours {
    private int creditHoursGenerated;
    private SubjectTerm subjectTerm;

    public SubjectCreditHours(int creditHoursGenerated, SubjectTerm subjectTerm) {
        this.creditHoursGenerated = creditHoursGenerated;
        this.subjectTerm = subjectTerm;
    }

    public int getCreditHoursGenerated() {
        return creditHoursGenerated;
    }

    public SubjectTerm getSubjectTerm() {
        return subjectTerm;
    }

}