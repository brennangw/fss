package web;

import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;

import main.StartParties;
import quickfix.SessionNotFound;

public class InitializeParties implements ServletContextListener {

	@Override
	public void contextDestroyed(ServletContextEvent arg0) {
		//Notification that the servlet context is about to be shut down.
	}

	@Override
	public void contextInitialized(ServletContextEvent arg0) {
		try {
			StartParties.main();
		} catch (SessionNotFound e) {
			System.out.println("No session to send test message");
			e.printStackTrace();
		}
	}

}
