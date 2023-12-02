_DATA_PATH = "service_territories/data/"
DISCONNECTION_COUNT_DATA_PATH = _DATA_PATH + "hard_fix_state_september_25.csv"
DISCONNECTION_UTILITY_DATA_PATH = _DATA_PATH + "hard_fix_september_25.csv"
US_STATES_SHAPE_PATH = _DATA_PATH + "us-states-geolocations.json"
US_CENCUS_PATH = _DATA_PATH + "us_census.csv"
NO_DATA_PATH = _DATA_PATH + "No_Data_Prepared.csv"
WRITEUP_PATH = _DATA_PATH + "state-notes.csv"
STATE_PROVIDERS = _DATA_PATH + "state_providers.csv"
COMBINED_PROVIDERS = _DATA_PATH + "combined_providers.csv"


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

YEARS = [1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 
         2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 
         2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023
         ]
MONTHS = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]
INDICATORS = [
    "Number of disconnections",
    "Disconnection rate"
]

SCOPE =[
    "State",
    "Service territories"
]

CITATION_MSG = (
    'When using these data, please cite: Sanya Carley and David Konisky, '
    '2023, "Utility Disconnections Dashboard," Energy Justice Lab'
)
CONTACT_MSG = "For questions about these data, please email: enjlab@indiana.edu"
