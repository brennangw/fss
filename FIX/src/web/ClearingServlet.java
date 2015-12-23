package web;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

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
	}

}
