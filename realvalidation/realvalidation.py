import requests
import logging
import re
import os

from .errors import (
    InvalidTokenError, InvalidPhoneFormatError, InvalidJSONResponseError,
    ResponseCodeNotOkError
)


class RealValidation:
    """Short summary.

    Parameters
    ----------
    token : str
        RealValidation API Token. Defaults to environmental variable
        ``RV_TOKEN``
    output : str
        RealValidation API Output. Defaults to ``json``
    url : str
        RealValidation API URL. Defaults to
        ``https://api.realvalidation.com/rpvWebService/DNCLookup.php``
    phone_regex : str
        Regex to use when validating phone numbers. Defaults to ``r'^\d{10}$'``

    """
    DEFAULT_OUTPUT = 'json'
    DEFAULT_URL = 'https://api.realvalidation.com/rpvWebService/DNCLookup.php'

    PHONE_REGEX = r'^\d{10}$'  # 10 numeric digits only

    def _verify_phone(self, phone):
        """Verifies a phone using PHONE_REGEX

        Parameters
        ----------
        phone : str
            Phone to be verified.

        Returns
        -------
        bool
            True if successful, otherwise method raises exception (see below)

        Raises
        ------
        InvalidPhoneFormatException
            If the phone couldn't be verified using PHONE_REGEX

        """
        if re.match(self.phone_regex, phone):
            return True

        raise InvalidPhoneFormatError

    def __init__(self,
                 token=os.environ.get('RV_TOKEN'),
                 output=DEFAULT_OUTPUT,
                 url=DEFAULT_URL,
                 phone_regex=PHONE_REGEX):
        self.log = logging.getLogger(__name__)

        if token is None:
            raise InvalidTokenError

        self.output = output
        self.token = token
        self.url = url
        self.phone_regex = phone_regex

        self.log.debug('<RealValidation {} >'.format(self.__dict__))

    def lookup_phone(self, phone):
        """Makes a request to the RealValidation DNC API

        Parameters
        ----------
        phone : str
            10 numerical digits representing a phone number.

        Returns
        -------
        dict
            Dictionary representing JSON response from RealValidation DNC API.

        """
        self._verify_phone(phone)

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
        except ValueError:
            raise InvalidJSONResponseError

        # if realvalidation RESPONSECODE isn't OK raise error
        if data.get('RESPONSECODE') != 'OK':
            raise ResponseCodeNotOkError

        return data
