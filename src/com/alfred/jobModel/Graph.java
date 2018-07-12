package com.alfred.jobModel;

import java.awt.Canvas;
import java.awt.Color;
import java.awt.Graphics;


public class Graph extends Canvas{
	/**
	 * 
	 */
	private static final long serialVersionUID = 2L;
	Model model;
	int n_cities;
	int width, height;
	public Graph(int width, int height, Model m) {
		this.width = width;
		this.height = height;
		setSize(width, height);
		setBackground(Color.white);
		model = m;
		n_cities = m.cities.size(); //need to be careful this is done post init
	}
	
	public void paint(Graphics g) {
		Double min_rank = 1.0;
		for(City c : model.cities) {
			if(c.population_size() < min_rank && c.population_size() != 0) {
				min_rank = c.population_size();
				
			}
				
		}
		
		for(City c: model.cities) {
			g.setColor(new Color((float)c.average_industry(), (float)c.industry_variance() < 1.0f ? (float)c.industry_variance() : 1.0f , 1.0f - (float)c.average_industry()));
			//System.out.println(c.population_position());
			circle(g, (int)(Math.log(c.population_rank()) / Math.log(model.cities.size()) * width), (int)((Math.log(c.population_size()) /  Math.log(min_rank)) * height), 9);
		}
		
		//draw line with unit gradient
		
		g.setColor(Color.black);
		
		//System.out.println((int)(width * (1 / Math.log(model.cities.size()))) + " " + - 5 * (int)(height * (1 / Math.log(min_rank))));
		
		g.drawLine(0, 0, 5 * (int)(width * (1 / Math.log(model.cities.size()))), - 5 * (int)(height * (1 / Math.log(min_rank))));
		
	}
	
	public void circle(Graphics g, int x, int y, int r) {
		int render_x = x - r;
		int render_y = y - r;
		g.fillOval(render_x, render_y, 2*r, 2*r);
	}
}
