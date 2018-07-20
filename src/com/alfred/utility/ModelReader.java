package com.alfred.utility;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

import com.alfred.jobModel.Model;

public class ModelReader {
	public static Model get_from_file(String filename) {
		BufferedReader br = null;
		FileReader fr = null;
		
		double[] agent_params;
		double[] city_params;
		
		ArrayList<String[]> data = new ArrayList<String[]>();
		
		Model m;
		
		try {
			fr = new FileReader(filename);
			br = new BufferedReader(fr);
			
			String current_line;
		
		
			
		
			while((current_line = br.readLine()) != null) {
				String[] line_data = current_line.split(",");
				int i = 0;

				data.add(line_data);
			}
			
			agent_params = new double[data.get(0).length];
			city_params = new double[data.get(1).length];
			
			for(int i = 0; i < agent_params.length; i++){
				agent_params[i] = Double.parseDouble(data.get(0)[i]);
			}
			
			for(int i = 0; i < city_params.length; i++) {
				city_params[i] = Double.parseDouble(data.get(1)[i]);
			}
			m = new Model(agent_params, city_params);
			
				
			
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		} finally {
			try {
				if(br != null)
					br.close();
				if(fr != null)
					fr.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return m;
	}
}
