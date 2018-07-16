package com.alfred.controller;

import java.util.Random;

import com.alfred.calibration.Genetic;
import com.alfred.jobModel.Model;

public class Controller {
	public static boolean train = true;
	public static void main(String[] argv) {
		if(train) {
			Genetic.run(argv);
		} else {
			//TODO: configuration files
			double[] agent_params = {1, 1, 1, 10};
			double[] city_params = new double[380];
			
			Random r = new Random();
			
			for(int i = 0; i < 380; i++) {
				city_params[i] = r.nextDouble();
			}
			
			Model.run(argv, agent_params, city_params);
		}
	}
}
