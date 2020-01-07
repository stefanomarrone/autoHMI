package org.prgmdl.sgml;

import SmartHomeMM.EnergyUnit;
import datatype.Energy;
import datatype.EnergyPeriod;
import datatype.Fare;
import datatype.FarePeriod;
import datatype.Period;

public class Utils {

	public static double computeEnergy(Energy e) {
		double corr = 1;
		if (e.getUnit() == EnergyUnit.W) {
			corr = 0.001;
		} else if (e.getUnit() == EnergyUnit.MW) {
			corr = 1000;
		}
		double retval = e.getEnergy() * corr;
		return retval;
	}
	
	public static int computeMinutes(String time) {
		int index = time.indexOf(":");
		int len = time.length();
		String tmp = time.substring(index+1,len);
		int retval = new Integer(tmp);
		tmp = time.substring(0,index);
		retval += new Integer(tmp) * 60;
		return retval;
	}
	
	public static double getEnergy(EnergyPeriod ep) {
		Energy e = ep.getEnergy();
		return Utils.computeEnergy(e);
	}

	public static double getTimePeriod(EnergyPeriod ep) {
		return Utils.getTimePeriod(ep.getPeriod());
	}

	public static double getTimePeriod(FarePeriod fp) {
		return Utils.getTimePeriod(fp.getPeriod());
	}
	
	private static double getTimePeriod(Period p) {
		int startMin = Utils.computeMinutes(p.getStartTime());
		int endMin = Utils.computeMinutes(p.getEndTime());
		return (endMin - startMin) / 60;
	}

	public static double getFare(FarePeriod fp) {
		Fare f = fp.getFare();
		return f.getFare();
	}
}