package web;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ClearingRequestAcceptor extends HttpServlet {
	
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		System.out.println("Clearing request received and accepted");
		
		PrintWriter pw = resp.getWriter();
		String acceptMessage = "";
		pw.write(acceptMessage);
	}
}
