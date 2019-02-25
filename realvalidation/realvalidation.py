import requests
import logging
import re
import os


class InvalidTokenException(Exception):
    pass


class InvalidPhoneFormatException(Exception):
    pass


class InvalidJSONResponseException(Exception):
    pass


class ResponseCodeNotOkException(Exception):
    pass


class RealValidation:
    DEFAULT_OUTPUT = 'json'
    DEFAULT_URL = 'https://api.realvalidation.com/rpvWebService/DNCLookup.php'
    PHONE_REGEX = r'^\d{10}$'  # 10 numeric digits only

    def __init__(self,
                 token=os.environ.get('RV_TOKEN'),
                 output=DEFAULT_OUTPUT,
                 url=DEFAULT_URL):
        """Initializes RealValidation API Object.

        Parameters
        ----------
        token : str
            RealValidation API Token, defaults to environmental variable
            RV_TOKEN.
        output : str
            Set to json or xml, defaults to json.
        url : str
            ReaValdation API URL, defaults to production RealValidation DNC API

        Returns
        -------
        type
            A ready to use RealValidation object that can be used to query
            phones against the DNC api.

        """

        self.log = logging.getLogger(__name__)

        if token is None:
            raise InvalidTokenException

        self.output = output
        self.token = token
        self.url = url

        self.log.debug('<RealValidation {} >'.format(self.__dict__))

    def lookup_phone(self, phone):
        """Checks the RealValidation DNC Api for a given phone.

        Parameters
        ----------
        phone : str
            The phone to check against RealValidation's DNC

        Returns
        -------
        type
            JSON Response from RealValidation API.

        """
        # must match regular expression or raise error
        if not re.match(self.PHONE_REGEX, phone):
            raise InvalidPhoneFormatException

        # assemble our request payload
        payload = dict(
            output=self.output,
            token=self.token,
            phone=phone
        )

        # initiate our request
        req = requests.get(self.url, params=payload)

        # if request isn't ok raise for status
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        # attempt to decode json from response
        # if we can't, raise error
        try:
            data = req.json()
        except ValueError as error:
            raise InvalidJSONResponseException

        # if realvalidation RESPONSECODE isn't OK raise error
        if data.get('RESPONSECODE') != 'OK':
            raise ResponseCodeNotOkException

        return data
