from permit import Permit
from constants import PERMIT_API_KEY, PERMIT_PDP_URL


# This line initializes the SDK and connects your python app
# to the Permit.io PDP container you've set up.
permit = Permit(
    # in production, you might need to change this url to fit your deployment
    pdp=PERMIT_PDP_URL,
    # your secret API KEY
    token=PERMIT_API_KEY,
)
