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
	public Drawing(int width, int height, Model m) {
		this.width = width;
		this.height = height;
		setSize(width, height);
		setBackground(Color.white);
		model = m;
		n_cities = m.cities.size(); //need to be careful this is done post init
	}
	
	public void paint(Graphics g) {
		//System.out.println("Call");
		if(model.cities.size() != 0) {
			for(int i = 0; i < model.transport_costs.length; i++) {
				for(int j = i+1; j < model.transport_costs[i].length; j++) {
					g.setColor(new Color((float)(1 - model.transport_costs[i][j]), (float)(1 - model.transport_costs[i][j]), (float)(1 - model.transport_costs[i][j])));
					int x1 = (int)(model.cities.get(i).location[0] * width);
					int y1 = (int)(model.cities.get(i).location[1] * height);
					
					int x2 = (int)(model.cities.get(j).location[0] * width);
					int y2 = (int)(model.cities.get(j).location[1] * height);
					g.drawLine(x1, y1, x2, y2);
				}
			}
			
			for(City c : model.cities) {
				g.setColor(new Color((float)c.average_industry(), (float)c.industry_variance(model.agents), 1.0f - (float)c.average_industry()));
				//g.fillOval(, (int)(250 * Math.sin(2*Math.PI / 10 * c.get_id())) + 500, (int)(c.get_population() / 5), (int)(c.get_population() / 5));
				int x = (int)(c.location[0] * width);
				int y = (int)(c.location[1] * height);
				circle(g, x, y, 2 * (int)Math.sqrt(c.get_population()));
			}

		}
	}
	
	public void circle(Graphics g, int x, int y, int r) {
		int render_x = x - r;
		int render_y = y - r;
		g.fillOval(render_x, render_y, 2*r, 2*r);
	}
}
