package main;

import quickfix.SessionNotFound;

public class StartParties {

	public static ClientControl cl;
	public static ExchangeControl ex;
	
	public static void main() throws SessionNotFound {
		
		ex = new ExchangeControl("C:/Users/rajan/OneDrive/Columbia/sem 1/Financial Software Systems/project/fss/FIX/resources/settings-EX.txt");
		cl = new ClientControl("C:/Users/rajan/OneDrive/Columbia/sem 1/Financial Software Systems/project/fss/FIX/resources/settings-CL.txt");
		
		System.out.println("Session started between the client and the exchange.");
		
	}

}
