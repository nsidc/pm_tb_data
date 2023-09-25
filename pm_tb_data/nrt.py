"""Assess access options for NRT AMSR2 LANCE data.
"""
import earthaccess


if __name__ == '__main__':
    results = earthaccess.search_data(short_name='AU_SI12_NRT_R04')
    print(f'Found {len(results)} granules.')
