package com.alfred.jobModel;


import java.util.ArrayList;
import java.util.Random;

public class Agent {
	private double industry; //parameter whether to prefer being close to jobs of a similar industry or have cheap running costs
	private double consumerDependence; //parameter whether to care about being close to other jobs - irrespective of their industry - when connected to housing model, this will use people rather than job density
	private static double k = 10; //parameter for the activation function
	
	private double[] parameters; //weights used in the evaluation of cities	
	
	private City city; //current city
	public int moves = 0; //keep track of number of times agent has moved
	
	public Agent(ArrayList<City> cities, double[] parameters) {
		this(cities.get(new Random().nextInt(cities.size())), parameters);
	}
	
	public Agent(City city, double[] parameters) {
		this.parameters = parameters;
		Random r = new Random();
		industry = r.nextDouble();
		consumerDependence = 1.0 - industry;
		
		setCity(city);
	}
	
	public static double activation(double x) {
		return 1.0 / (1.0 + Math.exp(-x));
	}
	
	public double rating(ArrayList<City> cities, City city) {
		if(city.equals(this.city))
			return 0.0;
		
		double current_market    = 0;
		double potential_market  = 0;
		
		for(City c : cities) {
			double a = (c.getPopulation() - 1) * c.getIndustryVariance() + c.getPopulation() * (1.0 - Math.pow(c.getIndustryMean() - industry, 2));
			current_market   += a * this.city.transportCost(c);
			potential_market += a *      city.transportCost(c);
		}
		
		double consumer_market = this.city.getConsumerMarket();
		double potential_consumer_market = city.getConsumerMarket();
		
		double market_gain = potential_market / current_market;
		double consumer_gain = potential_consumer_market / consumer_market;
		double resource_match = (1.0 - Math.pow(city.getResource() - this.industry, 2)) / (1.0 - Math.pow(this.city.getResource() - this.industry, 2));
		
		double centripetal = parameters[0] * (1.0 - industry) * Math.log(market_gain) + parameters[1] * consumerDependence * Math.log(consumer_gain) + parameters[2] * (1.0 - consumerDependence) * Math.log(resource_match);
		
		double density_ratio = (0.5 + city.populationDensity()) / (0.5 + this.city.populationDensity());
		double immobility = (1.0 / this.city.transportCost(city));
		
		double centrifugal = industry * (parameters[3] * Math.log(density_ratio) + parameters[4] * Math.log(immobility));
		
		return centripetal - centrifugal;
	
	}
	
	public City getNextCity(ArrayList<City> cities) {
		if(cities.size() < 2)
			return null;
		
		
		Random rand = new Random();
		
		if(city == null) {
			setCity(cities.get((int)(rand.nextDouble() * cities.size()))); //if cities is empty then the program deserves to crash
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
	
	public void setCity(City c) {
		if (city == null || !city.equals(c)){
			if(city != null) {
				city.removeAgent(this);		
				moves++;
			}
			city = c;
			c.addAgent(this);
			
		}
	}
	
	public City getCity() {
		return city;
	}
	
	public double getIndustry() {
		return industry;
	}
}
