_DATA_PATH = "disconnection_policies/data/"
COLD_PROTECTIONS_PATH = _DATA_PATH + "cold_protections_data.csv"
HEAT_PROTECTIONS_PATH = _DATA_PATH + "heat_protections_data.csv"
INDIVIDUAL_PROTECTIONS_PATH = _DATA_PATH + "individual_protections_data.csv"
PROCEDURAL_REQUIREMENTS_PATH = _DATA_PATH + "procedural_requirements_data.csv"
# ADMINISTRATIVE_REQUIREMENTS_PATH = _DATA_PATH + "administrative_requirements_data.csv"
POLICY_WRITEUP_PATH = _DATA_PATH + "Policies_Sheet.csv"
US_STATES_SHAPE_PATH = _DATA_PATH + "us-states-geolocations.json"

STATE_CODE_TO_NAME = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "Washington, D.C.",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}
STATE_CODES = list(STATE_CODE_TO_NAME.keys())

POLICY_NAMES = {
    "Cold-based Protections": [
        "Cold-based protections",
        "Date-based protections",
        "Temperature-based protections"
    ],
    "Heat-based Protections": [
        "Heat-based protections",
        "Date-based protections",
        "Temperature-based protections"
    ],
    "Protection for Individuals": [
        "Young Individuals",
        "Medical Condition Individuals",
        "Elderly People",
        "Individuals with Disabilities",
        "Military Veterans",
    ],
    # 'Administrative Requirements': [
    #     'Utilities exempt from the state disconnection policies',
    #     'Payment plan availability'
    # ],
    "Procedural Requirements": [
        "Must a utility provide written notice?",
        "Must a utility attempt in-person notification?",
        "Must a utility attempt notice by phone?",
        #"Minimum number of days' notice prior to shutoff",
    ],
}
PROTECTION_TYPE = list(POLICY_NAMES.keys())

CITATION_MSG = (
    'When using these data, please cite: Sanya Carley and David Konisky, '
    '2023, "Utility Disconnections Dashboard," Energy Justice Lab'
)
CONTACT_MSG = "For questions about these data, please email: enjlab@indiana.edu"
