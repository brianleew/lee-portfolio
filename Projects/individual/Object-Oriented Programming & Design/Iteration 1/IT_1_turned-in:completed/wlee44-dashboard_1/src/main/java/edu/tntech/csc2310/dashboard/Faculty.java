package edu.tntech.csc2310.dashboard;

public class Faculty implements Comparable<Faculty>  {
    private String firstName;
    private String lastName;

    public Faculty(String firstName, String lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }

    public String getFirstName() {
        return firstName;
    }

    public String getLastName() {
        return lastName;
    }

    @Override
    public int compareTo(Faculty o) {
        Faculty c = (Faculty)o;
        int result = 0;
        if (this.lastName.compareTo(o.getLastName()) < 0)
            result = -1;
        else if (this.lastName.compareTo(o.getLastName()) > 0)
            result = 1;
        else if (this.firstName.compareTo(o.getFirstName()) < 0)
            result = -1;
        else if (this.firstName.compareTo(o.getFirstName()) > 0)
            result = 1;
        return result;
    }

}