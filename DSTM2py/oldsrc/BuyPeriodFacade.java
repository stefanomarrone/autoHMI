package org.prgmdl.sgml;

import org.eclipse.emf.common.util.EList;
import org.prgmdl.fspn.model.FSPN;
import org.prgmdl.mgrimoire.common.Configuration;

import datatype.FarePeriod;

public class BuyPeriodFacade extends FarePeriodFacade {

	public BuyPeriodFacade(EList<FarePeriod> fares, FSPN net) {
		super(fares, net);
	}

	@Override
	protected void setQtyString() {
		Configuration conf = Configuration.getConfiguration();
		this.qtyString = "(" + conf.getStraightValue("balance") + ")";
	}
}