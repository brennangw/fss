package main;

import java.io.FileInputStream;
import java.util.Date;

import apps.ClientSide;
import quickfix.*;
import quickfix.field.ClOrdID;
import quickfix.field.HandlInst;
import quickfix.field.OrdType;
import quickfix.field.OrderQty;
import quickfix.field.Price;
import quickfix.field.Side;
import quickfix.field.Symbol;
import quickfix.field.TransactTime;
import quickfix.fix42.NewOrderSingle;

public class ClientControl {

	Initiator client;
	
	public ClientControl(String clientFile) {
		
	    Application application = new ClientSide();

	    try {
	    SessionSettings clientSettings = new SessionSettings(new FileInputStream(clientFile));
	    MessageStoreFactory clientStoreFactory = new FileStoreFactory(clientSettings);
	    LogFactory clientLogFactory = new FileLogFactory(clientSettings);
	    MessageFactory clientMessageFactory = new DefaultMessageFactory();
	    client = new SocketInitiator
	      (application, clientStoreFactory, clientSettings, clientLogFactory, clientMessageFactory);
	    
	    client.start();
	    
	    // Sending test request
	    quickfix.fix42.NewOrderSingle mess = new quickfix.fix42.NewOrderSingle (
				new ClOrdID("321"),
				new HandlInst(HandlInst.MANUAL_ORDER),
				new Symbol("XYZ"),
				new Side(Side.BUY),
				new TransactTime(new Date()), 
				new OrdType(OrdType.MARKET));
		
		mess.set(new Price(Double.parseDouble("200")));
		mess.set(new OrderQty(Double.parseDouble("50")));

		Session.sendToTarget(mess, "CL", "EX");
	   
	    } catch(Exception e) {
	    	e.printStackTrace();
	    }
	}
	
	public void endConnection() {
		client.stop();
	}

	public boolean trySendingMessage(NewOrderSingle mess) throws SessionNotFound {
		return Session.sendToTarget(mess, "CL", "EX");
	}

}
