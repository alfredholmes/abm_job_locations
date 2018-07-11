package com.alfred.jobModel;

import java.util.ArrayList;
import java.util.Random;

public class City {
	private int id;
	private int population = 0;
	private ArrayList<City> cities;
	private double industry_total = 0; // for calculating average industry for clusters
	public double[] location = new double[2];
	private static Random r;
	
	public static final int RADIUS = 6371;
	
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
		//location[0] = r.nextGaussian() * 0.15 + 0.5;
		//location[1] = r.nextGaussian() * 0.15 + 0.5;
		//this(id, cities, lat, lon);
	}
	

	public City(int id, ArrayList<City> cities, double lat, double lon) {
		this.id = id;
		this.cities = cities;
		this.location[0] = lat;
		this.location[1] = lon;
	}
	
	public double distance_to(City city) {
		//double sq_distance = Math.pow(location[0] - city.location[0], 2) + Math.pow(location[1] - city.location[1], 2);
		//return Math.pow(sq_distance, 0.5);
		
		//convert to radians:
		double lat_1 = (     location[0] / 180) * Math.PI;
		double lat_2 = (city.location[0] / 180) * Math.PI;
		
		double lon_1 = (     location[1] / 180) * Math.PI;
		double lon_2 = (city.location[1] / 180) * Math.PI;
		
		//lat - 0 -  PI
		//lon - 0 - 2PI
		
		//find the cosine of the angle between the radial vectors by the dot product:
		
		double x1 = Math.cos(lon_1) * Math.sin(lat_1);
		double x2 = Math.cos(lon_2) * Math.sin(lat_2);
		
		double y1 = Math.sin(lon_1) * Math.sin(lat_1);
		double y2 = Math.sin(lon_2) * Math.sin(lat_2);
		
		double z1 = Math.cos(lat_1);
		double z2 = Math.cos(lat_2);
		
		
		double c_angle = (x1 * x2) + (y1 * y2) + (z1 * z2);
		//System.out.println(c_angle);
		return Math.abs(Math.acos(c_angle)) * RADIUS;
	}
	
	public int get_id() {
		return id;
	}
	
	public void add_agent(double industry) {
		population++;
		industry_total += industry;
	}
	
	public void remove_agent(double industry) {
		population--;
		industry_total -= industry;
	}
	
	public double population_rank() {
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
		return industry_total / population;
	}
	
	public double industry_variance(ArrayList<Agent> agents) {
		double m = average_industry();
		double s = 0;
		for(Agent a : agents) {
			//System.out.println(a.get_city().equals(this));
			if(a.get_city().equals(this)) {
				s += Math.pow((a.get_industry() - m), 2);
			}
		}
		//System.out.println(s);
		return s / (agents.size() - 1);
		
	}
	
	public int population_position() {
		int pos = 1;
		
		for(City c : cities) {
			if(c.population > population) {
				pos++;
			}
		}
		
		return pos;
	}
	

	
	
	
	
}
