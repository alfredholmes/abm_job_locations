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
	int n_cities;
	int n_models = 100;
	int top_model;
	double top_error = -1;
	
	private double[] fitness_cache;
	
	int n_cpus;
	
	public Genetic(boolean restore) {
		n_cpus = Runtime.getRuntime().availableProcessors();
		//n_cpus = 1;
		
		ArrayList<CSVReader> csv_files = new ArrayList<CSVReader>();
		
		for(int i = 2012; i < 2017; i++) {
			csv_files.add(new CSVReader("data/Employment_By_Local_Authority/" + i + ".csv"));
		}
		
		n_cities = csv_files.get(0).get_num_rows();
		
		target = new double[csv_files.size()][n_cities];
		
		for(int i = 0; i < csv_files.size(); i++) {
			ArrayList<String> employment = csv_files.get(i).get_column("employment");
			for(int j = 0; j < employment.size(); j++) {
				target[i][j] = Double.parseDouble(employment.get(j));
			}
		}
		
		//generate models
		for(int i = 0; i  < n_models; i++) {
			if(!restore) {
				double[] agent_params = new double[5];
				for(int j = 0; j < agent_params.length; j++) {
					agent_params[j] = rng.nextDouble();
				}
				
				double[] city_params = new double[n_cities];
				
				for(int j = 0; j < n_cities; j++) {
					city_params[j] = rng.nextDouble();
				}
			
			
				models.add(new Model(agent_params, city_params));
			
			}else {
				//System.out.println("Here!");
				models.add(ModelReader.get_from_file("traning/" + i + ".model"));
			}
		}
		
		
		fitness_cache = new double[n_models];
		for(int i = 0; i < fitness_cache.length; i++) fitness_cache[i] = -1;
		
	}
	

	
	public double update() {
		ArrayList<Thread> workers = new ArrayList<Thread>();
		
		double[] fitness_values = new double[models.size()];
		double average_error = 0;
		
		for(int i = 0; i < n_cpus; i++) {
			int start = (int)(i * (double)(models.size() / n_cpus));
			int end = (int)((i + 1) * (double)(models.size() / n_cpus));
			if(i == n_cpus - 1 && end != models.size())
				end = models.size();
			workers.add(new Thread(new ModelEvaluation(models, fitness_values, fitness_cache, target, start, end)));
		}
		
		for(Thread w : workers) {
			w.start();
		}
		
		

		try {
			for(Thread w : workers)
				w.join();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		double total_error = 0;
		double min_error = -1;
		for(int i = 0; i < fitness_values.length; i++) {
			double d = fitness_values[i];
			total_error += d;
			if(min_error == -1 || (d < min_error && d != 0)) {
				min_error = d;
				top_model = i;
				
			}
		}
		average_error = total_error  / fitness_values.length;
		top_error = min_error;
		
		
		
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
				double[] city_params = new double[n_cities];
				
				for(int j = 0; j < agent_params.length; j++) {
					double r = 10 * rng.nextDouble();
					agent_params[j] = r * parent1.agent_parameters[j] + (1.0 - r) * parent2.agent_parameters[j];
				}
				
				for(int j = 0; j < city_params.length; j++) {
					double r = rng.nextDouble();
					city_params[j] = r * parent1.city_parameters[j] + (1.0 - r) * parent2.city_parameters[j];
					city_params[j] = city_params[j] < 1 ? city_params[j] : 1;
					city_params[j] = city_params[j] > 0 ? city_params[j] : 0;
					
				}
				
				fitness_cache[i] = -1;
				
				
				models.set(i, new Model(agent_params, city_params));
			}
		
		}
		
		return average_error;
	}
	
	public void save_state() {
		for(int i = 0; i < models.size(); i++) {
			//write file
			CSVWriter writer = new CSVWriter("traning/" + i + ".model", false);
			writer.write(models.get(i).agent_parameters);
			writer.write(models.get(i).city_parameters);
			writer.close();
		}
		
		CSVWriter writer = new CSVWriter("config/optimal.model", false);
		writer.write(models.get(top_model).agent_parameters);
		writer.write(models.get(top_model).city_parameters);
	}
	
	
	
	public static void run(String[] argv) {
		//Generate population
		System.out.println("Generating population...");
		Genetic g = new Genetic(true);
		for(int i = 0; i < 20; i++) {
			System.out.println("Running generation " + i);
			double average_error = g.update();
			System.out.println(average_error + " " + g.top_error);
			g.save_state();
		}
		
		
	}
}
