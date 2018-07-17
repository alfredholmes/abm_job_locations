package com.alfred.jobModel;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class City {
	private int id;
	private int population = 0;
	private ArrayList<City> cities;
	private ArrayList<Agent> agents = new ArrayList<Agent>();
	public double[] location = new double[2];
	private static Random r;
	
	double[] transport_costs = new double[0]; //vector of transport_costs
	
	double area;
	boolean average_industry_cache = false;
	double last_average_industry = 0;
	
	double resource;
	
	public boolean update_consumer_markets = true;
	private ArrayList<Double> consumer_markets = new ArrayList();
	
	double k = 1.0 / 100.0; //parameter in transport costs - if k changes through time then could see better development of cities
	
	public static final int RADIUS = 6371; //not really relevant, could be put the parameter k, just a scaling factor but means distances are in KM
	
	public City(int id, ArrayList<City> cities) {
		if(r == null) {
			r = new Random();
			//r.setSeed(15);
			r.setSeed(0);
		}

		
		
		this.id = id;
		this.cities = cities;
		this.location[0] = r.nextDouble();
		this.location[1] = r.nextDouble();
		this.area = r.nextDouble();
		this.resource = r.nextDouble();
		//this.resource = 0.5;
	}
	

	public City(int id, ArrayList<City> cities, double lat, double lon, double area, double resource) {
		r = new Random();
		this.id = id;
		this.cities = cities;
		this.location[0] = lat;
		this.location[1] = lon;
		this.area = area;
		this.resource = resource;
	}
	
	public double distance_to(City city) {
		
		
		double lat_1 = (     location[0] / 180) * Math.PI;
		double lat_2 = (city.location[0] / 180) * Math.PI;
		
		double lon_1 = (     location[1] / 180) * Math.PI;
		double lon_2 = (city.location[1] / 180) * Math.PI;
		
		//latitude  - 0 -  PI (theta)
		//longitude - 0 - 2PI (phi)
		
		//find the cosine of the angle between the radial vectors by the dot product:
		
		double x1 = Math.cos(lon_1) * Math.sin(lat_1);
		double x2 = Math.cos(lon_2) * Math.sin(lat_2);
		
		double y1 = Math.sin(lon_1) * Math.sin(lat_1);
		double y2 = Math.sin(lon_2) * Math.sin(lat_2);
		
		double z1 = Math.cos(lat_1);
		double z2 = Math.cos(lat_2);
		
		
		double c_angle = (x1 * x2) + (y1 * y2) + (z1 * z2); //since vectors are of unit length
		return Math.abs(Math.acos(c_angle)) * RADIUS;
	}
	
	public double get_transport_cost_to(City c) {
		if(transport_costs.length < cities.size())
			refresh_transport_costs();
		return transport_costs[c.id];
	}
	
	public int get_id() {
		return id;
	}
	
	public double get_resource() {
		return resource;
	}
	
	public void add_agent(Agent a) {
		population++;
		agents.add(a);
		average_industry_cache = false;
		update_consumer_markets = true;
	}
	
	public void remove_agent(Agent a) {
		population--;
		agents.remove(a);
		average_industry_cache = false;
		update_consumer_markets = true;
	}
	
	public double population_size() {
		int max_pop = 0;
		for(City c : cities) {
			if(c.population > max_pop) {
				max_pop = c.population;
			}
		}
		
		
		
		return (double)population / (double)max_pop;
	}
	
	public int get_population() {
		return population;
	}
	
	public double average_industry() {
		if(average_industry_cache)
			return last_average_industry;
		
		double total_industry = 0;
		for(Agent a : agents) {
			total_industry += a.get_industry();
		}
		
		last_average_industry = population > 0 ? total_industry / population : 0;
		average_industry_cache = true;
		return last_average_industry;
	}
	
	public double industry_variance() {
		double m = average_industry();
		double s = 0;
		for(Agent a : agents) {
			//System.out.println(a.get_city().equals(this));
			s += Math.pow((a.get_industry() - m), 2);
		}
		//System.out.println(s);
		return agents.size() > 1 ? s / (agents.size() - 1) : 0;
		
	}
	
	public int population_rank() {
		int pos = 1;
		
		for(City c : cities) {
			if(c.population > population) {
				pos++;
			}
		}
		
		return pos;
	}
	
	public double population_density() {
		return population / area;
	}
	
	public void refresh_transport_costs() {
		transport_costs = new double[cities.size()];
		for(City c : cities) {
			double distance = distance_to(c);
			transport_costs[c.get_id()] = Math.exp(- k * distance);
		}
	}
	
	public double get_consumer_market(ArrayList<Agent> agents) {
		if(update_consumer_markets) {
			consumer_markets = new ArrayList<Double>();
			for(City c : cities) {
				double s = 0;
				for(Agent a : agents) {
					s += c.get_transport_cost_to(a.get_city());
				}
				consumer_markets.add(s);
			}
			update_consumer_markets = false; //TODO: Think of a way to implement this cache with multiple Model instances and multiple threads
		}
		return consumer_markets.get(id);
	}
	
	public void set_resource(double resource) {
		this.resource = resource;
	}
	
	
}
