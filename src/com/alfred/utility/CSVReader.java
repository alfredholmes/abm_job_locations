package com.alfred.utility;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class CSVReader {
	private String path;
	private ArrayList<Map<String, String>> data = new ArrayList<Map<String, String>>();
	public CSVReader(String path) {
		this.path = path;
		
		BufferedReader br = null;
		FileReader fr = null;
		
		try {
			fr = new FileReader(path);
			br = new BufferedReader(fr);
			
			String current_line;
			String[] header = null;
		
		
			
		
			while((current_line = br.readLine()) != null) {
				if(header == null) {
					header = current_line.split(",");
				}else {
					Map<String, String> line = new HashMap<String, String>();
					String[] line_data = current_line.split(",");
					int i = 0;
					for(String s : header) {
						//System.out.println(line_data[i]);
						line.put(s, line_data[i++]);
						
					}
					data.add(line);
				}
				
			//System.out.println(data);
			}
		} catch (IOException e) {
			e.printStackTrace();
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
	}
	
	public Map<String, String> get_row(int i) {
		if(i < data.size()) {
			return data.get(i);
		}else {
			return null;
		}
	}
	
	public ArrayList<String> get_column(String head){
		ArrayList<String> r = new ArrayList<String>();
		for(Map<String, String> line : data) {
			r.add(line.get(head));
		}
		
		return r;
	}
	
	public int get_num_rows() {
		return data.size();
	}
}
