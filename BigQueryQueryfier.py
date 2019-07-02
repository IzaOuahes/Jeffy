from google.oauth2 import service_account
from os.path import join
import pandas_gbq
import json

#import settings


class BigQueryQueryfier():
    """Class to query BigQuery and get data from datasetsself.

    Attributes
    ----------
    project_id: string
        Project ID set in Google Cloud Platform
    credentials: google.oauth2.service_account.Credentials

    """

    def __init__(self, project_id='zinc-bucksaw-245306',
                            credentials_filename='zinc-bucksaw-245306-4b1c1d26fd11.json'):
        """Initialize class.

        Parameters
        ----------
        project_id: string, default 'sephora-sea'
        credentials_filename: string, default 'sephora-sea-credentials.json'
            Name of file containing credentials

        """
        self.project_id = project_id

        credentials_filepath = credentials_filename
        self.credentials = service_account.Credentials.from_service_account_file(credentials_filepath)

    def query_to_df(self, sql_query):
        """Query sql_query and return results in pandas dataframeself.

        Parameters
        ----------
        sql_query: string

        Returns
        -------
        df: pandas.DataFrame

        """
        df = pandas_gbq.read_gbq(sql_query,
                                 project_id=self.project_id,
                                 credentials=self.credentials)
        return df


if __name__ == '__main__':
    SQL = """ SELECT id, property_type, place_name, country_name, state_name, geonames_id, lat_lon, price, surface_total_in_m2, floor, rooms, expenses, properati_url, description, title, image_thumbnail 
    FROM `properati-data-public.properties_mx.properties_rent_201802` 
        WHERE place_name LIKE '%{title_searched}%'
              AND description  LIKE '%{text_searched}%'
        """.format(title_searched='Colima', text_searched='vistas panorámicas')
    bqq = BigQueryQueryfier(project_id='zinc-bucksaw-245306',
                            credentials_filename='zinc-bucksaw-245306-4b1c1d26fd11.json')

    df=bqq.query_to_df(sql_query=SQL)
    dict_houses=df.to_dict(orient='record')
    output = json.dumps(dict_houses)
    loaded_r = json.loads(output)
    for r in loaded_r:
        print(r.get('properati_url'))

