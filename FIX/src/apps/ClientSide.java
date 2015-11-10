package apps;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.HttpClients;

import quickfix.Application;
import quickfix.DoNotSend;
import quickfix.FieldNotFound;
import quickfix.IncorrectDataFormat;
import quickfix.IncorrectTagValue;
import quickfix.Message;
import quickfix.RejectLogon;
import quickfix.SessionID;
import quickfix.UnsupportedMessageType;
import quickfix.field.OrdStatus;

public class ClientSide extends quickfix.MessageCracker implements Application {

	@Override
	public void fromAdmin(Message arg0, SessionID arg1)
			throws FieldNotFound, IncorrectDataFormat, IncorrectTagValue, RejectLogon {
		
	}

	@Override
	public void fromApp(Message message, SessionID session)
			throws FieldNotFound, IncorrectDataFormat, IncorrectTagValue, UnsupportedMessageType {
		crack(message, session);
	}
	
	public void onMessage(quickfix.fix42.NewOrderSingle order, SessionID sessionID)
		      throws FieldNotFound, UnsupportedMessageType, IncorrectTagValue {
		
	}
	
	public void onMessage(quickfix.fix42.ExecutionReport report, SessionID sessionID)
		      throws FieldNotFound, UnsupportedMessageType, IncorrectTagValue {
		// TODO: Get an ack or a partial/complete fill from the exchange and relay it to the python system
		
		//HttpClient httpClient = HttpClients.createDefault();
		//HttpPost httppost = new HttpPost("http://localhost:8000/hw2/exchange-message");
		
		switch(report.getOrdStatus().getValue()) {
		case OrdStatus.ACCEPTED_FOR_BIDDING:
			// ACknowledgement
			System.out.println("received ack");
			
			break;
		case OrdStatus.PARTIALLY_FILLED:
			// Partial fill
			
			break;
		case OrdStatus.FILLED:
			// Fully filled
			
			break;
		default:
			System.out.println("Error, exec report order status not valid");
		}
		
	}
	
	@Override
	public void onCreate(SessionID arg0) {
		
	}

	@Override
	public void onLogon(SessionID arg0) {
		
	}

	@Override
	public void onLogout(SessionID arg0) {
		
	}

	@Override
	public void toAdmin(Message arg0, SessionID arg1) {
		
	}

	@Override
	public void toApp(Message arg0, SessionID arg1) throws DoNotSend {
		
	}

}
