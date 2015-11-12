package main;

import java.util.Date;

import quickfix.Session;
import quickfix.SessionNotFound;
import quickfix.field.ClOrdID;
import quickfix.field.HandlInst;
import quickfix.field.OrdType;
import quickfix.field.OrderQty;
import quickfix.field.Price;
import quickfix.field.Side;
import quickfix.field.Symbol;
import quickfix.field.TransactTime;

public class StartParties {

	public static ClientControl cl;
	public static ExchangeControl ex;
	
	public static void main() throws SessionNotFound {
		
		ex = new ExchangeControl("C:/Users/rajan/OneDrive/Columbia/sem 1/Financial Software Systems/project/fss/FIX/resources/settings-EX.txt");
		cl = new ClientControl("C:/Users/rajan/OneDrive/Columbia/sem 1/Financial Software Systems/project/fss/FIX/resources/settings-CL.txt");
		
		System.out.println("Session started between the client and the exchange.");
		
	}

}
