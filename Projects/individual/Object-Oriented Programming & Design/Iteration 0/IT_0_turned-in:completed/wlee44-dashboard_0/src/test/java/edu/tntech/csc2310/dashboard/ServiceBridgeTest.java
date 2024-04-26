package edu.tntech.csc2310.dashboard;

import com.google.gson.stream.JsonReader;
import org.junit.Before;
import org.junit.Test;
import com.google.gson.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;

public class ServiceBridgeTest {
    private CourseInstance[] c;
    private ServiceBridge b = new ServiceBridge("202210","CSC");
    @Before
    public void Setup() throws Exception {
        Gson gson = new Gson();
        URL url = new URL("https://portapit.tntech.edu/express/api/unprotected/getCourseInfoByAPIKey.php?Key=0F4E62E9-C21F-4431-9045-CE0701D5EC95&Subject=CSC&Term=202210");
        BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
        JsonReader jr = gson.newJsonReader(in);
        c = gson.fromJson(jr, CourseInstance[].class);
    }
    @Test
    public void findSubject() {
        for (int i = 0; i < b.getCourses().toString().length(); i++) {
            if (c[i].toString().contains("2310")) {
                System.out.println("\n");
            }
        }
    }
}