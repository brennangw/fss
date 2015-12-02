import java.net.UnknownHostException;

import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.MongoClient;

public class Connect {

	public static void main(String[] args) throws UnknownHostException {
		// TODO Auto-generated method stub
		
		MongoClient mongoClient = new MongoClient( "localhost", 27017);
		
		DB db = mongoClient.getDB("myDB");
		DBCollection coll = db.getCollection("myCollection");
		
		for (int i=0; i < 100; i++) {
		    coll.insert(new BasicDBObject("i", i));
		}

	}

}
