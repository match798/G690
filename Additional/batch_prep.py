# import necessary libraries
import numpy as np
import netCDF4 as nc
from datetime import datetime, timedelta
import glob
import ntpath


def cumulative_daily(precip_file: str, output_file: str):
    # open the .nc file
    precip_ds = nc.Dataset(precip_file, 'r')

    # extract the shape and values of latitude and longitude
    lat_size = precip_ds.dimensions['south_north'].size
    lat_values = precip_ds.variables['XLAT'][0, :, 0]
    lon_size = precip_ds.dimensions['west_east'].size
    lon_values = precip_ds.variables['XLONG'][0, 0, :]

    # calculate the daily cumulative precipitation
    precip_data = precip_ds.variables['PRECIP'][:]
    precip_sum_data = np.ma.sum(precip_data.reshape(-1, 8, lat_size, lon_size), axis=1)

    # set up time values
    time_var = precip_ds.variables['XTIME']
    start_time = nc.num2date(time_var[0], time_var.units, calendar=time_var.calendar, only_use_python_datetimes=True)
    dates = np.ma.asarray([start_time + n * timedelta(days=1) for n in range(precip_sum_data.shape[0])])
    times = nc.date2num(dates, 'days since ' + str(start_time.isoformat()), calendar=time_var.calendar,
                        has_year_zero=True)
    times = np.ma.asarray(times, dtype=type(time_var[0]))

    # create output dataset
    precip_sum_ds = nc.Dataset(output_file, 'w')
    # set up dataset/group attributes
    ds_attr = {'timestamp': datetime.now().isoformat(timespec='seconds', sep=' '),
               'source': ntpath.basename(precip_file),
               'software': "Python library version: " + str(nc.__version__),
               'Conventions': "CF-1.8",
               'lat_min': 34.816276550293,
               'lat_max': 44.279541015625,
               'lon_min': -92.0864181518555,
               'lon_max': -79.7807235717773}
    precip_sum_ds.setncatts(ds_attr)

    # set up the dimensions and their sizes
    precip_sum_ds.createDimension('time', None)
    dim_names = ['time', 'lat', 'lon']
    for i in np.arange(1, 3):
        precip_sum_ds.createDimension(dim_names[i], precip_sum_data.shape[i])

    # set up time variable
    precip_sum_ds.createVariable('time', 'int32', ('time'))
    precip_sum_ds.variables['time'].setncatts({'long_name': 'time',
                                               'standard_name': 'time',
                                               'units': 'days since ' + str(start_time.isoformat()),
                                               'calendar': time_var.calendar})
    precip_sum_ds.variables['time'][:] = times[:]

    # set up latitude variable
    precip_sum_ds.createVariable('lat', 'float32', ('lat'), fill_value=precip_ds.variables['XLAT']._FillValue)
    precip_sum_ds.variables['lat'].setncatts({'FieldType': 104,
                                              'MemoryOrder': 'XY',
                                              'long_name': 'latitude, south is negative',
                                              'standard_name': 'latitude',
                                              'units': 'degrees_north',
                                              'stagger': ''})
    precip_sum_ds.variables['lat'][:] = lat_values[:]

    # set up longitude variable
    precip_sum_ds.createVariable('lon', 'float32', ('lon'), fill_value=precip_ds.variables['XLONG']._FillValue)
    precip_sum_ds.variables['lon'].setncatts({'FieldType': 104,
                                              'MemoryOrder': 'XY',
                                              'long_name': 'longitude, west is negative',
                                              'standard_name': 'longitude',
                                              'units': 'degrees_east',
                                              'stagger': ''})
    precip_sum_ds.variables['lon'][:] = lon_values[:]

    # set up precipitation variable
    precip_sum_ds.createVariable('precip', 'float32', ('time', 'lat', 'lon'),
                                 fill_value=precip_ds.variables['PRECIP']._FillValue)
    precip_sum_ds.variables['precip'].setncatts({'FieldType': 104,
                                                 'MemoryOrder': 'XY',
                                                 'long_name': 'accumulated daily cumulus precipitation',
                                                 'standard_name': 'lwe_thickness_of_precipitation_amount',
                                                 'units': 'mm',
                                                 'stagger': '',
                                                 'coordinates': 'time lat lon'})
    precip_sum_ds.variables['precip'][:] = precip_sum_data[:]

    # close both datasets/files
    precip_ds.close()
    precip_sum_ds.close()


