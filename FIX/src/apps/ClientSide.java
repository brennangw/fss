package apps;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;

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
		
		System.out.println("Received report from exchange. Processing it.");
		
		String URL = "http://localhost:8000/hw2/exchange-message";
		String USER_AGENT = "Eclipse-Tomcat";
		
		HttpClient httpClient = HttpClients.createDefault();
		
		HttpPost post = new HttpPost(URL);
		post.setHeader("User-Agent", USER_AGENT);
		
		List<NameValuePair> params = new ArrayList<>();
		
		switch(report.getOrdStatus().getValue()) {
		case OrdStatus.ACCEPTED_FOR_BIDDING:
			// Acknowledgement received
			System.out.println("Received ack.");
			
			params.add(new BasicNameValuePair("ClOrdID", report.getClOrdID().getValue()));
			params.add(new BasicNameValuePair("OrderID", report.getOrderID().getValue()));
			params.add(new BasicNameValuePair("ExecID", report.getExecID().getValue()));
			params.add(new BasicNameValuePair("ExecType", String.valueOf(report.getExecType().getValue())));
			params.add(new BasicNameValuePair("OrderStatus", String.valueOf(report.getOrdStatus().getValue())));
			params.add(new BasicNameValuePair("Symbol", report.getSymbol().getValue()));
			params.add(new BasicNameValuePair("Side", report.getSide().toString()));
			params.add(new BasicNameValuePair("TransactionTime", report.getTransactTime().getValue().toString()));
			
			break;
		case OrdStatus.PARTIALLY_FILLED:
			// Partial fill received
			System.out.println("Received partial fill.");
			
			params.add(new BasicNameValuePair("ClOrdID", report.getClOrdID().getValue()));
			params.add(new BasicNameValuePair("OrderID", report.getOrderID().getValue()));
			params.add(new BasicNameValuePair("ExecID", report.getExecID().getValue()));
			params.add(new BasicNameValuePair("ExecType", String.valueOf(report.getExecType().getValue())));
			params.add(new BasicNameValuePair("OrderStatus", String.valueOf(report.getOrdStatus().getValue())));
			params.add(new BasicNameValuePair("Symbol", report.getSymbol().getValue()));
			params.add(new BasicNameValuePair("Side", report.getSide().toString()));
			params.add(new BasicNameValuePair("TransactionTime", report.getTransactTime().getValue().toString()));
			params.add(new BasicNameValuePair("LastShares", String.valueOf(report.getLastShares().getValue())));
			params.add(new BasicNameValuePair("LastPrice", String.valueOf(report.getLastPx().getValue())));
			
		case OrdStatus.FILLED:
			// Full fill received
			System.out.println("Received full fill.");
			
			params.add(new BasicNameValuePair("ClOrdID", report.getClOrdID().getValue()));
			params.add(new BasicNameValuePair("OrderID", report.getOrderID().getValue()));
			params.add(new BasicNameValuePair("ExecID", report.getExecID().getValue()));
			params.add(new BasicNameValuePair("ExecType", String.valueOf(report.getExecType().getValue())));
			params.add(new BasicNameValuePair("OrderStatus", String.valueOf(report.getOrdStatus().getValue())));
			params.add(new BasicNameValuePair("Symbol", report.getSymbol().getValue()));
			params.add(new BasicNameValuePair("Side", report.getSide().toString()));
			params.add(new BasicNameValuePair("TransactionTime", report.getTransactTime().getValue().toString()));
			params.add(new BasicNameValuePair("LastShares", String.valueOf(report.getLastShares().getValue())));
			params.add(new BasicNameValuePair("LastPrice", String.valueOf(report.getLastPx().getValue())));
			
			break;
		default:
			System.out.println("Error, exec report order status not valid");
			return;
		}
		
		/*try {
			// Attaching the parameters and sending the data to python
			post.setEntity(new UrlEncodedFormEntity(params));
			HttpResponse resp = httpClient.execute(post);
			
			// TODO: Do something with the response
		} catch (UnsupportedEncodingException e) {
			System.out.println("Could not add parameters to post request");
			e.printStackTrace();
		} catch (ClientProtocolException e) {
			System.out.println("Could not send request to python - bad protocol");
			e.printStackTrace();
		} catch (IOException e) {
			System.out.println("Could not send request to client - IO exception");
			e.printStackTrace();
		}*/
		
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
