package org.prgmdl.sgml;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Map;

import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceFactoryImpl;

import SmartHomeMM.Microgrid;
import SmartHomeMM.SmartHomeMMPackage;

public class SgmlDeserializer {

	public static String readDataFile(String pathfile){
		/*parsing of declarations*/
		String declarations = "";
		BufferedReader reader;
		try {
			reader = new BufferedReader(new FileReader(pathfile));
			String line = null;
			StringBuilder stringBuilder = new StringBuilder();
			while( ( line = reader.readLine() ) != null ) {
				stringBuilder.append(line);
			}
			declarations = stringBuilder.toString();
		} catch (FileNotFoundException e1) {
			e1.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return declarations;
	}
	
	public static Microgrid stringToModel(String modelString){
		File modelFile = null;
		SmartHomeMMPackage.eINSTANCE.eClass();
		Resource.Factory.Registry reg = Resource.Factory.Registry.INSTANCE;
		Map<String, Object> m = reg.getExtensionToFactoryMap();
		m.put("smarthomemm", new XMIResourceFactoryImpl());
		ResourceSet resSet = new ResourceSetImpl();
		try {
			modelFile = new File("tmp.smarthomemm");
			FileWriter fw = new FileWriter(modelFile);
			fw.write(modelString);
			fw.flush();
			fw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		Resource resource = resSet.getResource(URI.createFileURI(modelFile.getPath()), true);
		Microgrid retval = (Microgrid) resource.getContents().get(0);
		return retval;
	}
}
