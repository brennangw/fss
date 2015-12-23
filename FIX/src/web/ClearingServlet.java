package web;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;

public class ClearingServlet extends HttpServlet {

	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		String startDate = req.getParameter("start");
		String endDate = req.getParameter("termination");
		int notional = Integer.parseInt(req.getParameter("notional"));
		String floatRate = req.getParameter("float_idx");
		double floatSpread = Double.parseDouble(req.getParameter("spread"));
		double fixedRate = Double.parseDouble(req.getParameter("fixed"));
		String fixedRatePayer = req.getParameter("payer");
		
		// Send request for consent
		String fpmlMessage = "";
		String URL = "http://localhost:8080/FIX/request-clearing";
		String USER_AGENT = "Eclipse-Tomcat";
		HttpClient httpClient = HttpClients.createDefault();
		HttpPost post = new HttpPost(URL);
		post.setHeader("User-Agent", USER_AGENT);
		List<NameValuePair> params = new ArrayList<>();
		params.add(new BasicNameValuePair("message", fpmlMessage));
		
		post.setEntity(new UrlEncodedFormEntity(params));
		HttpResponse httpResp = httpClient.execute(post);
		String responseFromClearing = httpResp.toString();
		
		System.out.println("Clearing accept received. Now randomly generating confirmed/refused.");
		
		// Now send the confirm/refused generated randomly
		fpmlMessage = "";
		URL = "http://localhost:8080/FIX/clearing-status";
		USER_AGENT = "Eclipse-Tomcat";
		httpClient = HttpClients.createDefault();
		post = new HttpPost(URL);
		post.setHeader("User-Agent", USER_AGENT);
		params = new ArrayList<>();
		params.add(new BasicNameValuePair("message", fpmlMessage));
		
		post.setEntity(new UrlEncodedFormEntity(params));
		httpResp = httpClient.execute(post);
	}

}
