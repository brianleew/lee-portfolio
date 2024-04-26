package edu.tntech.csc2310.dashboard;

import static org.junit.Assert.*;

import edu.tntech.csc2310.dashboard.data.CourseInstance;
import edu.tntech.csc2310.dashboard.data.Faculty;
import edu.tntech.csc2310.dashboard.data.FacultyCreditHours;
import edu.tntech.csc2310.dashboard.data.SubjectCreditHours;
import org.junit.Test;

import java.util.ArrayList;

public class ServiceBridgeTest {

    @Test // this is testing if the service has the number of beginterm, terms in-between, and endterm.
    public void schbydeptandterms() {
        ArrayList<SubjectCreditHours> bridge = new ServiceBridge().schbydeptandterms("CSC", 202010, 202210);
        assertEquals("schbydeptandterms has 7 terms", 7, bridge.size());
    }

    @Test // this is testing if the service has the same number of terms as termlist.
    public void schbydeptandtermlist() {
        ArrayList<SubjectCreditHours> bridge = new ServiceBridge().schbydeptandtermlist("CSC","202010,202210");
        assertEquals("schbydeptandtermlist has 2 terms", 2, bridge.size());
    }

    @Test // this is testing if the service has the number of beginterm, terms in-between, and endterm.
    public void schbyfacultyandterms() {
        ArrayList<FacultyCreditHours> bridge = new ServiceBridge().schbyfacultyandterms("CSC","Gannod","Gerald C",202010,202210);
        assertEquals("schbyfacultyandterms has 7 terms",7,bridge.size());
    }

    @Test // this is testing if the service has the same number of terms as termlist
    public void schbyfacultyandtermlist() {
        ArrayList<FacultyCreditHours> bridge = new ServiceBridge().schbyfacultyandtermlist("CSC","Gannod","Gerald C","202010,202210");
        assertEquals("schbyfacultyandtermlist has 2 terms",2,bridge.size());
    }

    @Test // this is testing if the service has the same number of CRNs as crnlist.
    public void coursesbycrnlist() {
        ArrayList<CourseInstance> bridge = new ServiceBridge().coursesbycrnlist("202210","13519,10625");
        assertEquals("coursesbycrnlist has 2 CRNs",2,bridge.size());
    }

    @Test
    public void facultybysubject() {
        ArrayList<Faculty> bridge = new ServiceBridge().facultybysubject("202210","CSC");
        assertTrue("facultybysubject exists", bridge.size() > 0); // this is testing if facultybysubject exists
        assertEquals("The number of professors teaching CSC in 202210", 24, bridge.size()); // testing if facultybysubject has right numbers of prof.
    }

    @Test
    public void getallsubjects() {
        ArrayList<String> bridge = new ServiceBridge().getallsubjects("202210");
        assertTrue("allsubjects exists", bridge.size() > 0); // testing if getallsubjects exists
        assertEquals("The number of subjects in 202210 term",150,bridge.size()); // testing if getallsubjects has right number of subjects.
    }

}