package com.alfred.jobModel;


import java.util.ArrayList;
import java.util.Random;

public class Agent {
	private double industry;
	private double consumer_dependence;
	private double k = 10; //parameter for the activation function
	
	private double a = 1; //industry
	private double b = 1; //consumer
	private double c = 1; //rent / population density
	private double d = 1; //immobility
	
	//private double target;
	private City city;
	int moves = 0;
	
	public Agent(ArrayList<City> cities) {
		Random r = new Random();
		industry = r.nextDouble();
		
		consumer_dependence = 1.0 - industry;
		
		//consumer_dependence = r.nextDouble();
		
		city = cities.get((int)(cities.size() * r.nextDouble()));
		city.add_agent(this);
		
	}
	
	public Agent(City city) {
		Random r = new Random();
		
		industry = r.nextDouble();
		consumer_dependence = 1.0 - industry;
		
		//consumer_dependence = r.nextDouble();
		this.city = city;
		city.add_agent(this);
	}
	
	public double activation(double x) {
		return 1.0 / (1.0 + Math.exp(-x));
	}
	
	public double rating(ArrayList<Agent> agents, City city) {
		if(city.equals(this.city))
			return 0.0;
		
		double current_market   = 0;
		double potential_market = 0;
		double consumer_market   = 0;
		double potential_consumer_market = 0;
		
		for(Agent a : agents) {
			double industry_difference = Math.abs(industry - a.industry);
			current_market   += this.city.get_transport_cost_to(a.city) * (1.0 - industry_difference);
			potential_market +=      city.get_transport_cost_to(a.city) * (1.0 - industry_difference);
				
			consumer_market      += this.city.get_transport_cost_to(a.city);
			potential_consumer_market += city.get_transport_cost_to(a.city);
		}
		
		double market_gain   = potential_market / current_market;
		double consumer_gain = potential_consumer_market / consumer_market;
		
		double centripetal = a * (1.0 - industry) * Math.log(market_gain) + b * consumer_dependence * Math.log(consumer_gain);
		
		double rent_ratio = (0.5 + city.population_size()) / (0.5 + this.city.population_size()); //will use the actual rents in the housing model
		double density_ratio = (0.5 + city.population_density()) / (0.5 + this.city.population_density());
		double immobility = (1.0 / this.city.get_transport_cost_to(city));
		
		double centrifugal = industry * (/*c * Math.log(rent_ratio)*/ + c * Math.log(density_ratio)) +  d * Math.log(immobility);
		
		
		return centripetal - centrifugal;
		//return (1.0 - industry) * Math.log(market_gain) - (industry) * Math.log(rent_ratio) + consumer_dependence * Math.log(consumer_gain);
	}
	
	public City get_next_city(ArrayList<Agent> agents, ArrayList<City> cities) {
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
		}else {
			best = cities.get(0);
		}
		double best_rating = rating(agents, best);
		for(City c : cities) {
			if(!c.equals(city)) {
				double r = rating(agents, c);
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
		if (!city.equals(c)){
			city.remove_agent(this);		
			city = c;
			c.add_agent(this);
			moves++;
		}
	}
	
	public City get_city() {
		return city;
	}
	
	public double get_industry() {
		return industry;
	}
}
