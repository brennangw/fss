package apps;

import java.sql.Connection;
import java.sql.DriverManager;
import java.util.Date;
import java.util.Random;

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
		System.out.println("Got new order message.");
		System.out.println("Sending ack.");
		ExecutionReport ackRep = new ExecutionReport(
				new OrderID(order.getClOrdID().getValue()), 
				this.genExecID(order), 
				new ExecTransType(ExecTransType.STATUS), 
				new ExecType(ExecType.NEW),
				new OrdStatus(OrdStatus.ACCEPTED_FOR_BIDDING), 
				order.getSymbol(), 
				order.getSide(), 
				new LeavesQty(order.getOrderQty().getValue()), 
				new CumQty(0),
				new AvgPx(0));
		
		ackRep.set(order.getClOrdID());
		ackRep.set(new Text("New order"));
		ackRep.set(new TransactTime(new Date()));
		
		try {
			this.trySendingMessage(ackRep);
		} catch (SessionNotFound e) {
			System.out.println("Ack send failed.");
			e.printStackTrace();
		}
		
		// TODO: Connect to order book, and add/match as needed, and send fills when there is a match
		
		/*
		 *  Sending a partial and a full fill for now
		 */
		
		int orderSize = (int) Math.floor(order.getPrice().getValue());
		Random randGenerator = new Random();
		int low = 1;
		
		// Partial fill
		System.out.println("Sending partial fill.");
		double priceMatchForPartialFill = order.getPrice().getValue();
		double quantitiyForPartialFill = (double) randGenerator.nextInt(orderSize - low) + low;
		ExecutionReport testPartialFill = new ExecutionReport(
				new OrderID(order.getClOrdID().getValue()),
				this.genExecID(order),
				new ExecTransType(ExecTransType.NEW),
				new ExecType(ExecType.PARTIAL_FILL),
				new OrdStatus(OrdStatus.PARTIALLY_FILLED),
				order.getSymbol(),
				order.getSide(),
				new LeavesQty(0),
				new CumQty(quantitiyForPartialFill),
				new AvgPx(priceMatchForPartialFill));
		
		testPartialFill.set(new LastShares(order.getOrderQty().getValue()));
		testPartialFill.set(order.getClOrdID());
		testPartialFill.set(new TransactTime(new Date()));
		testPartialFill.set(new LastPx(priceMatchForPartialFill));
		
		try {
			this.trySendingMessage(testPartialFill);
		} catch (SessionNotFound e) {
			System.out.println("Fill send failed.");
			e.printStackTrace();
		}
		
		// Full fill
		System.out.println("Sending full fill.");
		double priceMatchForFullFill = order.getPrice().getValue() - 0.5;
		double quantityForFullFill = orderSize - quantitiyForPartialFill;
		ExecutionReport testFullFill = new ExecutionReport(
				new OrderID(order.getClOrdID().getValue()),
				this.genExecID(order),
				new ExecTransType(ExecTransType.NEW),
				new ExecType(ExecType.FILL),
				new OrdStatus(OrdStatus.FILLED),
				order.getSymbol(),
				order.getSide(),
				new LeavesQty(0),
				new CumQty(quantityForFullFill),
				new AvgPx(priceMatchForFullFill));
		
		testFullFill.set(new LastShares(order.getOrderQty().getValue()));
		testFullFill.set(order.getClOrdID());
		testFullFill.set(new TransactTime(new Date()));
		testFullFill.set(new LastPx(priceMatchForFullFill));
		
		try {
			this.trySendingMessage(testPartialFill);
		} catch (SessionNotFound e) {
			System.out.println("Fill send failed.");
			e.printStackTrace();
		}
	}
	
	private ExecID genExecID(NewOrderSingle order) throws FieldNotFound {
		int ret = this.execId;
		this.execId++;
		return new ExecID(order.getClOrdID().getValue() + " " + String.valueOf(ret));
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
