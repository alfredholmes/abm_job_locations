import graphics, location, time

#min, max long: -6.65721989,  1.64949596
#min, max lat: 	49.92332077, 60.50495148


def main():
    size = 1920
    g = graphics.Graphics(size, size)

    print('Loading LA data...')
    lm = location.LocationManager('data/geographic/local_authority_locations.csv', 'data/migrations/la_companies_house_migration.csv')
    print('done')

    for id, la in lm.local_authorities.items():
        print(id)
        x, y = ll_to_xy((la.long, la.lat), size)
        #g.draw_point(int(x), int(y), 1)
        for la_m, n in la.emmigration.items():
            x_, y_ = ll_to_xy((la_m.long, la_m.lat), size)
            c = '#ff5a5f'
            if y_ < y:
                #if move to is further south - make white
                c = '#bfd7ea'
            #g.flip()
            g.draw_line(x, y, x_, y_, c, int(n / 300 * 255))


    g.save_to_file('output_.bmp')
    g.flip()

    #while not g.should_quit():
    #    pass

    g.quit()

def ll_to_xy(position, size):
        x = (position[0] - (-6.65)) / ((1.649 - -6.657)) * 0.75 * size + 0.125 * size
        y = size -(position[1] - (49.9233)) / (60.5049 - 49.9233) * size - 0.05 * size
        return (x, y)

if __name__ == '__main__':
    main()
