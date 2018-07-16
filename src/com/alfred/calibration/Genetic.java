package com.alfred.calibration;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

import com.alfred.jobModel.Model;
import com.alfred.utility.CSVReader;;

public class Genetic {
	public ArrayList<Model> models = new ArrayList<Model>();
	Random rng = new Random();
	
	public double[][] target;
	int n_cities;
	int n_models = 100;
	int top_model;
	
	public Genetic() {
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
			
			double[] agent_params = new double[4];
			for(int j = 0; j < agent_params.length; j++) {
				agent_params[j] = rng.nextDouble();
			}
			
			double[] city_params = new double[n_cities];
			
			for(int j = 0; j < city_params.length; j++) {
				city_params[j] = rng.nextDouble();
			}
			
			models.add(new Model(agent_params, city_params));
		}
		
	}
	
	private double fitness(Model m) {
		m = new Model(m.agent_parameters, m.city_parameters);
		double error = 0;
		for(int i = 1; i < target.length; i++) {
			double[] output = m.update();
			for(int j = 0; j < target[i].length; j++) {
				error += Math.pow(output[j] - target[i][j], 2);
			}
		}
		//System.out.println(error);
		return error;
	}
	
	public double update() {
		//get array of fitness values
		double[] fitness_values = new double[models.size()];
		double average_error = 0;
		
		top_model = 0;
		double top_model_fitness = -1;
		for(int i = 0; i < models.size(); i++) {
			System.out.println("\t Evaluating fitness of model " + i);
			fitness_values[i] = fitness(models.get(i));
			if(top_model == 0) {
				top_model_fitness = fitness_values[0];
			}else if(fitness_values[i] < top_model_fitness) {
				top_model = i;
				top_model_fitness = fitness_values[i];
			}	
		}
		
		for(double v : fitness_values) 
			average_error += v;
		
		average_error /= (double)fitness_values.length;
		
		double[] f = new double[fitness_values.length];
		System.arraycopy(fitness_values, 0, f, 0, fitness_values.length);
		Arrays.sort(f);
		
		double median = f[(fitness_values.length + 1) / 2];
		
		ArrayList<Integer> new_parent_ids = new ArrayList<Integer>();
		
		for(int i = 0; i < fitness_values.length; i++) {
			if(fitness_values[i] > median) {
				fitness_values[i] = -1;
			}else {
				new_parent_ids.add(i);
			}
		}
		
		for(int i = 0; i < fitness_values.length; i++) {
			if(fitness_values[i] == -1) {
				
				//make new model
				Model parent1 = models.get(new_parent_ids.get(rng.nextInt(new_parent_ids.size())));
				Model parent2 = models.get(new_parent_ids.get(rng.nextInt(new_parent_ids.size())));
				
				double[] agent_params = new double[4];
				double[] city_params = new double[n_cities];
				
				for(int j = 0; j < agent_params.length; j++) {
					double r = 1.5 * rng.nextDouble();
					agent_params[j] = r * parent1.agent_parameters[j] + (1.0 - r) * parent2.agent_parameters[j];
				}
				
				for(int j = 0; j < city_params.length; j++) {
					double r = rng.nextDouble();
					city_params[j] = r * parent1.city_parameters[j] + (1.0 - r) * parent2.city_parameters[j];
					
				}
				
				
				models.set(i, new Model(agent_params, city_params));
			}
		
		}
		
		return average_error;
	}
	
	public static void run(String[] argv) {
		//Generate population
		System.out.println("Generating population...");
		Genetic g = new Genetic();
		for(int i = 0; i < 5; i++) {
			System.out.println("Running generation " + i);
			double average_error = g.update();
			System.out.println(average_error);
		}
		//print top parameters (lol)
		
		//System.out.println();
		for(int i = 0; i < g.models.get(g.top_model).agent_parameters.length; i++) {
			System.out.println(g.models.get(g.top_model).agent_parameters[i]);
		}
	}
}
