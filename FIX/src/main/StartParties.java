package main;

public class StartParties {

	public static ClientControl cl;
	public static ExchangeControl ex;
	
	public static void main() {
		
		ex = new ExchangeControl("C:/Users/rajan/OneDrive/Columbia/sem 1/Financial Software Systems/project/fss/FIX/resources/settings-EX.txt");
		cl = new ClientControl("C:/Users/rajan/OneDrive/Columbia/sem 1/Financial Software Systems/project/fss/FIX/resources/settings-CL.txt");

	}

}
