package dstm.dstm2py;

import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Vector;

import org.eclipse.emf.common.util.EList;
import DSTM4Rail.DSTM;

public class DSTM2PyDSTM {
	
	private DSTM model;
	
	private Hashtable<String,String> params;
	
	private Vector<String> transitions;
	
	private Vector<String> inbound;
	
	private Vector<String> outbound;
	
	private Vector<String> observations;
	
	private Vector<String> variables;

	private String initialState;

	private Vector<String> statistics;

	private Vector<String> events;
	
	public DSTM2PyDSTM(DSTM mdl) {
		this.model = mdl;
		this.params = new Hashtable<String,String>();
		this.transitions = new Vector<String>();
		this.inbound = new Vector<String>();
		this.outbound = new Vector<String>();
		this.observations = new Vector<String>();
		this.variables = new Vector<String>();
		this.statistics = new Vector<String>();
		this.events = new Vector<String>();
	}
	
	private String writevector(String header, Vector<String> payload, String prefix) {
		String retval = "";
		retval += "[" + header + "]\n";
		for (int i=0; i<payload.size(); i++) {
			retval += prefix + "_" + i + ": " + payload.elementAt(i) + "\n";
		}
		return retval;
	}
	
	private String flush() {
		String retval = "";
		retval += "[Main]\n";
		Enumeration<String> keys = this.params.keys();
		while (keys.hasMoreElements()) {
			String key = keys.nextElement();
			retval += key + ": " + this.params.get(key) + "\n";
		}
		retval += "[States]\n";
		retval += "initial: " + this.initialState + "\n";
		retval += this.writevector("Transitions",this.transitions,"t");
		retval += this.writevector("Inbound",this.inbound,"ich");
		retval += this.writevector("Outbound",this.outbound,"och");
		retval += this.writevector("Variables",this.variables,"v");
		retval += this.writevector("Observations",this.observations,"o");
		retval += this.writevector("Statistics",this.statistics,"s");
		retval += this.writevector("Events",this.events,"e");
		return retval;
	}


	private void extractFeatures() {
		this.
		
	}

	public String translate() {
		this.extractFeatures();
		return this.flush();
	}
}