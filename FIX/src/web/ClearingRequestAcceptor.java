package web;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ClearingRequestAcceptor extends HttpServlet {
	
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		System.out.println("Clearing request received and accepted");
		
		PrintWriter pw = resp.getWriter();
		String acceptMessage = readFile(ClearingServlet.baseURI + "consentGranted.xml");
		pw.write(acceptMessage);
	}
	
	private String readFile(String file) throws IOException {
	    BufferedReader reader = new BufferedReader(new FileReader(file));
	    String line = null;
	    StringBuilder stringBuilder = new StringBuilder();
	    String ls = System.getProperty("line.separator");

	    while((line = reader.readLine()) != null) {
	        stringBuilder.append( line );
	        stringBuilder.append( ls );
	    }

	    return stringBuilder.toString();
	}
	
	private String replaceTagValues(String inp) throws IOException {
		DateFormat df2 = new SimpleDateFormat("HH:mm:ss");
		String time = df2.format(Calendar.getInstance().getTime());

		inp.replaceAll("current_time!!!!", time);
		
		return inp;
	}
}