def min_max_mean_daily(t2_file: str, output_file: str):
    # open the .nc file
    t2_ds = nc.Dataset(t2_file, 'r')

    # extract the shape and values of latitude and longitude
    lat_size = t2_ds.dimensions['south_north'].size
    lat_values = t2_ds.variables['XLAT'][0, :, 0]
    lon_size = t2_ds.dimensions['west_east'].size
    lon_values = t2_ds.variables['XLONG'][0, 0, :]

    # calculate the daily min, max and mean temperature, respectively
    t2_data = t2_ds.variables['T2'][:].reshape(-1, 8, lat_size, lon_size)
    t2_min_data = np.ma.min(t2_data, axis=1)
    t2_max_data = np.ma.max(t2_data, axis=1)
    t2_mean_data = np.ma.mean(t2_data, axis=1)

    # set up time values
    time_values = np.ma.masked_array(range(t2_data.shape[0]), dtype=int)
    start_time = nc.num2date(t2_ds.variables['XTIME'][0], t2_ds.variables['XTIME'].units,
                             calendar=t2_ds.variables['XTIME'].calendar, only_use_python_datetimes=True)

    # create output dataset
    t2_daily_ds = nc.Dataset(output_file, 'w')
    # set up dataset/group attributes
    ds_attr = {'timestamp': datetime.now().isoformat(timespec='seconds', sep=' '),
               'source': ntpath.basename(t2_file),
               'software': "Python library version: " + str(nc.__version__),
               'Conventions': "CF-1.8",
               'lat_min': 34.816276550293,
               'lat_max': 44.279541015625,
               'lon_min': -92.0864181518555,
               'lon_max': -79.7807235717773}
    t2_daily_ds.setncatts(ds_attr)

    # set up the dimensions and their sizes
    t2_daily_ds.createDimension('time', None)
    t2_daily_ds.createDimension('lat', lat_size)
    t2_daily_ds.createDimension('lon', lon_size)

    # create variables
    time_var = t2_daily_ds.createVariable('time', np.int32, ('time'))
    lat_var = t2_daily_ds.createVariable('lat', np.float32, ('lat'), fill_value=t2_ds.variables['XLAT']._FillValue)
    lon_var = t2_daily_ds.createVariable('lon', np.float32, ('lon'), fill_value=t2_ds.variables['XLONG']._FillValue)
    min_var = t2_daily_ds.createVariable('t2_min', np.float32, ('time', 'lat', 'lon'),
                                         fill_value=t2_ds.variables['T2']._FillValue)
    max_var = t2_daily_ds.createVariable('t2_max', np.float32, ('time', 'lat', 'lon'),
                                         fill_value=t2_ds.variables['T2']._FillValue)
    mean_var = t2_daily_ds.createVariable('t2_mean', np.float32, ('time', 'lat', 'lon'),
                                          fill_value=t2_ds.variables['T2']._FillValue)

    # set up the attributes of variables
    time_var.setncatts({'long_name': 'time',
                        'standard_name': 'time',
                        'units': 'days since ' + str(start_time.isoformat()),
                        'calendar': t2_ds.variables['XTIME'].calendar})
    lat_var.setncatts({'FieldType': 104,
                       'MemoryOrder': 'XY',
                       'long_name': 'latitude, south is negative',
                       'standard_name': 'latitude',
                       'units': 'degrees_north',
                       'stagger': ''})
    lon_var.setncatts({'FieldType': 104,
                       'MemoryOrder': 'XY',
                       'long_name': 'longitude, west is negative',
                       'standard_name': 'longitude',
                       'units': 'degrees_east',
                       'stagger': ''})
    min_var.setncatts({'FieldType': 104,
                       'MemoryOrder': 'XY',
                       'long_name': 'minimum air temperature at 2 m',
                       'standard_name': 'air_temperature',
                       'units': 'K',
                       'stagger': '',
                       'coordinates': 'time lat lon'})
    max_var.setncatts({'FieldType': 104,
                       'MemoryOrder': 'XY',
                       'long_name': 'maximum air temperature at 2 m',
                       'standard_name': 'air_temperature',
                       'units': 'K',
                       'stagger': '',
                       'coordinates': 'time lat lon'})
    mean_var.setncatts({'FieldType': 104,
                        'MemoryOrder': 'XY',
                        'long_name': 'mean air temperature at 2 m',
                        'standard_name': 'air_temperature',
                        'units': 'K',
                        'stagger': '',
                        'coordinates': 'time lat lon'})

    # save data to variables
    time_var[:] = time_values[:]
    lat_var[:] = lat_values[:]
    lon_var[:] = lon_values[:]
    min_var[:] = t2_min_data[:]
    max_var[:] = t2_max_data[:]
    mean_var[:] = t2_mean_data[:]

    # close both datasets/files
    t2_ds.close()
    t2_daily_ds.close()


if __name__ == "__main__":
    # set up the input and output locations
    input_folder = "R:\\Projects\\WaterBalance\\RunoffRecharge\\SWB\\Carbonate\\I74WaterStudy\\downscaled_from_Ben\\"
    output_folder = "R:\\Projects\\WaterBalance\\RunoffRecharge\\SWB\\Carbonate\\I74WaterStudy\\CESM1_downscaled\\Ruhui\\Output\\"

    # find all nc files in the input folder
    input_file_list = glob.glob(input_folder + "*.nc")
    for file_num, input_file in enumerate(input_file_list):
        file_name = ntpath.basename(input_file).split('.')[0].split('_')
        output_file = output_folder + file_name[0] + '_daily_' + file_name[2] + '.nc'
        if file_name[0] == 'PRECIP':
            #cumulative_daily(input_file, output_file)
            print(file_num+1)
            #print(output_file)
        elif file_name[0] == 'T2' and file_num+1 > 204:
            min_max_mean_daily(input_file, output_file)
            print(file_num+1)
            print(output_file)
        else:
            print("file is not precipitation or t2")
