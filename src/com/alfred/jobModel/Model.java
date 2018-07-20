package com.alfred.jobModel;

import java.util.ArrayList;
import java.util.Map;

import com.alfred.utility.CSVReader;

public class Model {
	public ArrayList<Agent> agents = new ArrayList<Agent>(); 
	public ArrayList<City> cities = new ArrayList<City>();	
	public double[] agentParameters;
	public double[] cityParameters;
	
	private double jobsPerAgent = 5; //number of thousands of jobs represented by each agent
	
	private int nCPU;
	
	
	public Model(double[] agentParameters, double[] cityParameters) {
		nCPU = Runtime.getRuntime().availableProcessors();
		
		this.agentParameters = agentParameters;
		this.cityParameters  = cityParameters;
		
		//loading data
		
		CSVReader location_data = new CSVReader("data/Local_Authority_Districts_December_2017_Full_Clipped_Boundaries_in_Great_Britain.csv");
		CSVReader employment_data = new CSVReader("data/Employment_By_Local_Authority/2012.csv");
	
		int n_cities = location_data.getNRows();
		
		ArrayList<Double> lats  = new ArrayList<Double>();
		ArrayList<Double> lons  = new ArrayList<Double>();
		ArrayList<Double> areas = new ArrayList<Double>();
		ArrayList<Double> employment = new ArrayList<Double>();
		
		ArrayList<String> lats_string  = location_data.getColumn("lat" );
		ArrayList<String> lons_string  = location_data.getColumn("long");
		ArrayList<String> areas_string = location_data.getColumn("st_areashape");
		
		ArrayList<String> location_names_geographic = location_data.getColumn("lad17nm"); 
		ArrayList<String> location_names_employment = employment_data.getColumn("name");
		ArrayList<String> employment_string = employment_data.getColumn("employment");
		
		
		
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
			employment.add(Double.parseDouble(s) / jobsPerAgent);
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
			cities.add(new City(i, cities, lats.get(i), lons.get(i), areas.get(i), cityParameters[i]));
			String name = location_names_geographic.get(i);
			
			int j = 0;
			for(; j < location_names_employment.size(); j++) {
				if(name.equals(location_names_employment.get(j)))
					break;
			}
			if(j != location_names_employment.size()) {
				for(int k = 0; k < employment.get(j); k++)
					agents.add(new Agent(cities.get(i), agentParameters));
			}
			
		}
		
	}
	
	public static void run(String[] argv, double[] agent_params, double[] city_params) {
		
		double previous_moves = 0;
		Model m = new Model(agent_params, city_params);
		Plot p = new Plot(m, 0);
		for(int i = 0; i < 200; i++) {
			m.update();
			double moves = m.averageNMoves();
			System.out.println("Step " + i + " " + moves + " "  + (moves - previous_moves));
			p.draw();
			previous_moves = moves;	
		}
		m.dumpCities();
		
	}
	
	public void dumpCities() {
		for(City c: cities) {
			System.out.println(c.populationSize() + " \t" + c.getIndustryMean() + " \t" + Math.pow(c.getIndustryVariance(), 0.5));
		}
	}
	
	public double averageNMoves() {
		int sum = 0;
		for(Agent a : agents)
			sum += a.moves;
		return (double)sum / (double)agents.size();
	}
	
	
	
	public double[] update() {
		ArrayList<AgentDecisionRunnable> decisions = new ArrayList<AgentDecisionRunnable>();
		ArrayList<Thread> workers = new ArrayList<Thread>();
		for(int i = 0; i < nCPU; i++) {
			double s = (double)agents.size() / (double)(nCPU);
			int start = i * (int)s;
			int end   = (i + 1) * (int)s;
			if(i == (nCPU - 1) && end != agents.size())
				end = agents.size();
			decisions.add(new AgentDecisionRunnable(agents, cities, start, end));
			workers.add(new Thread(decisions.get(i)));
		}
		
		for(Thread w : workers)
			w.start();
		
		try{
			for(Thread w : workers)
				w.join();
		}catch(InterruptedException e) {
			e.printStackTrace();
		}
			
		//move agents
		for(AgentDecisionRunnable d : decisions) {
			for(Map.Entry<Agent, City> e : d.getDecisions().entrySet()) {
				e.getKey().setCity(e.getValue());
			}
		}
		
		
		//reset cache on all cities
		for(City c : cities) {
			c.setUpdateConsumerMarket(true);
		}
		//sort out return for genetic alg
		double[] r = new double[cities.size()];
		for(int i = 0; i < r.length; i++) {
			r[i]= cities.get(i).getPopulation() * jobsPerAgent;
		}
		return r;
	}
}
