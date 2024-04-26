package edu.tntech.csc2310.dashboard;

import com.google.gson.*;
import com.google.gson.stream.JsonReader;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;

@RestController
public class ServiceBridge {
    private static final String apiKey = "0F4E62E9-C21F-4431-9045-CE0701D5EC95";
    private static final String urlString = "https://portapit.tntech.edu/express/api/unprotected/getCourseInfoByAPIKey.php?Subject=%s&Term=%s&Key=%s";

    public CourseInstance[] courses;

    @GetMapping("/allcourses")
    public SemesterSchedule allcourses
            (@RequestParam(value = "term", defaultValue = "na") String term) {
        Gson gson = new Gson();
        try {
            String urlFmt = String.format(urlString, "", term, apiKey);
            URL url = new URL(urlFmt);
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
            JsonReader jr = gson.newJsonReader(in);
            courses = gson.fromJson(jr, CourseInstance[].class);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        for (CourseInstance ci : courses) {
            ci.setFaculty();
            ci.setSubjectTerm(term);
        }

        return new SemesterSchedule(new SubjectTerm("ALL",term),courses);
    }

    @GetMapping("/coursesbysubject")
    public SemesterSchedule coursesbysubject
            (@RequestParam(value = "term", defaultValue = "na") String term,
            @RequestParam(value = "subject", defaultValue = "na") String subject) {
        Gson gson = new Gson();
        try {
            String urlFmt = String.format(urlString, subject, term, apiKey);
            URL url = new URL(urlFmt);
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
            JsonReader jr = gson.newJsonReader(in);
            courses = gson.fromJson(jr, CourseInstance[].class);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        for (CourseInstance ci : courses) {
            ci.setFaculty();
            ci.setSubjectTerm(term);
        }

        return new SemesterSchedule(new SubjectTerm(subject,term),courses);
    }

    @GetMapping("/coursesbyfaculty")
    public CourseInstance[] coursesbyfaculty
            (@RequestParam(value = "term", defaultValue = "na") String term,
            @RequestParam(value = "subject", defaultValue = "na") String subject,
            @RequestParam(value = "lastname", defaultValue = "na") String lastname,
            @RequestParam(value = "firstname", defaultValue = "na") String firstname) {
        Gson gson = new Gson();
        try {
        String urlFmt = String.format(urlString, subject, term, apiKey);
        URL url = new URL(urlFmt);
        BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
        JsonReader jr = gson.newJsonReader(in);
        courses = gson.fromJson(jr, CourseInstance[].class);
    } catch (MalformedURLException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    }

        for (CourseInstance ci : courses) {
            ci.setFaculty();
            ci.setSubjectTerm(term);
        }

        ArrayList<CourseInstance> courseInstArr = new ArrayList<CourseInstance>();
        Faculty f = new Faculty(firstname, lastname);
        for (CourseInstance c : courses) {
            if (f.compareTo(c.getFaculty()) == 0) {
                courseInstArr.add(c);
            }
        }

        CourseInstance[] fc = new CourseInstance[courseInstArr.size()];
        return courseInstArr.toArray(fc);
    }

    @GetMapping("/coursebysection")
    public CourseInstance coursebysection
            (@RequestParam(value = "course", defaultValue = "na") String course,
            @RequestParam(value = "term", defaultValue = "na") String term,
            @RequestParam(value = "subject", defaultValue = "na") String subject,
            @RequestParam(value = "section", defaultValue = "na") String section) {
        Gson gson = new Gson();
        try {
        String urlFmt = String.format(urlString, subject, term, apiKey);
        URL url = new URL(urlFmt);
        BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
        JsonReader jr = gson.newJsonReader(in);
        courses = gson.fromJson(jr, CourseInstance[].class);
    } catch (MalformedURLException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    }

        for (CourseInstance ci : courses) {
            ci.setFaculty();
            ci.setSubjectTerm(term);
        }

        CourseInstance cs = null;
        for (CourseInstance c : courses) {
            if (c.getSECTION().contains(section) && c.getCOURSE().contains(course)) {
                cs = c;
            }
        }
        return cs;
    }

    @GetMapping("/schbydepartment")
    public SubjectCreditHours schbydepartment
            (@RequestParam(value = "term", defaultValue = "na") String term,
            @RequestParam(value = "subject", defaultValue = "na") String subject) {
        Gson gson = new Gson();
        try {
        String urlFmt = String.format(urlString, subject, term, apiKey);
        URL url = new URL(urlFmt);
        BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
        JsonReader jr = gson.newJsonReader(in);
        courses = gson.fromJson(jr, CourseInstance[].class);
    } catch (MalformedURLException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    }

        for (CourseInstance ci : courses) {
            ci.setFaculty();
            ci.setSubjectTerm(term);
        }

        String credStr;
        int credits = 0;
        for (CourseInstance c : courses) {
            credStr = c.getCREDITS();
            if (credStr == null) {
                credStr = "0.0";
            }
            credits += Integer.parseInt(credStr.substring(0,1));
        }

        SubjectTerm st = new SubjectTerm(subject, term);
        return new SubjectCreditHours(credits, st);
    }

    @GetMapping("/schbyfaculty")
    public FacultyCreditHours schbyfaculty
            (@RequestParam(value = "term", defaultValue = "na") String term,
             @RequestParam(value = "subject", defaultValue = "na") String subject,
            @RequestParam(value = "lastname", defaultValue = "na") String lastname,
            @RequestParam(value = "firstname", defaultValue = "na") String firstname) {
        Gson gson = new Gson();
        try {
        String urlFmt = String.format(urlString, subject, term, apiKey);
        URL url = new URL(urlFmt);
        BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
        JsonReader jr = gson.newJsonReader(in);
        courses = gson.fromJson(jr, CourseInstance[].class);
    } catch (MalformedURLException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    }

        for (CourseInstance ci : courses) {
            ci.setFaculty();
            ci.setSubjectTerm(term);
        }

        Faculty f = new Faculty(firstname, lastname);

        String credStr;
        int credits = 0;
        for (CourseInstance c : courses) {
            credStr = c.getCREDITS();
            if (credStr == null) {
                credStr = "0.0";
            }
            if (f.compareTo(c.getFaculty()) != 0) {
                credits += 0;
            }
            else
            credits += Integer.parseInt(credStr.substring(0,1));
        }

        SubjectTerm st = new SubjectTerm(subject,term);
        return new FacultyCreditHours(f, credits, st);
    }

}
