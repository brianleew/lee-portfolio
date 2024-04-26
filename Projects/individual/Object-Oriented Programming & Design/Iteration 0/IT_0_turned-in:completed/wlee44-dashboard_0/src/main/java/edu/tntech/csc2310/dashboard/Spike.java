package edu.tntech.csc2310.dashboard;
// mvn exec:java -D exec.mainClass=edu.tntech.csc2310.dashboard.Spike -D exec.args="CSC 202210 2310" "subject term course"
public class Spike {
    public static void main(String[] args) {
        ServiceBridge sb = new ServiceBridge(args[1],args[0]);
        int i = 0;
        do {
            if (sb.getCourses()[i].toString().contains(args[2])) {
                System.out.println(sb.getCourses()[i].toString());
            }
            i++;
        } while (i < sb.getCourses().toString().length()); // index length
    }
}
