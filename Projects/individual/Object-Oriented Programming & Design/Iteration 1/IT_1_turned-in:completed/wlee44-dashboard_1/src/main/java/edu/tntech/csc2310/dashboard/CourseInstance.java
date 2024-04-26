package edu.tntech.csc2310.dashboard;

public class CourseInstance {

    public String DEPARTMENT;
    public String STUDENTCOUNT;
    public String CREDITS;
    public String CRN;
    public String COURSE;
    public String SECTION;
    public String ISTIMEDETERMINED;
    public String STARTTIME;
    public String STARTAM_PM;
    public String ENDTIME;
    public String ENDAM_PM;
    public String CLASSDAYS;
    public String ISLOCDETERMINED;
    public String BUILDING;
    public String ROOM;
    public String ISONLINE;
    public String PROF;
    public String MAXIMUMSTUDENTS;
    public String ISOPEN;
    public String TITLE;

    public Faculty faculty;
    public SubjectTerm subjectTerm;

    public void setFaculty() {
        String fullName = PROF;
        String firstName;
        String lastName;
        String[] names;
        if (fullName == null) {
            firstName = "";
            lastName = "";
        } else {
            names = fullName.split(", ");
            firstName = names[1].trim();
            lastName = names[0].trim();
        }
        faculty = new Faculty(firstName, lastName);
    }

    public void setSubjectTerm(String term) {
        subjectTerm = new SubjectTerm(DEPARTMENT, term);
    }

    public Faculty getFaculty() {
        return faculty;
    }

    public SubjectTerm getSubjectTerm() {
        return subjectTerm;
    }

    public String getDEPARTMENT() { return DEPARTMENT; }

    public String getSTUDENTCOUNT() {
        return STUDENTCOUNT;
    }

    public String getCREDITS() {
        return CREDITS;
    }

    public String getCRN() {
        return CRN;
    }

    public String getCOURSE() {
        return COURSE;
    }

    public String getSECTION() {
        return SECTION;
    }

    public String getISTIMEDETERMINED() {
        return ISTIMEDETERMINED;
    }

    public String getSTARTTIME() {
        return STARTTIME;
    }

    public String getSTARTAM_PM() {
        return STARTAM_PM;
    }

    public String getENDTIME() {
        return ENDTIME;
    }

    public String getENDAM_PM() {
        return ENDAM_PM;
    }

    public String getCLASSDAYS() {
        return CLASSDAYS;
    }

    public String getISLOCDETERMINED() {
        return ISLOCDETERMINED;
    }

    public String getBUILDING() {
        return BUILDING;
    }

    public String getROOM() {
        return ROOM;
    }

    public String getISONLINE() {
        return ISONLINE;
    }

    public String getPROF() {
        return PROF;
    }

    public String getMAXIMUMSTUDENTS() {
        return MAXIMUMSTUDENTS;
    }

    public String getISOPEN() {
        return ISOPEN;
    }

    public String getTITLE() {
        return TITLE;
    }

    public String toString(){
        return DEPARTMENT + " " + COURSE + "-" + SECTION + " (" + PROF + ") " +
                CLASSDAYS + "\t\t" + STARTTIME + STARTAM_PM + " - " + ENDTIME + ENDAM_PM + "\t" + STUDENTCOUNT + "/" + MAXIMUMSTUDENTS;
    }
}
