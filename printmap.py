from skyfield.api import Topos, load
from matplotlib import pyplot as plt
from numpy import arange

# starts a timescale so we can grab the epoch later
ts = load.timescale()

# loads up all active satellites, and makes a dictionary with the name as the key, and EarthSatellite object as the data
stations_url = 'http://celestrak.com/NORAD/elements/active.txt'
satellites = load.tle_file(stations_url)
print('Loaded', len(satellites), 'satellites')

by_name = {sat.name: sat for sat in satellites}

while (1):
    # try-except block incase they make a typo in their satellite selection
    isSuccessful = False
    while (not isSuccessful):
        try:
            selected_satellite = input(
                "Please type the official satelite name you would like to graph (ex KEPLER-1 (CASE)): ")
            satellite = by_name[selected_satellite]
            isSuccessful = True
        except (KeyError):
            print('Hmmm, seems you made a typo or this satelite is not currently active')

    print(satellite)

    # builds an array that holds times from epoch to a day before epoch
    t = ts.tt_jd(arange(satellite.epoch.tt - 1.0, satellite.epoch.tt, 0.001))

    latitudes = []
    longitudes = []

    # fills lat and long arrays with satellite values over the past 24h
    for time in t:
        latitudes.append(satellite.at(time).subpoint().latitude.degrees)
        longitudes.append(satellite.at(time).subpoint().longitude.degrees)

    # plot formatting. Includes picture, title, axis titles, and the plot itself
    background = plt.imread('./map.png')
    fig, ax = plt.subplots()
    ax.plot(longitudes, latitudes)
    ax.set_title('24h trajectory of ' + satellite.name)
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    plt.ylabel('Latitude (degrees)')
    plt.xlabel('Longitude (degrees)')
    ax.imshow(background, zorder=0, extent=(
        (-180), (180), (-90), (90)), aspect='auto')

    # saves the plot, and shows the user
    plt.savefig('trajectory_of_' + satellite.name + '.png')
    plt.show()

