package edu.tntech.csc2310.dashboard;

import com.google.gson.*;
import com.google.gson.stream.JsonReader;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;

public class ServiceBridge {

    private CourseInstance[] courses;

    public ServiceBridge(String term, String subject) {
        Gson gson = new Gson();

        try {
            URL url = new URL("https://portapit.tntech.edu/express/api/unprotected/getCourseInfoByAPIKey.php?Key=0F4E62E9-C21F-4431-9045-CE0701D5EC95" + "&Term=" + term + "&Subject=" + subject);
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream())); //read the data from the network
            JsonReader jr = gson.newJsonReader(in);
            courses = gson.fromJson(jr, CourseInstance[].class);

        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public CourseInstance[] getCourses() {
        return courses;
    }

}
