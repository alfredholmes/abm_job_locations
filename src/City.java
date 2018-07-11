import java.util.ArrayList;
import java.util.Random;

public class City {
	private int id;
	private int population = 0;
	private ArrayList<City> cities;
	private double industry_total = 0; // for calculating average industry for clusters
	public double[] location = new double[2];
	private static Random r;
	
	public City(int id, ArrayList<City> cities) {
		if(r == null) {
			r = new Random();
			//r.setSeed(15);
			//r.setSeed(0);
		}
		this.id = id;
		this.cities = cities;
		
		
		location[0] = r.nextDouble();
		location[1] = r.nextDouble();
		//location[0] = r.nextGaussian() * 0.15 + 0.5;
		//location[1] = r.nextGaussian() * 0.15 + 0.5;
	}
	
	public double distance_to(City city) {
		double sq_distance = Math.pow(location[0] - city.location[0], 2) + Math.pow(location[1] - city.location[1], 2);
		return Math.pow(sq_distance, 0.5);
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
