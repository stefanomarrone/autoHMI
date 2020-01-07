package org.prgmdl.sgml;

public class TimeCostPlace {
	
	private double cost;
	
	private double time;
	
	private String placename;

	public TimeCostPlace(double c, double t, String p) {
		this.cost = c;
		this.time = t;
		this.placename = p;
	}
	
	public TimeCostPlace(double c, double t) {
		this.cost = c;
		this.time = t;
		this.placename = null;
	}

	public double getCost() {
		return this.cost;
	}
	
	public double getTime() {
		return this.time;
	}

	public String getPName() {
		return this.placename;
	}

	public void setPName(String p) {
		this.placename = p;
	}
}