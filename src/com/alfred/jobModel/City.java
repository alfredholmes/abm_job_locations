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

	private double[] transportCosts = new double[0]; //vector of transport_costs

	private double area;

	private double industryMean = 0;
	private double industryVariance = 0;

	private double resource;

	public boolean updateConsumerMarkets = true;
	private double consumerMarkets = 0;

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
	
	
	public double getIndustryMean() {
		return industryMean;
	}
	
	public double getIndustryVariance() {
		return industryVariance;
	}

	public double transportCost(City c) {
		if(transportCosts.length == 0) refreshTransportCosts();
		return transportCosts[c.id];
	}

	public int get_id() {
		return id;
	}

	public double getResource() {
		return resource;
	}

	public void addAgent(Agent a) {

		agents.add(a);
		//calculate the industry mean and variance
		industryMean = (population * industryMean + a.getIndustry()) / (double)(population + 1);
		population++;
		industryVariance = calculateVariance();
		updateConsumerMarkets = true;
	}

	public void removeAgent(Agent a) {
		industryMean = population > 1 ? ((population * industryMean) - a.getIndustry()) / (double)(population - 1) : 0;
		population--;
		agents.remove(a);
		industryVariance = calculateVariance();
		updateConsumerMarkets = true;
	}

	public double populationSize() {
		int max_pop = 0;
		for(City c : cities) {
			if(c.population > max_pop) {
				max_pop = c.population;
			}
		}



		return (double)population / (double)max_pop;
	}

	public int getPopulation() {
		return population;
	}



	public int populationRank() {
		int pos = 1;

		for(City c : cities) {
			if(c.population > population) {
				pos++;
			}
		}

		return pos;
	}

	public double populationDensity() {
		return population / area;
	}

	public void refreshTransportCosts() {
		transportCosts = new double[cities.size()];
		for(City c : cities) {
			double distance = distance_to(c);
			transportCosts[c.get_id()] = Math.exp(- k * distance);
		}
	}

	public double get_consumer_market() {
		if(updateConsumerMarkets) {
			synchronized(this) {
				consumerMarkets = 0;
				for(City c : cities)
					consumerMarkets += transportCost(c) * c.population;
				}
			updateConsumerMarkets = false; //TODO: Think of a way to implement this cache with multiple Model instances and multiple threads
		}
		return consumerMarkets;
	}

	public double calculateVariance(){
		if(agents.size() < 2)
			return 0.0;

		double s = 0;
		for(Agent a : agents) {
			s += Math.pow(a.getIndustry() - industryMean, 2);
			
		
		}
		
		return s / (double)(agents.size() - 1);
	}
	public void setUpdateConsumerMarket(boolean value) {
		updateConsumerMarkets = value;
	}
	
	
	public void setResource(double resource) {
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
