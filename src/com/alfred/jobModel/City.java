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
	
	double industry_step = 0.01;
	
	Map<Double, Map<City, Map<City, Double>>> cache = new HashMap<Double, Map<City, Map<City, Double>>>();
	
	double k = 1.0 / 50; //parameter in transport costs - if k changes through time then could see better development of cities
	
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
		//location[0] = r.nextGaussian() * 0.15 + 0.5;
		//location[1] = r.nextGaussian() * 0.15 + 0.5;
		//this(id, cities, lat, lon);
	}
	

	public City(int id, ArrayList<City> cities, double lat, double lon, double area) {
		this.id = id;
		this.cities = cities;
		this.location[0] = lat;
		this.location[1] = lon;
		this.area = area;
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
	
	public void add_agent(Agent a) {
		population++;
		agents.add(a);
		average_industry_cache = false;
	}
	
	public void remove_agent(Agent a) {
		population--;
		agents.remove(a);
		average_industry_cache = false;
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
		return s / (agents.size() - 1);
		
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
		for(int i = 0; i < cities.size(); i++) {
			double distance = distance_to(cities.get(i));
			transport_costs[i] = Math.exp(- k * distance);
		}
	}
	
	public boolean cached(double industry, City c1, City c2) {
		industry = industry_step * (int)(industry / industry_step);
		
		if(cache.containsKey(industry)) {
			if(cache.get(industry).containsKey(c1)) {
				if(cache.get(industry).get(c1).containsKey(c2)) {
					return true;
				}
			}else if(cache.get(industry).containsKey(c2)) {
				if(cache.get(industry).get(c2).containsKey(c1)) {
					return true;
				}
			}
		}
		return false;
	}
	
	public double get_from_cache(double industry, City c1, City c2) {
		industry = industry_step * (int)(industry / industry_step);
		
		if(cache.containsKey(industry)) {
			if(cache.get(industry).containsKey(c1)) {
				if(cache.get(industry).get(c1).containsKey(c2)) {
					return cache.get(industry).get(c1).get(c2);
				}
			}else if(cache.get(industry).containsKey(c2)) {
				if(cache.get(industry).get(c2).containsKey(c1)) {
					return 1.0 / cache.get(industry).get(c2).get(c1);
				}
			}
		}
		return -1; //not found
	}

	public void   store_in_cache(double value, double industry, City c1, City c2) {
		industry = industry_step * (int)(industry / industry_step); //could be error prone since values could vary up to 2 * industry_step
		
		if(cache.containsKey(industry)) {
			if(cache.get(industry).containsKey(c1)) {
				cache.get(industry).get(c1).put(c2, value);
			}else {
				Map<City, Double> m = new HashMap<City, Double>();
				m.put(c2, value);
				cache.get(industry).put(c1, m);
			}
		}else {
			Map<City, Double> m = new HashMap<City, Double>();
			Map<City, Map<City, Double>> n = new HashMap<City, Map<City, Double>>();
			m.put(c2, value);
			n.put(c1, m);
			cache.put(industry, n);
		}
	}
	
	public void clear_cache() {
		cache = new HashMap<Double, Map<City, Map<City, Double>>>();
	}
	

	
	
	
	
}
