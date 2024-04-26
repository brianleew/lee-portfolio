package edu.tntech.csc2310.dashboard;

public class FacultyCreditHours extends SubjectCreditHours {
    private Faculty faculty;

    public FacultyCreditHours(Faculty faculty, int creditHoursGenerated, SubjectTerm subjectTerm) {
        super(creditHoursGenerated, subjectTerm);
        this.faculty = faculty;
    }

    public Faculty getFaculty() {
        return faculty;
    }

}