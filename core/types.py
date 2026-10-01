from typing import Annotated
from pydantic import Field
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator
from phonenumbers import PhoneNumberFormat

PHONE_NUMBER_TYPE = Annotated[
  PhoneNumber,
  PhoneNumberValidator(
    default_region="IQ",
    number_format="NATIONAL"
  )
]







