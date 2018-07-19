package com.alfred.jobModel;

import java.util.ArrayList;
import java.util.Random;

public class City {


	
	private int id;
	private int population = 0;
	private ArrayList<City> cities;
	private ArrayList<Agent> agents = new ArrayList<Agent>();
	public double[] location = new double[2];
	private static Random r;

	private double[] transport_costs = new double[0]; //vector of transport_costs

	private double area;

	private double industry_mean = 0;
	private double industry_variance = 0;

	private double resource;

	public boolean update_consumer_markets = true;
	private double consumer_markets = 0;

	private double k = 1.0 / 100.0; //parameter in transport costs - if k changes through time then could see better development of cities

	public static final int RADIUS = 6371; //not really relevant, could be put the parameter k, just a scaling factor but means distances are in KM




	public City(int id, ArrayList<City> cities, double lat, double lon, double area, double resource) {
		this.id = id;
		this.cities = cities;
		this.location[0] = lat;
		this.location[1] = lon;
		this.area = area;
		this.resource = resource;

		if(r == null) r = new Random(); //initialise the static rand

	}
	//If randomly generating cities, use this method
	public City(int id, ArrayList<City> cities) {
		this(id, cities, new Random().nextDouble(), new Random().nextDouble(), new Random().nextDouble(), new Random().nextDouble());
	}
	
	
	public double get_industry_mean() {
		return industry_mean;
	}
	
	public double get_industry_variance() {
		return industry_variance;
	}

	public double transport_cost_to(City c) {
		if(transport_costs.length == 0) refresh_transport_costs();
		return transport_costs[c.id];
	}

	public int get_id() {
		return id;
	}

	public double get_resource() {
		return resource;
	}

	public void add_agent(Agent a) {

		agents.add(a);
		//calculate the industry mean and variance
		industry_mean = (population * industry_mean + a.get_industry()) / (double)(population + 1);
		population++;
		industry_variance = calculate_variance();
		update_consumer_markets = true;
	}

	public void remove_agent(Agent a) {
		industry_mean = population > 1 ? ((population * industry_mean) - a.get_industry()) / (double)(population - 1) : 0;
		population--;
		agents.remove(a);
		industry_variance = calculate_variance();
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

	public double industry_mean() {
		return industry_mean;
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

	public double get_consumer_market() {
		if(update_consumer_markets) {
			synchronized(this) {
				consumer_markets = 0;
				for(City c : cities)
					consumer_markets += transport_cost_to(c) * c.population;
				}
			update_consumer_markets = false; //TODO: Think of a way to implement this cache with multiple Model instances and multiple threads
		}
		return consumer_markets;
	}

	public double calculate_variance(){
		if(agents.size() < 2)
			return 0.0;

		double s = 0;
		for(Agent a : agents) {
			s += Math.pow(a.get_industry() - industry_mean, 2);
			
		
		}
		
		return s / (double)(agents.size() - 1);
	}
	public void set_update_consumer_market(boolean value) {
		update_consumer_markets = value;
	}
	
	
	public void set_resource(double resource) {
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


}
