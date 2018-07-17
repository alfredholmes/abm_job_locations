package com.alfred.calibration;

import java.util.ArrayList;

import com.alfred.jobModel.Model;

public class ModelEvaluation implements Runnable {
	ArrayList<Model> models;
	double[] fitness_values;
	double[] fitness_cache;
	double[][] target;
	
	int start, end;
	
	ModelEvaluation(ArrayList<Model> models, double[] fitness_values, double[] fitness_cache, double[][] target, int start, int end){
		this.models = models;
		this.fitness_values = fitness_values;
		this.fitness_cache = fitness_cache;
		this.target = target;
		this.start = start;
		this.end = end;
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
		
		return error;
	}
	
	
	public void run() {
		//evaluate the fitness of the required models
		for(int i = start; i < end; i++) {
			System.out.println("Evaluating model " + i);
			if(fitness_cache[i] == -1) {
				fitness_values[i] = fitness(models.get(i)); 
			}else {
				fitness_values[i] = fitness_cache[i];
			}
		}
		
	}

}
