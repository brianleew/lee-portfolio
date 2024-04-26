package edu.tntech.csc2310.dashboard;

import com.google.gson.Gson;
import com.google.gson.stream.JsonReader;
import edu.tntech.csc2310.dashboard.data.*;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.TreeSet;

@RestController
public class ServiceBridge {

    private static final String apiKey = "0F4E62E9-C21F-4431-9045-CE0701D5EC95";
    private static final String urlString = "https://portapit.tntech.edu/express/api/unprotected/getCourseInfoByAPIKey.php?Subject=%s&Term=%s&Key=%s";

    private CourseInstance[] courses(String subject, String term) {

        String serviceString = String.format(urlString, subject.toUpperCase(), term, apiKey);
        Gson gson = new Gson();
        CourseInstance[] courses = null;

        try {
            URL url = new URL(serviceString);
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
            JsonReader jr = gson.newJsonReader(in);
            courses = gson.fromJson(jr, CourseInstance[].class);

            for (CourseInstance c: courses){
                c.setSubjectterm(term);
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return courses;
    }

    @GetMapping("/allcourses")
    public SemesterSchedule allcourses(
            @RequestParam(value = "term", defaultValue = "na") String term
    ) {

        String urlString = "https://portapi.tntech.edu/express/api/unprotected/getCourseInfoByAPIKey.php?Term=%s&Key=%s";
        String serviceString = String.format(urlString, term, apiKey);
        Gson gson = new Gson();
        CourseInstance[] gm = null;
        SemesterSchedule schedule = null;

        try {
            URL url = new URL(serviceString);
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));

            JsonReader jr = gson.newJsonReader(in);
            gm = gson.fromJson(jr, CourseInstance[].class);

            for (CourseInstance c: gm){
                c.setSubjectterm(term);
            }

            SubjectTerm subjectTerm = new SubjectTerm("ALL", term);
            schedule = new SemesterSchedule(subjectTerm, gm);

        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return schedule;
    }

    @GetMapping("/coursesbysubject")
    public SemesterSchedule coursesbysubject(
            @RequestParam(value = "subject", defaultValue = "CSC") String subject,
            @RequestParam(value = "term", defaultValue = "202210") String term
    ){
        CourseInstance[] courses = this.courses(subject, term);
        SubjectTerm subjectTerm = new SubjectTerm(subject, term);
        SemesterSchedule schedule = new SemesterSchedule(subjectTerm, courses);
        return schedule;
    }

    @GetMapping("/coursesbyfaculty")
    public ArrayList<CourseInstance> coursesbyfaculty(
            @RequestParam(value = "subject", defaultValue = "CSC") String subject,
            @RequestParam(value = "term", defaultValue = "202210") String term,
            @RequestParam(value = "lastname", defaultValue = "Gannod") String lastname,
            @RequestParam(value = "firstname", defaultValue = "Gerald C") String firstname
    ) {

        CourseInstance[] courses = this.courses(subject, term);

        ArrayList<CourseInstance> list = new ArrayList<>();

        for (CourseInstance c: courses){
            Faculty f = c.getFaculty();
            if (f.getLastname() != null && f.getFirstname() != null) {
                if (lastname.toLowerCase().contentEquals(f.getLastname().toLowerCase()) && firstname.toLowerCase().contentEquals(f.getFirstname().toLowerCase()))
                    list.add(c);
            }
        }
        return list;
    }

    @GetMapping("/coursebysection")
    public CourseInstance coursebysection(
            @RequestParam(value = "subject", defaultValue = "CSC") String subject,
            @RequestParam(value = "term", defaultValue = "202210") String term,
            @RequestParam(value = "course", defaultValue = "2310") String course,
            @RequestParam(value = "section", defaultValue = "001") String section
    ) {
        CourseInstance[] courses = this.courses(subject, term);

        CourseInstance result = null;
        for (CourseInstance c: courses){
            if (c.getCOURSE().contentEquals(course) && c.getSECTION().contentEquals(section))
                result = c;
        }
        return result;
    }

    @GetMapping("/schbydepartment")
    public SubjectCreditHours creditHours(
            @RequestParam(value = "subject", defaultValue = "CSC") String subject,
            @RequestParam(value = "term", defaultValue = "202210") String term
    ) {

        CourseInstance[] gm = this.courses(subject, term);
        int scrh = 0;

        for (CourseInstance i : gm){
            scrh += i.getSTUDENTCOUNT() * i.getCREDITS();
        }
        SubjectCreditHours sch = new SubjectCreditHours(subject, term, scrh);
        return sch;
    }

    @GetMapping("/schbyfaculty")
    public FacultyCreditHours creditHoursByFaculty(
            @RequestParam(value = "subject", defaultValue = "CSC") String subject,
            @RequestParam(value = "term", defaultValue = "202210") String term,
            @RequestParam(value = "lastname", defaultValue = "Gannod") String lastname,
            @RequestParam(value = "firstname", defaultValue = "Gerald C") String firstname
    ) {
        CourseInstance[] courses = this.courses(subject, term);
        int scrh = 0;
        for (CourseInstance c : courses){
            Faculty f = c.getFaculty();
            if (f.getLastname() != null && f.getFirstname() != null) {
                if (lastname.toLowerCase().contentEquals(f.getLastname().toLowerCase()) && firstname.toLowerCase().contentEquals(f.getFirstname().toLowerCase()))
                    scrh += c.getSTUDENTCOUNT() * c.getCREDITS();
            }
        }
        FacultyCreditHours sch = new FacultyCreditHours(subject, term, lastname, firstname, scrh);
        return sch;
    }

    /**
     *
     * @param subject This is the subject parameter passed into the localhost url to request a corresponding subject from this service.
     *                It is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to a particular subject.
     * @param beginterm This is the beginterm parameter passed into the localhost url to request a corresponding beginterm from this service.
     *                  It is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to a particular beginterm.
     *                  It is also used to calculate or evaluate the terms in between to retrieve its data.
     * @param endterm This is the endterm parameter passed into the localhost url to request a corresponding endterm from this service.
     *                It is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to a particular endterm.
     *                It is also used to calculate or evaluate the terms in between to retrieve its data.
     * @return returns an arraylist type SubjectCreditHours called list which contains the semester credit hours generated by a specific subject within beginterm, terms in between, and endterm.
     */
    @GetMapping("/schbydeptandterms")
    public ArrayList<SubjectCreditHours> schbydeptandterms( // Semester Credit Hour(s) by Department and Terms
            @RequestParam(value = "subject", defaultValue = "na") String subject,
            @RequestParam(value = "beginterm", defaultValue = "na") int beginterm,
            @RequestParam(value = "endterm", defaultValue = "na") int endterm
    ) {
        ArrayList<SubjectCreditHours> list = new ArrayList<>();
        while(beginterm != endterm){
            CourseInstance[] gm = this.courses(subject, Integer.toString(beginterm));
            int credit = 0;
            for (CourseInstance i : gm){
                credit += i.getSTUDENTCOUNT() * i.getCREDITS();
            }
            SubjectCreditHours sch = new SubjectCreditHours(subject, Integer.toString(beginterm), credit);
            list.add(sch);

            beginterm = Math.addExact(beginterm, 30);
            if (beginterm % 100 == 40) {
                beginterm = Math.addExact(beginterm, 10);
            }

            if (beginterm == endterm) {
                CourseInstance[] g = this.courses(subject, Integer.toString(endterm));
                int cred = 0;
                for (CourseInstance j : g) {
                    cred += j.getSTUDENTCOUNT() * j.getCREDITS();
                }
                SubjectCreditHours s = new SubjectCreditHours(subject, Integer.toString(endterm), cred);
                list.add(s);
            }
        }
        return list;
    }

    /**
     *
     * @param subject This is the subject parameter passed into the localhost url to request a corresponding subject from this service.
     *                It is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to a particular subject.
     * @param termlist This is the termlist parameter passed into the localhost url to request each corresponding term separated by comma(s).
     *                 It is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to each term.
     * @return returns an arraylist type SubjectCreditHours called list which contains semester credit hours generated by a specific subject within each term.
     */
    @GetMapping("/schbydeptandtermlist")
    public ArrayList<SubjectCreditHours> schbydeptandtermlist(
            @RequestParam(value = "subject", defaultValue = "na") String subject,
            @RequestParam(value = "termlist", defaultValue = "na") String termlist
    ) {
        ArrayList<SubjectCreditHours> list = new ArrayList<>();
        String[] terms = termlist.split(",");
        for (int k = 0; k < terms.length; k++){
            CourseInstance[] gm = this.courses(subject, terms[k]);
            int credit = 0;
            for (CourseInstance i : gm) {
                credit += i.getSTUDENTCOUNT() * i.getCREDITS();
            }
            SubjectCreditHours sch = new SubjectCreditHours(subject, terms[k], credit);
            list.add(sch);
        }
       return list;
    }

    /**
     *
     * @param subject This is the subject parameter passed into the localhost url to request a corresponding subject from this service.
     *                It is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to a particular subject.
     * @param lastname This is the lastname parameter passed into the localhost url to request corresponding lastname from this service.
     *                 Also, this is evaluated to match the lastname in the Faculty object within CourseInstance[] gm.
     * @param firstname This is the firstname parameter passed into the localhost url to request corresponding firstname from this service.
     *                  Also, this is evaluated to match the firstname in the Faculty object within CourseInstance[] gm.
     * @param beginterm This is the beginterm parameter passed into the localhost url to request corresponding beginterm from this service.
     *                  It is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to beginterm.
     *                  It is also used to calculate or evaluate the terms in between to retrieve its data.
     * @param endterm This is the endterm parameter passed into the localhost url to request corresponding endterm from this service.
     *                It is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to endterm.
     *                It is also used to calculate or evaluate the terms in between to retrieve its data.
     * @return returns an arraylist type FacultyCreditHours called list which contains semester credit hours generated by a specific subject with respect to lastname and firstname within beginterm, terms in between, and endterm.
     */
    @GetMapping("/schbyfacultyandterms")
    public ArrayList<FacultyCreditHours> schbyfacultyandterms(
            @RequestParam(value = "subject", defaultValue = "na") String subject,
            @RequestParam(value = "lastname", defaultValue = "na") String lastname,
            @RequestParam(value = "firstname", defaultValue = "na") String firstname,
            @RequestParam(value = "beginterm", defaultValue = "na") int beginterm,
            @RequestParam(value = "endterm", defaultValue = "na") int endterm
    ) {
        ArrayList<FacultyCreditHours>list = new ArrayList<>();
        while(beginterm != endterm){
            CourseInstance[] gm = this.courses(subject, Integer.toString(beginterm));
            int credit = 0;
            for (CourseInstance c : gm){
                Faculty f = c.getFaculty();
                if (f.getLastname() != null && f.getFirstname() != null) {
                if (lastname.toLowerCase().contentEquals(f.getLastname().toLowerCase()) && firstname.toLowerCase().contentEquals(f.getFirstname().toLowerCase()))
                credit += c.getSTUDENTCOUNT() * c.getCREDITS();
                }
            }
            FacultyCreditHours sch = new FacultyCreditHours(subject, Integer.toString(beginterm), lastname, firstname, credit);
            list.add(sch);

            beginterm = Math.addExact(beginterm, 30);
            if (beginterm % 100 == 40) {
                beginterm = Math.addExact(beginterm, 10);
            }

            if (beginterm == endterm) {
                CourseInstance[] g = this.courses(subject, Integer.toString(endterm));
                int cred = 0;
                for (CourseInstance b : g) {
                    Faculty ff = b.getFaculty();
                    if (ff.getLastname() != null && ff.getFirstname() != null) {
                        if (lastname.toLowerCase().contentEquals(ff.getLastname().toLowerCase()) && firstname.toLowerCase().contentEquals(ff.getFirstname().toLowerCase()))
                            cred += b.getSTUDENTCOUNT() * b.getCREDITS();
                    }
                }
                FacultyCreditHours ss = new FacultyCreditHours(subject, Integer.toString(endterm), lastname, firstname, cred);
                list.add(ss);
            }
        }
        return list;
    }

    /**
     *
     * @param subject This is the subject parameter passed into the localhost url to request a corresponding subject from this service.
     *                It is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to a particular subject.
     * @param lastname This is the lastname parameter passed into the localhost url to request corresponding lastname from this service.
     *                 Also, this is evaluated to match the lastname in the Faculty object within CourseInstance[] gm.
     * @param firstname This is the firstname parameter passed into the localhost url to request corresponding firstname from this service.
     *                  Also, this is evaluated to match the firstname in the Faculty object within CourseInstance[] gm.
     * @param termlist This is the termlist parameter passed into the localhost url to request each corresponding term separated by comma(s).
     *                 It is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to each term.
     * @return returns an arraylist type FacultyCreditHours which contains semester credit hours generated by a specific subject with respect to lastname and firstname within each term.
     */
    @GetMapping("/schbyfacultyandtermlist")
    public ArrayList<FacultyCreditHours> schbyfacultyandtermlist(
            @RequestParam(value = "subject", defaultValue = "na") String subject,
            @RequestParam(value = "lastname", defaultValue = "na") String lastname,
            @RequestParam(value = "firstname", defaultValue = "na") String firstname,
            @RequestParam(value = "termlist", defaultValue = "na") String termlist
    ) {
        ArrayList<FacultyCreditHours>list = new ArrayList<>();
        String[] terms = termlist.split(",");
        for (int k = 0; k < terms.length; k++) {
            CourseInstance[] gm = this.courses(subject, terms[k]);
            int credit = 0;
            for (CourseInstance i : gm) {
                Faculty ff = i.getFaculty();
                if (ff.getLastname() != null && ff.getFirstname() != null) {
                    if (lastname.toLowerCase().contentEquals(ff.getLastname().toLowerCase()) && firstname.toLowerCase().contentEquals(ff.getFirstname().toLowerCase()))
                        credit += i.getSTUDENTCOUNT() * i.getCREDITS();
                }
            }
            FacultyCreditHours sch = new FacultyCreditHours(subject, terms[k], lastname, firstname, credit);
            list.add(sch);
        }
        return list;
    }

    /**
     *
     * @param term This is the term parameter passed into the localhost url to request a corresponding term from this service.
     *             This is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to a particular term.
     * @param crnlist This is the crnlist parameter passed into the localhost url to request each corresponding crn separated by comma(s).
     *                Also, this is evaluated to match the CRN from the list of CRNs within a specific term to be added to another list.
     * @return returns an Arraylist of type CourseInstance called list containing all the course information in relation to CRN(s) specified by the crnlist.
     */
    @GetMapping("/coursesbycrnlist")
    public ArrayList<CourseInstance> coursesbycrnlist(
            @RequestParam(value = "term", defaultValue = "na") String term,
            @RequestParam(value = "crnlist", defaultValue = "na") String crnlist
    ) {
        ArrayList<CourseInstance> list = new ArrayList<>();
        String[] crn = crnlist.split(",");
        CourseInstance[] gm = this.courses("", term);
        for (int k = 0; k < crn.length; k++) {
            for (CourseInstance c : gm) {
                if (c.getCRN().contentEquals(crn[k])){
                    list.add(c);
                }
            }
        }
        return list;
    }

    /**
     *
     * @param term This is the term parameter passed into the localhost url to request a corresponding term from this service.
     *             This is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to particular term.
     * @param subject This is the subject parameter passed into the localhost url to request a corresponding subject from this service.
     *                It is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation to a particular subject.
     * @return returns an Arraylist of type Faculty called list which contains all the first and last names of each professor with respect to a particular term and subject.
     */
    @GetMapping("/facultybysubject")
    public ArrayList<Faculty> facultybysubject(
            @RequestParam(value = "term", defaultValue = "na") String term,
            @RequestParam(value = "subject", defaultValue = "na") String subject
    ) {
        TreeSet<Faculty> ts = new TreeSet<>();
        CourseInstance[] gm = this.courses(subject,term);
        for (CourseInstance c : gm) {
            Faculty f = c.getFaculty();
            if (f.getLastname() != null && f.getFirstname() != null) {
                ts.add(f);
            }
        }
        ArrayList<Faculty> list = new ArrayList<>(ts);
        return list;
    }

    /**
     *
     * @param term This is the term parameter passed into the localhost url to request a corresponding term from this service.
     *             This is also passed as a parameter for the API url and CourseInstance[] constructor to retrieve data in relation a particular to term.
     * @return returns an Arraylist of type String that contains all the subjects under a particular term.
     */
    @GetMapping("/getallsubjects")
    public ArrayList<String> getallsubjects(
            @RequestParam(value = "term", defaultValue = "na") String term
    ) {
        TreeSet<String> ts = new TreeSet<>();
        CourseInstance[] gm = this.courses("",term);
        for (CourseInstance c : gm) {
            ts.add(c.getSubjectterm().getSubject());
        }
        ArrayList<String> list = new ArrayList<>(ts);
        return list;
    }

}
