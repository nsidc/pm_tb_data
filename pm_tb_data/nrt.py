"""Assess access options for NRT AMSR2 LANCE data.
"""
import earthaccess


if __name__ == '__main__':
    results = earthaccess.search_data(short_name='AU_SI12_NRT_R04')
    print(f'Found {len(results)} granules.')
    results = sorted(results, key=lambda x: x['meta']['revision-date'], reverse=True)
    for granule in results:
        # This looks like the fn
        native_id = granule['meta']['native-id']
        revision_date = granule['meta']['revision-date']
        print(f'{native_id} {revision_date=}')
