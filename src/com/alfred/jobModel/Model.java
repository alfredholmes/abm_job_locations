package com.alfred.jobModel;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

import com.alfred.utility.CSVReader;

public class Model {
	public ArrayList<Agent> agents = new ArrayList<Agent>(); 
	public ArrayList<City> cities = new ArrayList<City>();	
	
	public Model(int n_agents) {
		
		//loading data
		
		CSVReader location_data = new CSVReader("data/Local_Authority_Districts_December_2017_Full_Clipped_Boundaries_in_Great_Britain.csv");
		CSVReader employment_data = new CSVReader("data/Employment_By_Local_Authority.csv");
	
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
			System.out.println(s);
			employment.add(Double.parseDouble(s) / 25.0);
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
			cities.add(new City(i, cities, lats.get(i), lons.get(i), areas.get(i)));
			String name = location_names_geographic.get(i);
			//get_id in employment column
			int j;
			for(j = 0; j < location_names_employment.size(); j++) {
				if(name.equals(location_names_employment.get(j)))
					break;
			}
			if(j != location_names_employment.size()) {
				for(int k = 0; k < employment.get(j); k++)
					agents.add(new Agent(cities.get(i)));
			}
		}
		
		
		

		//generate agents
		//for(int i = 0; i < n_agents; i++)
		//	agents.add(new Agent(cities));

		
	}
	
	public static void main(String[] argv) {
		
		long then = System.currentTimeMillis();
		double previous_moves = 0;
		Model m = new Model(1000);
		Plot p = new Plot(m, 0);
		//Plot q = new Plot(m, 1);
		for(int i = 0; i < 200; i++) {
			//m.dump_cities();
			m.update();
			
			double moves = m.average_number_of_moves();
			System.out.println("Step " + i + " " + moves + " "  + (moves - previous_moves));
			long now = System.currentTimeMillis();
			if(now - then > 1000) {
				then = now;
				p.draw();
				//q.draw();
			}
			previous_moves = moves;
			
			
		}
		m.dump_cities();
		
	}
	
	public void dump_cities() {
		for(City c: cities) {
			System.out.println(c.population_size() + " \t" + c.average_industry() + " \t" + Math.pow(c.industry_variance(), 0.5) + "\t " + transport_cost_to_largest_city(c));
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
		return capital.get_transport_cost_to(city);
	}
	
	public void update() {
		Map<Agent, City> movements = new HashMap<Agent, City>();
		for(Agent a : agents) {			
			movements.put(a, a.get_next_city(agents, cities));
		}
		//do the actual updates after all the agents have made their decisions
		for(Map.Entry<Agent, City> m : movements.entrySet()) {
			m.getKey().set_city(m.getValue());
		}
	}
}
