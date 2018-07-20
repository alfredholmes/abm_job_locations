package com.alfred.controller;


import com.alfred.calibration.Genetic;
import com.alfred.jobModel.Model;
import com.alfred.utility.ModelReader;

public class Controller {
	public static boolean train = false;
	public static void main(String[] argv) {
		if(train) {
			Genetic.run(argv);
		} else {
			Model m = ModelReader.get_from_file("config/optimal.model");
			Model.run(argv, m.agentParameters, m.cityParameters);
		}
	}
}
