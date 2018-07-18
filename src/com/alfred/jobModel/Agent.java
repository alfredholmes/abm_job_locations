package com.alfred.jobModel;


import java.util.ArrayList;
import java.util.Random;

public class Agent {
	private double industry; //parameter whether to prefer being close to jobs of a similar industry or have cheap running costs
	private double consumer_dependence; //parameter whether to care about being close to other jobs - irrespective of their industry
	private static double k = 10; //parameter for the activation function
	
	private double[] parameters; //weights in the evaluation function of 
	
	private City city; //current city
	int moves = 0; //keep track of number of times agent has moved
	
	public Agent(ArrayList<City> cities, double[] parameters) {
		this(cities.get(new Random().nextInt(cities.size())), parameters);
	}
	
	public Agent(City city, double[] parameters) {
		this.parameters = parameters;
		Random r = new Random();
		industry = r.nextDouble();
		consumer_dependence = 1.0 - industry;
		
		set_city(city);
	}
	
	public double activation(double x) {
		return 1.0 / (1.0 + Math.exp(-x));
	}
	
	public double rating(ArrayList<City> cities, City city) {
		if(city.equals(this.city))
			return 0.0;
		
		double current_market    = 0;
		double potential_market  = 0;
		
		for(City c : cities) {
			double a = c.get_population() * (1.0 - Math.abs(industry - c.get_industry_mean()));
			current_market   += a * this.city.transport_cost_to(c);
			potential_market += a *      city.transport_cost_to(c);
			//current_market += 1;
			//potential_market += 1;
		
		}
		
		double consumer_market = this.city.get_consumer_market();
		double potential_consumer_market = city.get_consumer_market();
		
		double market_gain = potential_market / current_market;
		double consumer_gain = potential_consumer_market / consumer_market;
		double resource_match = (1.0 - Math.pow(city.get_resource() - this.industry, 2)) / (1.0 - Math.pow(this.city.get_resource() - this.industry, 2));
		
		double centripetal = parameters[0] * (1.0 - industry) * Math.log(market_gain) + parameters[1] * consumer_dependence * Math.log(consumer_gain) + parameters[2] * (1.0 - consumer_dependence) * Math.log(resource_match);
		
		double density_ratio = (0.5 + city.population_density()) / (0.5 + this.city.population_density());
		double immobility = (1.0 / this.city.transport_cost_to(city));
		
		double centrifugal = industry * (parameters[3] * Math.log(density_ratio)) +  parameters[4] * Math.log(immobility);
		
		return centripetal - centrifugal;
	
	}
	
	public City get_next_city(ArrayList<City> cities) {
		if(cities.size() < 2)
			return null;
		
		
		Random rand = new Random();
		
		if(city == null) {
			set_city(cities.get((int)(rand.nextDouble() * cities.size()))); //if cities is empty then the program deserves to crash
		}
		
		
		City best;
		if(cities.get(0).equals(city))
		{
			best = cities.get(1);
		}else{
			best = cities.get(0);
		}
		double best_rating = rating(cities, best);
		for(City c : cities) {
			if(!c.equals(city)) {
				double r = rating(cities, c);
				if(r > best_rating) {
					best = c;
					best_rating = r;
					
				}
			}
		}
		
		if(rand.nextDouble() < activation(k * (best_rating)) && best_rating > -1000) {
			return best; //move
		}else {
			return city; //don't move
		}
	}
	
	public void set_city(City c) {
		if (city == null || !city.equals(c)){
			if(city != null) {
				city.remove_agent(this);		
				moves++;
			}
			city = c;
			c.add_agent(this);
			
		}
	}
	
	public City get_city() {
		return city;
	}
	
	public double get_industry() {
		return industry;
	}
}
