package com.alfred.jobModel;

import java.awt.Canvas;
import java.awt.Color;
import java.awt.Graphics;

public class Drawing extends Canvas{
	/**
	 * 
	 */
	private static final long serialVersionUID = -5833125259908110049L;
	Model model;
	int width, height;
	double min_x, max_x, min_y, max_y;
	public Drawing(int width, int height, Model m) {
		this.width = width;
		this.height = height;
		setSize(width, height);
		setBackground(Color.white);
		model = m;
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
				g.setColor(new Color((float)c.getIndustryMean(), (float)c.getIndustryVariance(), 1.0f - (float)c.getIndustryMean()));
				int x = (int)((c.location[1] - min_x) * width / (10.0 - min_x)) + 150;
				int y = (int)((-c.location[0] + max_y) * 5 * height / (max_y - min_y)) + 100;
				circle(g, x, y, (int)(1.5  * Math.sqrt(c.getPopulation())));
			}

		}
	}
	
	public void circle(Graphics g, int x, int y, int r) {
		int render_x = x - r;
		int render_y = y - r;
		g.fillOval(render_x, render_y, 2*r, 2*r);
	}
}
