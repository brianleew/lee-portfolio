import java.sql.*;
import java.util.ArrayList;
import java.util.Scanner;

public class project3 {
    public static void main(String[] args) {
        try
        {
            String url = "jdbc:mysql://localhost:3306/library";
            Scanner kb = new Scanner(System.in);
            System.out.print("Enter your username: ");
            String un = kb.nextLine(); // get user input for username
            System.out.print("Enter your password: ");
            String pw = kb.nextLine(); // get user input for password
            Connection conn = DriverManager.getConnection(url,un,pw);
            while (true) {
                System.out.println("\nSelect an option below.\n" + // printing out the menu
                        "(a) Retrieve ISBN, title, genre name, publication date, name of the publisher, edition number and description of each book.\n" +
                        "(b) Retrieve for a book first, middle and last names of its authors.\n" +
                        "(c) Retrieve ISBN, title and barcode of every book copy.\n" +
                        "(d) Retrieve card number, first, middle and last name of every member.\n" +
                        "(e) Retrieve info (ISBN, title, barcode, date borrowed and number of renewals) of every loan that was not finalized for a chosen member.\n" +
                        "(f) Register in the system the return of a book a chosen member borrowed.\n" +
                        "(g) Borrow a book copy to a chosen member.\n" +
                        "(h) Renew a loan of a book copy to a chosen member.\n" +
                        "(i) Retrieve how much money a chosen member owes to the library.\n" +
                        "(j) Retrieve for a member ISBN, title, barcode, date borrowed, date returned and fee for every book the member owes money to the library.\n" +
                        "(k) Register in the system, for a member, a payment for a loan of a book copy that was overdue.\n" +
                        "(q) quit");
                System.out.print("Enter a choice: ");
                String choice = kb.nextLine(); // get user input for a choice
                System.out.print("\n");
                switch(choice) {
                    case "a": // (a) Retrieve ISBN, title, genre name, publication date, name of the publisher, edition number and description of each book.
                        PreparedStatement pStmt_a = conn.prepareStatement("select title, ISBN, ifnull(name, 'n/a') as genre, date_published, publisher, edition, description from BOOK natural left outer join GENRE group by ISBN;");
                        ResultSet result_a = pStmt_a.executeQuery(); // execute the query
                        System.out.println("[retrieved ISBN, title, genre name, publication date, name of the publisher, edition number and description of each book]");
                        while (result_a.next()) { // show the results
                            System.out.println(result_a.getString("title") + " | "
                                    + result_a.getString("ISBN") + " | "
                                    + result_a.getString("genre") + " | "
                                    + result_a.getString("date_published") + " | "
                                    + result_a.getString("publisher") + " | "
                                    + result_a.getString("edition") + " | "
                                    + result_a.getString("description"));
                        }
                        break;
                    case "b": // (b) Retrieve for a book first, middle and last names of its authors.
                        System.out.print("Enter the title of a book: ");
                        String tb = kb.nextLine(); // get user input for a title of a book
                        PreparedStatement pStmt_b = conn.prepareStatement("select first_name, ifnull(middle_name, 'n/a') as middle, last_name, title from AUTHOR natural left outer join BOOK_AUTHOR natural left outer join BOOK where title = ?;");
                        pStmt_b.setString(1, tb);
                        ResultSet result_b = pStmt_b.executeQuery(); // execute the query with user input
                        System.out.println("[retrieved first, middle, and last name(s) of author(s) from (" + tb + ")]");
                        while (result_b.next()) { // show the results
                            System.out.println(result_b.getString("first_name") + " | "
                                    + result_b.getString("middle") + " | "
                                    + result_b.getString("last_name"));
                        }
                        break;
                    case "c": // (c) Retrieve ISBN, title and barcode of every book copy.
                        PreparedStatement pStmt_c = conn.prepareStatement("select ISBN, title, barcode from COPY natural left outer join BOOK order by barcode;");
                        ResultSet result_c = pStmt_c.executeQuery(); // execute the query
                        System.out.println("[retrieved ISBN, title, and barcode of every book copy]");
                        while (result_c.next()) { // show the result
                            System.out.println(result_c.getString("ISBN") + " | "
                                    + result_c.getString("title") + " | "
                                    + result_c.getString("barcode"));
                        }
                        break;
                    case "d": // (d) Retrieve card number, first, middle and last name of every member.
                        PreparedStatement pStmt_d = conn.prepareStatement("select card_no, first_name, ifnull(middle_name, 'n/a') as middle, last_name from MEMBER;");
                        ResultSet result_d = pStmt_d.executeQuery(); // execute the query
                        System.out.println("[retrieved card number, first, middle, and last name of every member]");
                        while (result_d.next()) { // show the result
                            System.out.println(result_d.getString("card_no") + " | "
                                    + result_d.getString("first_name") + " | "
                                    + result_d.getString("middle") + " | "
                                    + result_d.getString("last_name"));
                        }
                        break;
                    case "e": // (e) Retrieve info (ISBN, title, barcode, date borrowed and number of renewals) of every loan that was not finalized for a chosen member.
                        System.out.print("Enter the card number of a member: ");
                        String cne = kb.nextLine(); // get user input for a card number
                        PreparedStatement pStmt_e = conn.prepareStatement("select ISBN, title, barcode, date_borrowed, renewals_no from BORROW natural left outer join COPY natural left outer join BOOK where date_returned is null and card_no = ?;");
                        pStmt_e.setString(1, cne);
                        ResultSet result_e = pStmt_e.executeQuery(); // execute the query
                        System.out.println("[retrieved ISBN, title, barcode, date_borrowed, and number of renewals of every loan that was not finalized for a chosen member (" + cne + ")]");
                        while (result_e.next()) { // show the result
                            System.out.println(result_e.getString("ISBN") + " | "
                                    + result_e.getString("title") + " | "
                                    + result_e.getString("barcode") + " | "
                                    + result_e.getString("date_borrowed") + " | "
                                    + result_e.getString("renewals_no"));
                        }
                        break;
                    case "f": // (f) Register in the system the return of a book a chosen member borrowed.
                        PreparedStatement pStmt_cnmf = conn.prepareStatement("select card_no from MEMBER order by card_no;");
                        ResultSet result_cnmf = pStmt_cnmf.executeQuery(); // execute the query
                        ArrayList<String> arc_f = new ArrayList<String>();
                        while (result_cnmf.next()) { // show the list of all unique card numbers of the members
                            System.out.println(result_cnmf.getString("card_no"));
                            arc_f.add(result_cnmf.getString("card_no")); // storing tuples in an array to compare later
                        }
                        System.out.print("Enter the card number of a member from the list of ALL members above: ");
                        String cnf = kb.nextLine(); // get user input for a card number
                        // if user enters card_no not in the query keep asking until they enter one out of the list
                        boolean f = arc_f.contains(cnf); // false if input string is not in array. true if input string is in array
                        while (!f) { // keep asking
                            System.out.println("Not in the list!");
                            System.out.print("Enter the card number of a member from the list of ALL members: ");
                            cnf = kb.nextLine(); // get user input for a card number again
                            if (arc_f.contains(cnf)) {
                                f = true; // break out of asking repeatedly
                            }
                        }
                        PreparedStatement pStmt_bcf = conn.prepareStatement("select barcode from COPY order by barcode;");
                        ResultSet result_bcf = pStmt_bcf.executeQuery(); // execute query
                        ArrayList<String> arb_f = new ArrayList<String>();
                        while (result_bcf.next()) { // show result + adding result into array
                            System.out.println(result_bcf.getString("barcode"));
                            arb_f.add(result_bcf.getString("barcode")); // storing tuples in an array to compare with user input
                        }
                        System.out.print("Enter the barcode of the book from the list of ALL book copies above: ");
                        String bf = kb.nextLine(); // get user input for a book copy
                        // if user enters barcode not in the query keep asking until they enter one out of the list
                        boolean ff = arb_f.contains(bf);
                        while (!ff) { // repeated ask until correct input
                            System.out.println("Not in the list!");
                            System.out.print("Enter the barcode of the book from the list of ALL book copies: ");
                            bf = kb.nextLine();
                            if (arb_f.contains(bf)) {
                                ff = true;
                            }
                        }
                        PreparedStatement pStmt_f = conn.prepareStatement("update BORROW set date_returned = now() where date_returned is null and card_no = ? and barcode = ?;");
                        pStmt_f.setString(1, cnf);
                        pStmt_f.setString(2, bf);
                        pStmt_f.executeUpdate(); // update the database
                        System.out.println("[registered in the system the return of a book copy (" + bf + ") to a chosen member (" + cnf + ") borrowed]");
                        break;
                    case "g": // (g) Borrow a book copy to a chosen member.
                        PreparedStatement pStmt_cnmg = conn.prepareStatement("select card_no from MEMBER order by card_no;");
                        ResultSet result_cnmg = pStmt_cnmg.executeQuery(); // execute the query
                        ArrayList<String> arc_g = new ArrayList<String>();
                        while (result_cnmg.next()) { // show the result + add result into array
                            System.out.println(result_cnmg.getString("card_no"));
                            arc_g.add(result_cnmg.getString("card_no"));
                        }
                        System.out.print("Enter the card number of a member from the list of ALL members above: ");
                        String cng = kb.nextLine(); // get user input for a card number
                        // if user enters card_no not in the query keep asking until they enter one out of the list
                        boolean g = arc_g.contains(cng); // false if input string is not in array. true if input string is in array
                        while (!g) { // keep asking until correct input
                            System.out.println("Not in the list!");
                            System.out.print("Enter the card number of a member from the list of ALL members: ");
                            cng = kb.nextLine(); // get user input for a card number again
                            if (arc_g.contains(cng)) {
                                g = true;
                            }
                        }
                        PreparedStatement pStmt_bch = conn.prepareStatement("select barcode from COPY order by barcode;");
                        ResultSet result_bch = pStmt_bch.executeQuery(); // execute the query
                        ArrayList<String> arb_g = new ArrayList<String>();
                        while (result_bch.next()) { // show the result + add result into array
                            System.out.println(result_bch.getString("barcode"));
                            arb_g.add(result_bch.getString("barcode"));
                        }
                        System.out.print("Enter the barcode of the book from the list of ALL book copies above: ");
                        String bg = kb.nextLine(); // get user input for a book copy
                        // if user enters barcode not in the query keep asking until they enter one out of the list
                        boolean gg = arb_g.contains(bg);
                        while (!gg) { // keep asking until correct input
                            System.out.println("Not in the list!");
                            System.out.print("Enter the barcode of the book from the list of ALL book copies: ");
                            bg = kb.nextLine(); // get user input for a barcode again
                            if (arb_g.contains(bg)) {
                                gg = true;
                            }
                        }
                        PreparedStatement pStmt_g = conn.prepareStatement("insert into BORROW values (?,?,now(),null,0,null);");
                        pStmt_g.setString(1, cng);
                        pStmt_g.setString(2, bg);
                        pStmt_g.executeUpdate(); // insert info into database
                        System.out.println("[member (" + cng + ") borrowing a book copy (" + bg + ") on current day was inserted into the system]");
                        break;
                    case "h": // (h) Renew a loan of a book copy to a chosen member.
                        PreparedStatement pStmt_cnmh = conn.prepareStatement("select card_no from MEMBER order by card_no;");
                        ResultSet result_cnmh = pStmt_cnmh.executeQuery(); // execute the query
                        ArrayList<String> arc_h = new ArrayList<String>();
                        while (result_cnmh.next()) { // show the result + add result into array
                            System.out.println(result_cnmh.getString("card_no"));
                            arc_h.add(result_cnmh.getString("card_no"));
                        }
                        System.out.print("Enter the card number of a member from the list of ALL members above: ");
                        String cnh = kb.nextLine(); // get user input for a card number
                        // if user enters card_no not in the query keep asking until they enter one out of the list
                        boolean h = arc_h.contains(cnh); // false if input string is not in array. true if input string is in array
                        while (!h) { // keep asking until correct input
                            System.out.println("Not in the list!");
                            System.out.print("Enter the card number of a member from the list of ALL members: ");
                            cnh = kb.nextLine(); // get user input for a card number again
                            if (arc_h.contains(cnh)) {
                                h = true;
                            }
                        }
                        PreparedStatement pStmt_h = conn.prepareStatement("update BORROW set renewals_no = renewals_no+1 where renewals_no < 2 and date_returned is null and card_no = ?;");
                        pStmt_h.setString(1, cnh);
                        pStmt_h.executeUpdate(); // update the database
                        System.out.println("[renewed a loan of a book copy for the member (" + cnh + ")]");
                        break;
                    case "i": // (i) Retrieve how much money a chosen member owes to the library.
                        System.out.print("Enter the card number of a member: ");
                        String cni = kb.nextLine(); // get user input for a card number
                        PreparedStatement pStmt_i = conn.prepareStatement("select card_no, first_name, ifnull(middle_name, 'n/a') as middle, last_name, ifnull(sum(abs(m)),0) as fee from\n" +
                                "MEMBER natural left outer join\n" +
                                "(select card_no, barcode, date_borrowed, date_returned, renewals_no, abs(datediff(date_returned, date_add(date_borrowed, interval renewals_no * 14 DAY)) * .25) as m\n" +
                                "from BORROW\n" +
                                "where date_returned is not null\n" +
                                "union\n" +
                                "select card_no, barcode, date_borrowed, date_returned, renewals_no, (datediff(now(), date_add(date_borrowed, interval renewals_no * 14 DAY)) * .25) as m\n" +
                                "from BORROW\n" +
                                "where date_returned is null) as t1\n" +
                                "natural left outer join COPY\n" +
                                "natural left outer join BOOK\n" +
                                "where card_no = ?\n" +
                                "group by card_no;");
                        pStmt_i.setString(1, cni);
                        ResultSet result_i = pStmt_i.executeQuery(); // execute the query
                        System.out.println("[retrieved how much " + cni + " owes to the library]");
                        while (result_i.next()) { // show results
                            System.out.println(result_i.getString("card_no") + " | "
                                    + result_i.getString("first_name") + " | "
                                    + result_i.getString("middle") + " | "
                                    + result_i.getString("last_name") + " | "
                                    + result_i.getString("fee"));
                        }
                        break;
                    case "j": // (j) Retrieve for a member ISBN, title, barcode, date borrowed, date returned and fee for every book the member owes money to the library.
                        System.out.print("Enter the card number of a member: ");
                        String cnj = kb.nextLine();
                        PreparedStatement pStmt_j = conn.prepareStatement("select ISBN, title, barcode, date_borrowed, date_returned, abs(m) as fee, renewals_no from\n" +
                                "(select card_no, barcode, date_borrowed, date_returned, renewals_no, abs(datediff(date_returned, date_add(date_borrowed, interval renewals_no * 14 DAY)) * .25) as m\n" +
                                "from BORROW\n" +
                                "where date_returned is not null\n" +
                                "union\n" +
                                "select card_no, barcode, date_borrowed, date_returned, renewals_no, (datediff(now(), date_add(date_borrowed, interval renewals_no * 14 DAY)) * .25) as m\n" +
                                "from BORROW\n" +
                                "where date_returned is null) as t1\n" +
                                "natural left outer join COPY\n" +
                                "natural left outer join BOOK\n" +
                                "where card_no = ?;");
                        pStmt_j.setString(1, cnj);
                        ResultSet result_j = pStmt_j.executeQuery(); // execute query
                        System.out.println("[retrieved for a member (" + cnj + ") the ISBN, title, barcode, date borrowed, date returned, and fee for every book the member owes to the library]");
                        while (result_j.next()) { // show results
                            System.out.println(result_j.getString("ISBN") + " | "
                                    + result_j.getString("title") + " | "
                                    + result_j.getString("barcode") + " | "
                                    + result_j.getString("date_borrowed") + " | "
                                    + result_j.getString("date_returned") + " | "
                                    + result_j.getString("fee"));
                        }
                        break;
                    case "k": // (k) Register in the system, for a member, a payment for a loan of a book copy that was overdue.
                        PreparedStatement pStmt_cnmk = conn.prepareStatement("select card_no from MEMBER order by card_no;");
                        ResultSet result_cnmk = pStmt_cnmk.executeQuery(); // execute the query
                        ArrayList<String> arc_k = new ArrayList<String>();
                        while (result_cnmk.next()) { // show the list of all unique card numbers of the members
                            System.out.println(result_cnmk.getString("card_no"));
                            arc_k.add(result_cnmk.getString("card_no")); // storing tuples in an array to compare later
                        }
                        System.out.print("Enter the card number of a member from the list of ALL members above: ");
                        String cnk = kb.nextLine(); // get user input for a card number
                        // if user enters card_no not in the query keep asking until they enter one out of the list
                        boolean k = arc_k.contains(cnk); // false if input string is not in array. true if input string is in array
                        while (!k) { // keep asking
                            System.out.println("Not in the list!");
                            System.out.print("Enter the card number of a member from the list of ALL members: ");
                            cnk = kb.nextLine(); // get user input for a card number again
                            if (arc_k.contains(cnk)) {
                                k = true; // break out of asking repeatedly
                            }
                        }
                        PreparedStatement pStmt_k1 = conn.prepareStatement("update BORROW set paid = true where date_returned is null and card_no = ? and datediff(now(), date_add(date_borrowed, interval renewals_no * 14 DAY)) > 14;");
                        pStmt_k1.setString(1, cnk);
                        pStmt_k1.executeUpdate(); // update the database
                        PreparedStatement pStmt_k2 = conn.prepareStatement("update BORROW set paid = true where date_returned is not null and card_no = ? and abs(datediff(date_add(date_borrowed, interval renewals_no * 14 DAY), date_returned)) > 14;");
                        pStmt_k2.setString(1, cnk);
                        pStmt_k2.executeUpdate(); // update the database
                        System.out.println("[Registered " + cnk + " a payment for a loan of a book copy that was overdue]");
                        break;
                    case "q":
                        System.out.println("The program has ended.");
                        System.exit(0);
                    default:
                        System.out.println("Please enter a valid choice!");
                }
            }
        }
        catch (Exception e)
        { System.out.println(e);}
        main(args);
        }
}
