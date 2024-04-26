package edu.tntech.csc2310.dashboard;

public class CourseInstance {
    String CRN, DEPARTMENT, COURSE, SECTION, CREDITS, ISTIMEDETERMINED, STARTTIME, STARTAM_PM, ENDTIME, ENDAM_PM;
    String CLASSDAYS, ISLOCDETERMINED, BUILDING, ROOM, ISONLINE, PROF, STUDENTCOUNT, MAXIUMSTUDENT, ISOPEN, TITLE;

    public String toString() {
        return DEPARTMENT + " " + COURSE + "-" + SECTION + " (" + PROF + ") " + CLASSDAYS + " " + STARTTIME + STARTAM_PM + " - " + ENDTIME + ENDAM_PM;
    }

}
