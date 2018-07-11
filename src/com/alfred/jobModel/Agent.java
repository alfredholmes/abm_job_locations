package com.alfred.jobModel;


import java.util.ArrayList;
import java.util.Random;

public class Agent {
	private double industry;
	private double consumer_dependence;
	private double k = 1; //parameter for the activation function
	private double a = 1; //immobility factor
	private double b = 1; //centripetal vs centrifugal 
	
	
	//private double target;
	private City city;
	int moves = 0;
	
	public Agent(ArrayList<City> cities) {
		Random r = new Random();
		industry = r.nextDouble();
		//consumer_dependence = (1.0 - industry);
		//consumer_dependence = industry;
		//consumer_dependence = industry + r.nextGaussian() * 0.01;
		consumer_dependence = r.nextDouble();
		city = cities.get((int)(cities.size() * r.nextDouble()));
		city.add_agent(industry);
		
	}
	
	public double activation(double x) {
		return 1.0 / (1.0 + Math.exp(-x));
	}
	
	public double rating(ArrayList<Agent> agents, City city, double[][] transport_costs) {
		if(city.equals(this.city))
			return 0.0;
		
		double current_market   = 0;
		double potential_market = 0;
		double consumer_market   = 0;
		double potential_consumer_market = 0;
		
		for(Agent a : agents) {
			double industry_difference = Math.pow(industry - a.industry, 2);
			current_market   += transport_costs[a.city.get_id()][this.city.get_id()] * (1.0 - industry_difference);
			potential_market += transport_costs[a.city.get_id()][city.get_id()] * (1.0 - industry_difference);
			
			consumer_market  += transport_costs[a.city.get_id()][this.city.get_id()];
			potential_consumer_market += transport_costs[a.city.get_id()][this.city.get_id()];
		}
		
		
		
		double market_gain   = potential_market / current_market;
		double consumer_gain = potential_consumer_market / consumer_market;
		
		double centripetal = (1.0 - industry) * Math.log(market_gain) + consumer_dependence * Math.log(consumer_gain);
		
		double rent_ratio = (0.5 + city.population_rank()) / (0.5 + this.city.population_rank()); //will use the actual rents in the housing model
		double immobility = a * (1.0 - transport_costs[city.get_id()][this.city.get_id()]);
		
		double centrifugal = industry * (Math.log(rent_ratio) + immobility);
		
		return b * centripetal - centrifugal;
		//return (1.0 - industry) * Math.log(market_gain) - (industry) * Math.log(rent_ratio) + consumer_dependence * Math.log(consumer_gain);
	}
	
	public City get_next_city(ArrayList<Agent> agents, ArrayList<City> cities, double[][] transport_costs) {
		Random rand = new Random();
		
		
		
		if(city == null) {
			set_city(cities.get((int)(rand.nextDouble() * cities.size()))); //if cities is empty then the program deserves to crash
		}
		City best = city;
		double current_rating = 0.0;
		double best_rating = current_rating;
		for(City c: cities) {
			double r = rating(agents, c, transport_costs);
			if(r > best_rating) {
				best = c;
				best_rating = r;
			}
		}
		//System.out.println(best_rating - current_rating);
		if(rand.nextDouble() < activation(k * (best_rating - current_rating))) {
			return city; //don't move
		}else {
			return best; //move
		}
	}
	
	public void set_city(City c) {
		if (city.equals(c))
			return;
		city.remove_agent(industry);
		city = c;
		c.add_agent(industry);
		moves++;
	}
	
	public City get_city() {
		return city;
	}
	
	public double get_industry() {
		return industry;
	}
}
