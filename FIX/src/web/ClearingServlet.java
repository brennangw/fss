package web;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Random;

import javax.jms.ConnectionFactory;
import javax.jms.JMSException;
import javax.jms.Message;
import javax.jms.Session;
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
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.jms.annotation.EnableJms;
import org.springframework.jms.config.JmsListenerContainerFactory;
import org.springframework.jms.config.SimpleJmsListenerContainerFactory;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.jms.core.MessageCreator;
import org.springframework.util.FileSystemUtils;

@SuppressWarnings("serial")
@SpringBootApplication
@EnableJms
public class ClearingServlet extends HttpServlet {
	
	public static String baseURI = "C:/Users/rajan/OneDrive/Columbia/sem 1/Financial Software Systems/project/fss/FIX/FPML_templates/";

	@Bean // Strictly speaking this bean is not necessary as boot creates a default
    JmsListenerContainerFactory<?> myJmsContainerFactory(ConnectionFactory connectionFactory) {
        SimpleJmsListenerContainerFactory factory = new SimpleJmsListenerContainerFactory();
        factory.setConnectionFactory(connectionFactory);
        return factory;
	}
        
	@Override
	protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		String startDate = req.getParameter("start");
		String endDate = req.getParameter("termination");
		String notional = req.getParameter("notional");
		String floatRate = req.getParameter("float_idx");
		String floatSpread = req.getParameter("spread");
		String fixedRate = req.getParameter("fixed");
		String fixedRatePayer = req.getParameter("payer");
		String traderID = req.getParameter("trader_id");
		
		// Send request for consent
		String reqConsent = readFile(baseURI + "requestConsent.xml");
		reqConsent = replaceTagValues(reqConsent, 
				startDate, 
				endDate, 
				notional, 
				floatRate, 
				floatSpread, 
				fixedRate, 
				fixedRatePayer,
				traderID);
		String URL = "http://localhost:8080/FIX/request-clearing";
		String USER_AGENT = "Eclipse-Tomcat";
		HttpClient httpClient = HttpClients.createDefault();
		HttpPost post = new HttpPost(URL);
		post.setHeader("User-Agent", USER_AGENT);
		List<NameValuePair> params = new ArrayList<>();
		params.add(new BasicNameValuePair("message", reqConsent));
		
		post.setEntity(new UrlEncodedFormEntity(params));
		HttpResponse httpResp = httpClient.execute(post);
		String responseFromClearing = httpResp.toString();
		
		System.out.println("Clearing accept received. Now randomly generating confirmed/refused.");
		
		// Now send the confirm/refused generated randomly
		Random rand = new Random();
		int randomInteger = rand.nextInt(100);
		String consentStatus = randomInteger > 50 ? 
								readFile(ClearingServlet.baseURI + "clearingConfirmed.xml"):
								readFile(ClearingServlet.baseURI + "clearingRefused.xml");
		consentStatus = replaceTagValues(consentStatus, 
				startDate, 
				endDate, 
				notional, 
				floatRate, 
				floatSpread, 
				fixedRate, 
				fixedRatePayer,
				traderID);
		URL = "http://localhost:8080/FIX/clearing-status";
		USER_AGENT = "Eclipse-Tomcat";
		httpClient = HttpClients.createDefault();
		post = new HttpPost(URL);
		post.setHeader("User-Agent", USER_AGENT);
		params = new ArrayList<>();
		params.add(new BasicNameValuePair("message", consentStatus));
		
		post.setEntity(new UrlEncodedFormEntity(params));
		httpResp = httpClient.execute(post);
		
		
		// Clean out any ActiveMQ data from a previous run
        FileSystemUtils.deleteRecursively(new File("activemq-data"));

        // Launch the application
        ConfigurableApplicationContext context = SpringApplication.run(ClearingServlet.class, new String[0]);

        // Send a message
        MessageCreator messageCreator = new MessageCreator() {
            @Override
            public Message createMessage(Session session) throws JMSException {
                return session.createTextMessage("works!!");
            }
        };
        JmsTemplate jmsTemplate = context.getBean(JmsTemplate.class);
        System.out.println("Sending a new message.");
        jmsTemplate.send("consent-request-receiver", messageCreator);
        
        PrintWriter pw = resp.getWriter();
        if(randomInteger > 50) pw.write("confirmed");
        else pw.write("refused");
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
	
	private String replaceTagValues(String inp, 
			String startDate, 
			String endDate, 
			String notional, 
			String floatRate, 
			String floatSpread, 
			String fixedRate, 
			String fixedRatePayer,
			String traderID) throws IOException {
		DateFormat df = new SimpleDateFormat("MM dd, yyyy");
		String date = df.format(Calendar.getInstance().getTime());
		DateFormat df2 = new SimpleDateFormat("HH:mm:ss");
		String time = df2.format(Calendar.getInstance().getTime());
		
		inp.replaceAll("<swap>(.*)</swap>", readFile(ClearingServlet.baseURI + "swap.xml"));
		
		inp.replaceAll("trader_id!!!!", traderID);
		inp.replaceAll("trade_date!!!!", date);
		inp.replaceAll("clear_date!!!!", date);
		inp.replaceAll("current_time!!!!", time);
		inp.replaceAll("StartDate!!!!", startDate);
		inp.replaceAll("Termination!!!!", endDate);
		inp.replaceAll("Notional!!!!", notional);
		inp.replaceAll("FixedRate!!!!", fixedRate);
		
		return inp;
	}

}
