package com.alfred.jobModel;

import java.awt.Canvas;
import java.awt.Color;
import java.awt.Graphics;

public class Drawing extends Canvas{
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	Model model;
	int n_cities;
	int width, height;
	double min_x, max_x, min_y, max_y;
	public Drawing(int width, int height, Model m) {
		this.width = width;
		this.height = height;
		setSize(width, height);
		setBackground(Color.white);
		model = m;
		n_cities = m.cities.size(); //need to be careful this is done post init
		boolean first = true;
		for(City c : model.cities) {
			if(first) {
				min_x = max_x = c.location[0];
				min_y = max_y = c.location[1];
				first = false;
			}else {
				if(c.location[1] < min_x) {
					min_x = c.location[1];
				}
				if(c.location[1] > max_x) {
					max_x = c.location[1];
				}
				if(c.location[0] < min_y) {
					min_y = c.location[0];
				}
				if(c.location[0] > max_y) {
					max_y = c.location[0];
				}
			}
		}
	}
	
	public void paint(Graphics g) {
		//System.out.println("Call");
		if(model.cities.size() != 0) {			
			for(City c : model.cities) {
				g.setColor(new Color((float)c.get_industry_mean(), (float)c.get_industry_variance(), 1.0f - (float)c.get_industry_mean()));
				//g.fillOval(, (int)(250 * Math.sin(2*Math.PI / 10 * c.get_id())) + 500, (int)(c.get_population() / 5), (int)(c.get_population() / 5));
				//int x = (int)(c.location[0] * width);
				//int y = (int)(c.location[1] * height);
				int x = (int)((c.location[1] - min_x) * width / (10.0 - min_x)) + 150;
				int y = (int)((-c.location[0] + max_y) * 5 * height / (max_y - min_y)) + 100;
				//System.out.println(min_x + " " + min_y + " " + max_x + " " + 10.0);
				circle(g, x, y, (int)(1.5  * Math.sqrt(c.get_population())));
			}

		}
	}
	
	public void circle(Graphics g, int x, int y, int r) {
		int render_x = x - r;
		int render_y = y - r;
		g.fillOval(render_x, render_y, 2*r, 2*r);
	}
}
