import bisect

# Initial a level list for iaqi and each pollutant based on the China Standard.
iaqi_list = [0, 50, 100, 150, 200, 300, 400, 500]
so2_24h_list = [0, 50, 150, 475, 800, 1600, 2100, 2620]
so2_1h_list = [0, 150, 500, 650, 800]
no2_24h_list = [0, 40, 80, 180, 280, 565, 750, 940]
no2_1h_list = [0, 100, 200, 700, 1200, 2340, 3090, 3840]
pm10_24h_list = [0, 50, 150, 250, 350, 420, 500, 600]
co_24h_list = [0, 2, 4, 14, 24, 36, 48, 60]
co_1h_list = [0, 5, 10, 35, 60, 90, 120, 150]
o3_1h_list = [0, 160, 200, 300, 400, 800, 1000, 1200]
o3_8h_list = [0, 100, 160, 215, 265, 800]
pm25_24h_list = [0, 35, 75, 115, 150, 250, 350, 500]


def calc_iaqi(pollutant_level_list, pollutant_value, allow_exceed=True):
    list_index = bisect.bisect_right(pollutant_level_list, pollutant_value)
    if list_index < len(pollutant_level_list):
        iaqi = round(((iaqi_list[list_index] - iaqi_list[list_index - 1]) /
                      (pollutant_level_list[list_index] - pollutant_level_list[list_index - 1]) *
                      (pollutant_value - pollutant_level_list[list_index - 1])) + iaqi_list[list_index - 1])
    else:
        if allow_exceed:
            iaqi = 500
        else:
            iaqi = 0
    return iaqi


if __name__ == '__main__':
    # data for test
    pollutant_data = {
        'SO2_24h': 200,
        'SO2_1h': 1000,
        'NO2_24h': 200,
        'NO2_1h': 800,
        'PM10_24h': 333,
        'CO_24h': 9,
        'CO_1h': 13,
        'O3_1h': 280,
        'O3_8h': 323,
        'PM25_24h': 99
    }

    # iaqi_result_dict stores all iaqi values.
    iaqi_result_dict = dict()
    iaqi_result_dict['SO2_24h'] = calc_iaqi(so2_24h_list, pollutant_data['SO2_24h'])
    iaqi_result_dict['SO2_1h'] = calc_iaqi(so2_1h_list, pollutant_data['SO2_1h'], allow_exceed=False)
    iaqi_result_dict['NO2_24h'] = calc_iaqi(no2_24h_list, pollutant_data['NO2_24h'])
    iaqi_result_dict['NO2_1h'] = calc_iaqi(no2_1h_list, pollutant_data['NO2_1h'])
    iaqi_result_dict['PM10_24h'] = calc_iaqi(pm10_24h_list, pollutant_data['PM10_24h'])
    iaqi_result_dict['CO_24h'] = calc_iaqi(co_24h_list, pollutant_data['CO_24h'])
    iaqi_result_dict['CO_1h'] = calc_iaqi(co_1h_list, pollutant_data['CO_1h'])
    iaqi_result_dict['O3_1h'] = calc_iaqi(o3_1h_list, pollutant_data['O3_1h'])
    iaqi_result_dict['O3_8h'] = calc_iaqi(o3_8h_list, pollutant_data['O3_8h'], allow_exceed=False)
    iaqi_result_dict['PM25_24h'] = calc_iaqi(pm25_24h_list, pollutant_data['PM25_24h'])
    print(f'IAQI: {iaqi_result_dict}\n')

    # output the AQI value.
    aqi_value = max(iaqi_result_dict.values())
    print(f'AQI: {aqi_value}')

    # output the primary pollutant.
    if aqi_value > 50:
        # primary_pollutant could be more than one.
        primary_pollutant_list = [key for key, value in iaqi_result_dict.items() if value == aqi_value]
        primary_pollutant_str = ''
        for primary_pollutant in primary_pollutant_list:
            primary_pollutant_str += primary_pollutant + ', '
        primary_pollutant_str = primary_pollutant_str[:-2]   # remove the comma at the end.
        print(f'Primary Pollutant: {primary_pollutant_str}')
