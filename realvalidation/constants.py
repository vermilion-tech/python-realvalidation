from pbr.version import VersionInfo

VERSION = VersionInfo('realvalidation').semantic_version().release_string()
DESCRIPTION = "RealValidation v{}".format(VERSION)

MOCK_DNC_URL = 'https://realvalidation-dnc-mock.herokuapp.com/validate'
PROD_DNC_URL = 'https://api.realvalidation.com/rpvWebService/DNCLookup.php'

PHONE_COLUMN_REGEX = r'^phone$'
PHONE_DIGIT_REGEX = r'^\d{10}$'

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'DEBUG'
