package com.alfred.calibration;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

import com.alfred.jobModel.Model;
import com.alfred.utility.CSVReader;
import com.alfred.utility.CSVWriter;
import com.alfred.utility.ModelReader;;

public class Genetic {
	public ArrayList<Model> models = new ArrayList<Model>();
	Random rng = new Random();
	
	public double[][] target;
	int nCities;
	int nModels = 100;
	int topModel;
	double topError = -1;
	
	private double[] fitnessCache;
	
	
	public Genetic(boolean restore) {
		
		ArrayList<CSVReader> csv_files = new ArrayList<CSVReader>();
		
		for(int i = 2012; i < 2017; i++) {
			csv_files.add(new CSVReader("resources/data/Employment_By_Local_Authority/" + i + ".csv"));
		}
		
		nCities = csv_files.get(0).getNRows();
		
		target = new double[csv_files.size()][nCities];
		
		for(int i = 0; i < csv_files.size(); i++) {
			ArrayList<String> employment = csv_files.get(i).getColumn("employment");
			for(int j = 0; j < employment.size(); j++) {
				target[i][j] = Double.parseDouble(employment.get(j));
			}
		}
		
		//generate models
		for(int i = 0; i  < nModels; i++) {
			if(!restore) {
				double[] agent_params = new double[5];
				for(int j = 0; j < agent_params.length; j++) {
					agent_params[j] = rng.nextDouble();
				}
				
				double[] city_params = new double[nCities];
				
				for(int j = 0; j < nCities; j++) {
					city_params[j] = rng.nextDouble();
				}
			
			
				models.add(new Model(agent_params, city_params));
			
			}else {
				//System.out.println("Here!");
				models.add(ModelReader.get_from_file("training/" + i + ".model"));
			}
		}
		
		
		fitnessCache = new double[nModels];
		for(int i = 0; i < fitnessCache.length; i++) fitnessCache[i] = -1;
		
	}
	
	private double fitness(Model m) {
		m = new Model(m.agentParameters, m.cityParameters);
		double error = 0;
		for(int i = 1; i < target.length; i++) {
			double[] output = m.update();
			for(int j = 0; j < target[i].length; j++) {
				error += Math.abs(output[j] - target[i][j]);
			}
		}
		
		return error;
	}
	

	
	public double update() {
		
		double[] fitness_values = new double[models.size()];
		
		for(int i = 0; i < fitness_values.length; i++) {
			System.out.print("\t Evaluating model " +  i + " ...");
			fitness_values[i] = fitness(models.get(i));
			System.out.println(" done");
		}
		
		
		double total_error = 0;
		double min_error = -1;
		for(int i = 0; i < fitness_values.length; i++) {
			double d = fitness_values[i];
			total_error += d;
			if(min_error == -1 || (d < min_error && d != 0)) {
				min_error = d;
				topModel = i;
			}
		}
		double average_error = total_error  / fitness_values.length;
		topError = min_error;
		
		
		
		double[] f = new double[fitness_values.length];
		System.arraycopy(fitness_values, 0, f, 0, fitness_values.length);
		Arrays.sort(f);
		
		double median = f[(fitness_values.length + 1) / 2];
		
		ArrayList<Integer> new_parent_ids = new ArrayList<Integer>();
		
		for(int i = 0; i < fitness_values.length; i++) {
			if(fitness_values[i] > median) {
				fitness_values[i] = -1;
			}else{
				new_parent_ids.add(i);
			}
		}
		
		for(int i = 0; i < fitness_values.length; i++) {
			if(fitness_values[i] == -1) {
				
				//make new model
				Model parent1 = models.get(new_parent_ids.get(rng.nextInt(new_parent_ids.size())));
				Model parent2 = models.get(new_parent_ids.get(rng.nextInt(new_parent_ids.size())));
				
				double[] agent_params = new double[5];
				double[] city_params = new double[nCities];
				
				for(int j = 0; j < agent_params.length; j++) {
					double r = rng.nextDouble();
					agent_params[j] = r * parent1.agentParameters[j] + (1.0 - r) * parent2.agentParameters[j];
				}
				
				for(int j = 0; j < city_params.length; j++) {
					double r = rng.nextDouble();
					city_params[j] = r * parent1.cityParameters[j] + (1.0 - r) * parent2.cityParameters[j];
					
				}
				
				fitnessCache[i] = -1;
				
				
				models.set(i, new Model(agent_params, city_params));
			}
		
		}
		
		return average_error;
	}
	
	public void saveState() {
		for(int i = 0; i < models.size(); i++) {
			//write file
			CSVWriter writer = new CSVWriter("training/" + i + ".model", false);
			writer.write(models.get(i).agentParameters);
			writer.write(models.get(i).cityParameters);
			writer.close();
		}
		
		CSVWriter writer = new CSVWriter("config/optimal.model", false);
		writer.write(models.get(topModel).agentParameters);
		writer.write(models.get(topModel).cityParameters);
	}
	
	
	
	public static void run(String[] argv) {
		//Generate population
		System.out.println("Generating population...");
		Genetic g = new Genetic(false);
		for(int i = 0; i < 4; i++) {
			System.out.println("Running generation " + i);
			double average_error = g.update();
			System.out.println(average_error + " " + g.topError);
			g.saveState();
		}
		
		
	}
}
