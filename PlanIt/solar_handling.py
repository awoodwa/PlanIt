import pandas as pd
import dateutil


def create_ghi_tseries(wtk, loc_idx):
    '''
    Creates a list of time series for inputs in other solar functions.

    Inputs
        wtk : h5pyd file
        loc_idx : tuple of latitude and longitude indices

    Outputs
        tseries_list : list of time series of solar data for 2007 - 2013
    '''
    # create dset
    dset = wtk['GHI']

    dt = wtk['datetime']
    dt = pd.DataFrame({'datetime': dt[:]}, index=range(0, dt.shape[0]))
    dt['datetime'] = dt['datetime'].apply(dateutil.parser.parse)

    twenty07 = dt.loc[(dt.datetime >= '2007-01-01') &
                      (dt.datetime < '2008-01-01')].index
    twenty08 = dt.loc[(dt.datetime >= '2008-01-01') &
                      (dt.datetime < '2009-01-01')].index
    twenty09 = dt.loc[(dt.datetime >= '2009-01-01') &
                      (dt.datetime < '2010-01-01')].index
    twenty10 = dt.loc[(dt.datetime >= '2010-01-01') &
                      (dt.datetime < '2011-01-01')].index
    twenty11 = dt.loc[(dt.datetime >= '2011-01-01') &
                      (dt.datetime < '2012-01-01')].index
    twenty12 = dt.loc[(dt.datetime >= '2012-01-01') &
                      (dt.datetime < '2013-01-01')].index
    twenty13 = dt.loc[(dt.datetime >= '2013-01-01') &
                      (dt.datetime < '2014-01-01')].index

    time_slices = [twenty07, twenty08, twenty09, twenty10, twenty11, twenty12,
                   twenty13]

    tseries_list = []

    for i in time_slices:
        t = dset[min(i):max(i) + 1, loc_idx[0], loc_idx[1]]
        tseries_list.append(t)

    return tseries_list


def annual_solar_energy(wtk, loc_idx):
    '''
    This function calculates the energy produced a year in kWh for
    a single solar panel with an average area of 65 in x 39 in
    and an average efficiency of 20% at a specific location in
    the United States.
    Inputs
        tseries_list : list of time series of solar data for 2007 - 2013
    Outputs
        annual_energies : energy generated by one solar panel each year
        in kWh.
    '''
    tseries_list = create_ghi_tseries(wtk, loc_idx)
    annual_energies = []
    for i in range(len(tseries_list)):
        annual_energies.append(sum(tseries_list[i] * 0.20 * 1.635481 / 1000))

    return annual_energies


def annual_solar_mean(wtk, loc_idx):
    '''
    This function calculates the average solar energy that could be
    generated by one solar panel at a specific location over the
    2007 - 2013 time range.
    Inputs
        annual_energies : energy generated by one solar panel each year
        in kWh.
    Outputs
        annual_mean : average solar energy generated by on solar panel
        in a year.
    '''
    annual_energies = annual_solar_energy(wtk, loc_idx)
    annual_mean = sum(annual_energies) / len(annual_energies)

    return annual_mean
