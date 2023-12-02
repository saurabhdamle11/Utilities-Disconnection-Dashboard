# Define constant values
_IU_LOGO = "iu_logo.png"
_ABOUT_PAGE_IMAGE = "small-transition.jpg"
_STATES = [
    "Minnesota",
    "North Carolina",
    "New York",
]
_PROTECTION_TYPE = [
    "Cold Protections",
    "Heat-based Protections",
    "Protection for Individuals",
    # 'Administrative Requirements',
    "Procedural Requirements",
]

_POLICY_NAMES = {
    "Cold Protections": ["Cold-based protections", "Date-based protections", "Temperature-based protections"],
    "Heat-based Protections": ["Heat-based protections", "Date-based protections", "Temperature-based protections"],
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
        "Minimum number of days' notice prior to shutoff",
    ],
}

# Options for dropdowns
_YEARS = ["All", 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

_MONTHS = [
    "All",
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

# Define paths to datasets here
# _QUANTIFICATION_DATA = r"H:\My Drive\Utility-Disconnection-Dashboard\Quantification and Vulnerability Protection Data Processing\Quantification Data.csv"
_QUANTIFICATION_DATA = r"~\Utility-Disconnection-Dashboard\Quantification and Vulnerability Protection Data Processing\Quantification Data.csv"
_MINNESOTA_DATA = r"~\Utility-Disconnection-Dashboard\2. Data Preparation\MN\MN_Data_Coordinates_Fixed.geojson"
