package com.alfred.jobModel;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class AgentDecisionRunnable implements Runnable {
	private ArrayList<Agent> agents;
	private ArrayList<City> cities;
	private Map<Agent, City> decisions = new HashMap<Agent, City>();
	private int start;
	private int end;

	AgentDecisionRunnable(ArrayList<Agent> agents, ArrayList<City> cities, int start, int end){
		this.agents = agents;
		this.cities = cities;
		this.start = start;
		this.end = end;
	}
	
	
	public void run() {
		for(int i = start; i < end; i++) {
			decisions.put(agents.get(i), agents.get(i).get_next_city(cities));
		}
	}
	
	public Map<Agent, City> getDecisions(){
		return decisions;
	}

}
