package org.prgmdl.sgml;

import org.eclipse.emf.common.util.EList;
import org.prgmdl.formalism.utils.LabelGenerator;
import org.prgmdl.fspn.model.Arc;
import org.prgmdl.fspn.model.DiscreteArc;
import org.prgmdl.fspn.model.FSPN;
import org.prgmdl.fspn.model.OrdinaryPlace;
import org.prgmdl.fspn.model.Place;
import org.prgmdl.fspn.model.StoTransition;
import org.prgmdl.fspn.model.Transition;

import datatype.FarePeriod;

public abstract class FarePeriodFacade {
	
	protected String costfunction;
	
	protected String qtyString;
		
	protected TimeCostPlace[] tcp;
	
	public FarePeriodFacade(EList<FarePeriod> fares, FSPN net) {
		this.setQtyString();
		this.extractTC(fares);
		this.genNetwork(net,fares.size());
		this.computeFunction();
	}

	protected abstract void setQtyString();
	
	private void genNetwork(FSPN net, int size) {
    	Place first = null;
    	Transition prec = null;
		for (int i = 0; i < size; i++) {
			int mark = (i == 0) ? 1 : 0;
	    	Place p = new OrdinaryPlace(LabelGenerator.get("p"),mark); net.add(p);
	    	double rate = this.tcp[i].getTime();
			Transition t = new StoTransition(LabelGenerator.get("t"),rate); net.add(t);
	        Arc a = new DiscreteArc(LabelGenerator.get("a"),p,t,1); net.add(a);
	        if (i > 0) {
		        Arc preca = new DiscreteArc(LabelGenerator.get("a"),prec,p,1); net.add(preca);
		        if (i == size-1) {
			        Arc fina = new DiscreteArc(LabelGenerator.get("a"),t,first,1); net.add(fina);		        	
		        }
	        } else {
	        	first = p;
	        }
	        prec = t;
	        this.tcp[i].setPName(p.getName());
		}
	}

	private void extractTC(EList<FarePeriod> fares) {
		int size = fares.size();
		this.tcp = new TimeCostPlace[size];
		for (int i = 0; i < size; i++) {
			FarePeriod fp = fares.get(i);
	    	double period = Utils.getTimePeriod(fp);
	    	double fare = Utils.getFare(fp);
	    	this.tcp[i] = new TimeCostPlace(fare,period);
		}
	}

	private void computeFunction() {
		int size = this.tcp.length;
		String assign = "" + this.tcp[0].getCost();
		for (int i=1; i<size; i++) {
			assign += "," + this.tcp[i].getPName() + "-0.5," + this.tcp[i].getCost() + ")";
			assign = "discont(" + assign;
		}
		this.costfunction = assign + "*" + this.qtyString;
	}

	public String getDeltaCost() {
		return this.costfunction;
	}
	
	public String getDeltaEnergy() {
		return this.qtyString;
	}
}