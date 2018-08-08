import graphics, location

#min, max long: -6.65721989,  1.64949596
#min, max lat: 	49.92332077, 60.50495148


def main():
    g = graphics.Graphics(1000, 1000)

    print('Loading LA data...')
    lm = location.LocationManager('data/geographic/local_authority_locations.csv', 'data/migrations/la_companies_house_migration.csv')
    print('done')

    for id, la in lm.local_authorities.items():
        print(id)
        x, y = ll_to_xy((la.long, la.lat))
        g.draw_point(int(x), int(y), 2)
        for la_m, n in la.emmigration.items():
            x_, y_ = ll_to_xy((la_m.long, la_m.lat))
            g.draw_line(x, y, x_, y_)
        g.draw_temp_surf_with_alpha(30)

    while not g.should_quit():
        #g.draw_point(5, 5, 20)
        g.flip()
        pass

    g.quit()

def ll_to_xy(position):
        x = (position[0] - (-6.65)) / ((1.649 - -6.657)) * 750 + 125
        y = 1000 -(position[1] - (49.9233)) / (60.5049 - 49.9233) * 900 - 50
        return (x, y)

if __name__ == '__main__':
    main()
