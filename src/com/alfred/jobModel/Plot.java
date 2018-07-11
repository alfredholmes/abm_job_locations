package com.alfred.jobModel;


import javax.swing.JFrame;

public class Plot {
	JFrame map_window;
	JFrame graph_window;
	Drawing map;
	Graph graph;
	int mode;
	public Plot(Model m, int mode) {
		this.mode = mode;
		if(mode == 1 || mode == 0) {
			map_window = new JFrame("Map");
			map_window.setSize(1000, 1000);
			map = new Drawing(1000, 1000, m);
			map_window.add(map);
			map_window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			map_window.setVisible(true);
			
		}
		
		if(mode == 2 || mode == 0) {
			
			graph_window = new JFrame("Graph");
			graph_window.setSize(800, 500);
			
			graph_window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			
			graph = new Graph(800, 500, m);
			
			//graph_window.setLocationRelativeTo(null);
			
			graph_window.add(graph);
			
			graph_window.setVisible(true);
		
		}
		
		
		
		
		
	}
	
	public void draw() {
		//drawing.
		if(mode == 0 || mode ==1)
			map.repaint();
		
		if(mode == 0 || mode == 2)
			graph.repaint();
		
	}
}
