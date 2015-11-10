package main;

import quickfix.*;

import java.io.FileInputStream;

import apps.ExchangeSide;

public class ExchangeControl {

	Acceptor exchange;
	
	public ExchangeControl(String exchangeFile) {
		
	    Application application = new ExchangeSide();

	    try {
	    SessionSettings exchangeSettings = new SessionSettings(new FileInputStream(exchangeFile));
	    MessageStoreFactory exchangeStoreFactory = new FileStoreFactory(exchangeSettings);
	    LogFactory exchangeLogFactory = new FileLogFactory(exchangeSettings);
	    MessageFactory exchangeMessageFactory = new DefaultMessageFactory();
	    exchange = new SocketAcceptor
	      (application, exchangeStoreFactory, exchangeSettings, exchangeLogFactory, exchangeMessageFactory);
	    
	    exchange.start();
	    
	    } catch(Exception e) {
	    	e.printStackTrace();
	    }
	}
	
	public void stopExchange() {
		exchange.stop();
	}

}
