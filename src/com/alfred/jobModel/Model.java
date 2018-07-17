package com.alfred.jobModel;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

import com.alfred.utility.CSVReader;

public class Model {
	public ArrayList<Agent> agents = new ArrayList<Agent>(); 
	public ArrayList<City> cities = new ArrayList<City>();	
	public double[] agent_parameters;
	public double[] city_parameters;
	
	double jobs_per_agent = 50;
	
	
	public Model(double[] agent_parameters, double[] city_parameters) {
		
		this.agent_parameters = agent_parameters;
		this.city_parameters  = city_parameters;
		
		//loading data
		
		CSVReader location_data = new CSVReader("data/Local_Authority_Districts_December_2017_Full_Clipped_Boundaries_in_Great_Britain.csv");
		CSVReader employment_data = new CSVReader("data/Employment_By_Local_Authority/2012.csv");
	
		int n_cities = location_data.get_num_rows();
		
		ArrayList<Double> lats  = new ArrayList<Double>();
		ArrayList<Double> lons  = new ArrayList<Double>();
		ArrayList<Double> areas = new ArrayList<Double>();
		ArrayList<Double> employment = new ArrayList<Double>();
		
		ArrayList<String> lats_string  = location_data.get_column("lat" );
		ArrayList<String> lons_string  = location_data.get_column("long");
		ArrayList<String> areas_string = location_data.get_column("st_areashape");
		
		ArrayList<String> location_names_geographic = location_data.get_column("lad17nm"); 
		ArrayList<String> location_names_employment = employment_data.get_column("name");
		ArrayList<String> employment_string = employment_data.get_column("employment");
		
		
		
		for(String s : lats_string) {
			lats.add(Double.parseDouble(s));
		}
		
		for(String s : lons_string) {
			lons.add(Double.parseDouble(s));
		}
		
		for(String s : areas_string) {
			areas.add(Double.parseDouble(s));
		}
		
		for(String s : employment_string) {
			employment.add(Double.parseDouble(s) / jobs_per_agent);
		}
		
		 
		
		for(String s : location_names_geographic) {
			boolean found = false;
			for(String t : location_names_employment) {
				if(t.equals(s)) {
					found = true;	
				}
			}
			if(!found) {
				System.out.println(s);
				
			}
		}
		
		

		for(int i = 0; i < n_cities; i++) {
			cities.add(new City(i, cities, lats.get(i), lons.get(i), areas.get(i), city_parameters[i]));
			String name = location_names_geographic.get(i);
			//get_id in employment column
			int j;
			for(j = 0; j < location_names_employment.size(); j++) {
				if(name.equals(location_names_employment.get(j)))
					break;
			}
			if(j != location_names_employment.size()) {
				for(int k = 0; k < employment.get(j); k++)
					agents.add(new Agent(cities.get(i), agent_parameters));
			}
			
		}
		
	}
	
	public static void run(String[] argv, double[] agent_params, double[] city_params) {
		
		double previous_moves = 0;
		Model m = new Model(agent_params, city_params);
		Plot p = new Plot(m, 0);
		for(int i = 0; i < 200; i++) {
			m.update();
			double moves = m.average_number_of_moves();
			System.out.println("Step " + i + " " + moves + " "  + (moves - previous_moves));
			p.draw();
			previous_moves = moves;	
		}
		m.dump_cities();
		
	}
	
	public void dump_cities() {
		for(City c: cities) {
			System.out.println(c.population_size() + " \t" + c.get_industry_mean() + " \t" + Math.pow(c.get_industry_variance(), 0.5) + "\t " + transport_cost_to_largest_city(c));
		}
	}
	
	public double average_number_of_moves() {
		int sum = 0;
		for(Agent a : agents)
			sum += a.moves;
		return (double)sum / (double)agents.size();
	}
	
	public double transport_cost_to_largest_city(City city) {
		//find the largest city
		int max_pop = 0;
		City capital = null;
		for(City c : cities) {
			if (c.get_population() > max_pop) {
				max_pop = c.get_population();
				capital = c;
			}
		}
		return capital.transport_cost_to(city);
	}
	
	public double[] update() {
		
		Map<Agent, City> movements = new HashMap<Agent, City>();
		for(Agent a : agents) {			
			movements.put(a, a.get_next_city(cities));
		}
		//do the actual updates after all the agents have made their decisions
		for(Map.Entry<Agent, City> m : movements.entrySet()) {
			m.getKey().set_city(m.getValue());
		}
		
		double[] r = new double[cities.size()];
		for(int i = 0; i < r.length; i++) {
			r[i]= cities.get(i).get_population() * jobs_per_agent;
		}
		return r;
	}
}
