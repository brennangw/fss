package web;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Date;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.json.simple.JSONObject;

import main.StartParties;
import quickfix.*;
import quickfix.field.*;


public class ClientServlet extends HttpServlet {

	@SuppressWarnings("unchecked")
	@Override
	protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
		PrintWriter pw = resp.getWriter();
		JSONObject ret = new JSONObject();
		
		try {
			String type = req.getParameter("type");
			char ordType;
			if(type.equals("limit"))
				ordType = OrdType.LIMIT;
			else if(type.equals("market"))
				ordType = OrdType.MARKET;
			else 
				ordType = OrdType.PEGGED;
			
			String buySell = req.getParameter("side");
			char side = (buySell == "buy" ? Side.BUY : Side.SELL);
			
			quickfix.fix42.NewOrderSingle mess = new quickfix.fix42.NewOrderSingle (
					new ClOrdID("321"),
					new HandlInst(HandlInst.MANUAL_ORDER),
					new Symbol(req.getParameter("symbol")),
					new Side(side),
					new TransactTime(new Date()), 
					new OrdType(ordType));
			
			mess.set(new Price(Double.parseDouble(req.getParameter("price"))));
			mess.set(new OrderQty(Double.parseDouble(req.getParameter("lots"))));
			
			if(StartParties.cl.trySendingMessage(mess))
				ret.put("status", "success");
			else
				ret.put("status", "failure, send function returned false");

		} catch(SessionNotFound e) {
			e.printStackTrace();
			ret.put("status", "failure, no session");
		}
		
		pw.write(ret.toJSONString());
	}

}
