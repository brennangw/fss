package web;

import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;

import main.StartParties;

public class InitializeParties implements ServletContextListener {

	@Override
	public void contextDestroyed(ServletContextEvent arg0) {
		//Notification that the servlet context is about to be shut down.
	}

	@Override
	public void contextInitialized(ServletContextEvent arg0) {
		//Notification that the web application initialization process is starting
		
		StartParties.main();
		System.out.println("Session started between the client and the exchange.");
	}

}
