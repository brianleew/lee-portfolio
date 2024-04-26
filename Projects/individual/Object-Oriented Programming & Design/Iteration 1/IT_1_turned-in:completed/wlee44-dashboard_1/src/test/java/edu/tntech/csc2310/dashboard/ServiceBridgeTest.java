package edu.tntech.csc2310.dashboard;

import org.junit.Test;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class ServiceBridgeTest {

    @Test
    public void allcoursesExist() {
        SemesterSchedule bridge = new ServiceBridge().allcourses("202210");
        assertTrue("all courses exist", bridge.getSubjectTerm().getTerm().length() > 0);
    }

    @Test
    public void allcoursesDontExist() {
        SemesterSchedule bridge = new ServiceBridge().allcourses("202220");
        CourseInstance[] ci = bridge.getSchedule();
        assertEquals("all courses do not exist", 0 , ci.length);
    }

    @Test
    public void coursesbysubjectExist () {
        SemesterSchedule bridge = new ServiceBridge().coursesbysubject("202210","CSC");
        assertTrue("courses by subject exists", bridge.getSubjectTerm().getSubject().length() > 0);
    }

    @Test
    public void coursesbysubjectDontExist() {
        SemesterSchedule bridge = new ServiceBridge().coursesbysubject("202215","CSS");
        CourseInstance[] ci = bridge.getSchedule();
        assertEquals("courses by subject does not exist",0, ci.length);
    }

    @Test
    public void coursesbyfacultyExist() {
        CourseInstance[] bridge = new ServiceBridge().coursesbyfaculty("202210","CSC","Gannod","Gerald C");
        assertTrue("courses by faculty exist", bridge.length > 0);
    }

    @Test
    public void coursesbyfacultyDontExist() {
        CourseInstance[] bridge = new ServiceBridge().coursesbyfaculty("202210","CSC","Lee","Brian");
        assertEquals("courses by faculty exist do not exist", 0, bridge.length);
    }


    @Test
    public void coursebysectionExists() {
        CourseInstance bridge = new ServiceBridge().coursebysection("2310","202210","CSC","101");
        assertTrue("course by section exists",bridge.getSECTION().length() > 0);
    }


    @Test
    public void schbydepartmentExists() {
        SubjectCreditHours bridge = new ServiceBridge().schbydepartment("202210","CSC");
        assertTrue("semester credit hours exist", bridge.getCreditHoursGenerated() > 0);
    }

    @Test
    public void schbyfacultyExists() {
        FacultyCreditHours bridge = new ServiceBridge().schbyfaculty("202210","CSC","Gannod","Gerald C");
        assertTrue("schbyfacultyExists",bridge.getCreditHoursGenerated() > 0);
    }
}