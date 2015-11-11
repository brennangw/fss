package apps;

import java.util.Date;

import quickfix.*;
import quickfix.field.*;
import quickfix.fix42.ExecutionReport;
import quickfix.fix42.NewOrderSingle;

public class ExchangeSide extends quickfix.MessageCracker implements Application {

	public int execId;
	
	public ExchangeSide() {
		this.execId = 0;
	}
	
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

		OrdType ordType = order.getOrdType();
		ClOrdID clOrdID = order.getClOrdID();
		OrderQty orderQty = order.getOrderQty();
		Price price = order.getPrice();
		Symbol symbol = order.getSymbol();
		Side side = order.getSide();
		
		ExecutionReport ackRep = new ExecutionReport(
				new OrderID(order.getClOrdID().getValue()), 
				new ExecID(order.getClOrdID().getValue() + genExecID()), 
				new ExecTransType(ExecTransType.STATUS), 
				new ExecType(ExecType.NEW), 
				new OrdStatus(OrdStatus.ACCEPTED_FOR_BIDDING), 
				order.getSymbol(), order.getSide(), 
				new LeavesQty(order.getOrderQty().getValue()), 
				new CumQty(0), 
				new AvgPx(0));
		
		ackRep.set(new Text("New order"));
		ackRep.set(new TransactTime(new Date()));
		
		try {
			this.trySendingMessage(ackRep);
		} catch (SessionNotFound e) {
			System.out.println("Ack send failed");
			e.printStackTrace();
		}
		
		// TODO: Connect to order book, and add/match as needed
		
		// TODO: Respond with fills as needed
		
	}
	
	private String genExecID() {
		int ret = this.execId;
		this.execId++;
		return String.valueOf(ret);
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
	
	public boolean trySendingMessage(Message mess) throws SessionNotFound {
		return Session.sendToTarget(mess, "EX", "CL");
	}

}