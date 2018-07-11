import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public class Model {
	public ArrayList<Agent> agents = new ArrayList<Agent>(); 
	public ArrayList<City> cities = new ArrayList<City>();
	
	double[][] transport_costs; // Slippage, IE 1 = no transport costs, 0 = infinite transport costs
	
	
	public Model(int n_cities, int n_agents) {
		

		for(int i = 0; i < n_cities; i++)
			cities.add(new City(i, cities));
		
		//generate distances
		transport_costs = least_distance_matrix(cities, n_cities);
		

		//generate agents
		for(int i = 0; i < n_agents; i++)
			agents.add(new Agent(cities));
	}
	
	public static void main(String[] argv) {
		
		long then = System.currentTimeMillis();
		double previous_moves = 0;
		Model m = new Model(100, 2000);
		Plot p = new Plot(m, 0);
		//Plot q = new Plot(m, 1);
		for(int i = 0; i < 100; i++) {
			m.dump_cities();
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
			System.out.println(c.population_rank() + " \t" + c.average_industry() + " \t" + Math.pow(c.industry_variance(agents), 0.5) + "\t " + transport_cost_to_largest_city(c));
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
		
		return transport_costs[city.get_id()][capital.get_id()];
		
		
	}
	
	public void update() {
		Map<Agent, City> movements = new HashMap<Agent, City>();
		for(Agent a : agents) {			
			movements.put(a, a.get_next_city(agents, cities, transport_costs));
		}
		//do the actual updates after all the agents have made their decisions
		for(Map.Entry<Agent, City> m : movements.entrySet()) {
			m.getKey().set_city(m.getValue());
		}
	}
	
	private boolean matricies_equal(double[][] A, double[][] B) {
		if (A.length != B.length)
			return false;
		for (int i = 0; i < A.length; i++) {
			for(int j = 0; j < A[i].length; j++) {
				try {
				if (A[i][j] != B[i][j])
					return false;
				} catch(ArrayIndexOutOfBoundsException e) {
					return false;
				}
			}
		}
		return true;
	}
	
	private double[][] least_distance_matrix(ArrayList<City> cities, int n_cities){
		//Random r = new Random();
		transport_costs = new double[n_cities][n_cities];
		for(int i = 0; i < n_cities; i++) {
			transport_costs[i][i] = 1;
			System.out.print(1);
			for(int j = i + 1; j < n_cities; j++) {
				double euclidian_distance = cities.get(i).distance_to(cities.get(j));
				System.out.print(euclidian_distance);
				transport_costs[i][j] = transport_costs[j][i] = Math.exp(-euclidian_distance * 5);
				
				}
			System.out.println();
		}
		//check to see matrix makes sense - ie triangle law holds
		//double[][] bak = new double[n_cities][n_cities];
		
		/*while(!matricies_equal(bak, transport_costs)) {
			bak = transport_costs.clone();
			//for each non diagonal element of the array, if the transport costs do not make sense change them
			for(int i = 0; i < n_cities; i++) {
				for(int j = i+1; j < n_cities; j++) {
					//inspecting transport_costs[i][j]
					for(int k = i+1; k < n_cities; k++) {
						if(k != j && transport_costs[i][k] * transport_costs[k][j] > transport_costs[i][j]) {
							transport_costs[i][j]  = transport_costs[j][i] = transport_costs[i][k] * transport_costs[k][j];
						}
					}
				}
			}
		}*/
		
		return transport_costs;
	}
}
