import configparser
import getpass
#from pathlib import Path


class Database:

    #ROOT_DIR = Path(__file__).parents[1]
    #CONFIG_DIR = os.path.abspath(os.path.join(ROOT_DIR, 'configs'))
    #CONFIG_FILENAME = CONFIG_DIR + '/config.ini'
    CONFIG_FILENAME = 'C:/Users/MarcelloCavalcanti/Google Drive/Trading/Python/Models/Stochastic_Pair_Trading/Fasanara/Futures_Execution/config.ini'

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.CONFIG_FILENAME)

    def configure_sql_user_settings(self):
        user_pass = getpass.getuser()
        SQL_credentials_map = {
            user_pass: {
                'user': self.config['DATABASE_USERS_SETTINGS']['username'],
                'password': self.config['DATABASE_USERS_SETTINGS']['password'],
                'host': self.config['DATABASE_USERS_SETTINGS']['hostname'],
                'port': '3306',
                'db': self.config['DATABASE_NAME_SETTINGS']['default_database']
            }
        }
        setattr(self, 'sql_credentials', SQL_credentials_map)

    def configure_twitter_dev_settings(self):
        twitter_credentials_map = {
            'username': self.config['TWITTER_DEV_CREDENTIALS']['username'],
            'consumer_key': self.config['TWITTER_DEV_CREDENTIALS']['consumer_key'],
            'consumer_secret': self.config['TWITTER_DEV_CREDENTIALS']['consumer_secret'],
            'access_key': self.config['TWITTER_DEV_CREDENTIALS']['access_key'],
            'access_secret': self.config['TWITTER_DEV_CREDENTIALS']['access_secret']
        }

        setattr(self, 'twitter_credentials', twitter_credentials_map)
        return self

    def configure_alpha_vantage_settings(self):
        alpha_vantage_credentials_map = {
            'api_key': self.config['ALPHA_VANTAGE_CREDENTIALS']['api_key'],
            'api_keys': self.config['ALPHA_VANTAGE_CREDENTIALS']['api_keys'],
            'email': self.config['ALPHA_VANTAGE_CREDENTIALS']['email'],
            'url': self.config['ALPHA_VANTAGE_CREDENTIALS']['url']

        }
        setattr(self, 'alpha_vantage_credentials_map', alpha_vantage_credentials_map)

    def configure_iex_cloud_settings(self):
        iex_credentials_map = {
            'account_number': self.config['IEX_CREDENTIALS']['account_number'],
            'secret_key': self.config['IEX_CREDENTIALS']['secret_token'],
            'public_key': self.config['IEX_CREDENTIALS']['publishable_token']
        }
        setattr(self, 'iex_credentials_map', iex_credentials_map)

    def configure_pau_email_credentials(self):
        pau_email_credentials_map = {
            'email': self.config['PAU_EMAIL']['email'],
            'password': self.config['PAU_EMAIL']['password'],
        }
        setattr(self, 'pau_email_credentials_map', pau_email_credentials_map)

    def configure_generic_email_credentials(self):
        generic_email_credentials_map = {
            'email': self.config['QUANT_EMAIL']['email'],
            'password': self.config['QUANT_EMAIL']['password'],
        }
        setattr(self, 'generic_email_credentials_map', generic_email_credentials_map)

    def configure_flexnow_live_credentials(self):
        live_credentials_map = {
            'client_id': self.config['FLEXNOW_EXECUTION_CREDENTIALS']['uat_client_id'],
            'token': self.config['FLEXNOW_EXECUTION_CREDENTIALS']['uat_token']
        }
        setattr(self, 'live_credentials_map', live_credentials_map)

    def configure_flexnow_uat_credentials(self):
        uat_credentials_map = {
            'client_id': self.config['FLEXNOW_EXECUTION_CREDENTIALS']['uat_client_id'],
            'token': self.config['FLEXNOW_EXECUTION_CREDENTIALS']['uat_token'],
            'user': self.config['FLEXNOW_EXECUTION_CREDENTIALS']['uat_user'],
            'psswd': self.config['FLEXNOW_EXECUTION_CREDENTIALS']['uat_password']
        }
        setattr(self, 'uat_credentials_map', uat_credentials_map)
