package com.alfred.utility;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class CSVWriter {
   FileWriter fw;
   PrintWriter out;
	
	public CSVWriter(String filename, boolean overwrite){
		try {
			fw = new FileWriter(filename);
			out = new PrintWriter(fw);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void write(double[] data) {
		for(int i = 0; i < data.length; i++) {
			out.print(data[i]);
			if(i != data.length - 1)
				out.print(",");
			
		}
		out.println();
		out.flush();
	}
	
	public void close() {
		out.close();
		try {
			fw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
