params = {
    # 'proparty_list' : ["joy_beach_villa", "the_view_villa"],
    'proparty_list' : ["joy_beach_villa"],
    'url' : "https://www.beds24.com/api/json/getPropertyContent",
    'fields': ["name", "rackRate", "cleaningFee", "securityDeposit","maxPeople", "maxAdult","maxChildren",
                "taxPercentage", "taxPerson", "featureCodes", "minStay", "id"],
    'db_path' : 'db/chroma_db',
    'FIELD_MAP' : {
            "name": "name/title/room_name/villa_name",
            "rackRate": "budget/budget_price/rackRate/price/base_price/rate/room_rate/standard_rate",
            "cleaningFee": "cleaningFee/cleaning_fee/cleaning_charge/service_cleaning_fee",
            "securityDeposit": "securityDeposit/deposit/security_fee/damage_deposit",
            "taxPercentage": "taxPercentage/tax_rate/tax_percentage/tax_percent",
            "taxPerson": "taxPerson/person_tax/tax_per_person/per_person_tax",
            "featureCodes": "featureCodes/features/amenities/facility_codes/room_features",
            "minStay": "minStay/minimum_stay/min_nights/minimum_nights",
        }
}