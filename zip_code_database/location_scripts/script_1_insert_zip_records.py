import json
from tqdm import tqdm

from zip_code_database.functions import mongodb_functions
from zip_code_database.functions import geo_functions

# printed out in console and copied
duplication_zip_codes = [
    '97839', '53547', '24407', '79106', '54331', '40211', '89604', '50667', '44799',
    '18356', '41747', '57539', '56355', '99819', '27755', '01127', '41069', '17438',
    '56288', '26954', '16230', '86465', '18445', '67745', '70439', '38154', '97320',
    '10623', '17493', '41748', '25491', '67808', '73469', '16818', '56132', '37447',
    '54441', '25377', '67256', '17337', '66903', '17099', '23966', '54570', '99099',
    '78479', '55608', '55758', '56424', '56472', '26571', '67822', '06667', '79117',
    '67273', '21244', '30161', '57520', '88709', '78333', '87648', '22946', '18565',
    '76831', '54295', '95163', '49459', '56346', '50939', '24799', '88471', '16845',
    '23845', '99897', '70771', '67742', '18573', '90455', '14558', '67744', '78052',
    '54413', '38642', '56859', '12305', '22113', '67271', '06542', '17375', '56244',
    '93426', '74597', '06536', '17440', '95485', '37197', '39343', '71397', '37170',
    '07751', '63916', '72766', '09117', '22844', '50735', '31789', '72764', '74354',
    '92265', '95460', '52152', '67753', '98711', '71672', '56242', '21423', '14778',
    '44577', '74426', '77880', '56412', '78089', '56858', '72108', '27356', '66989',
    '37412', '22929', '45897', '18374', '07980', '76835', '06493', '57629', '24405',
    '67483', '76646', '01465', '66987', '97640', '83487', '88457', '17489', '67591',
    '06729', '23881', '89605', '57627', '22453', '21444', '54298', '53520', '52159',
    '28755', '52156', '19322', '04617', '55566', '95505', '12559', '55459', '12059',
    '81545', '33609', '54657', '56843', '55606', '18569', '07919', '41063', '55270',
    '21391', '54317', '56814', '25776', '79364', '23911', '76829', '65558', '27499',
    '12107', '55483', '91477', '26909', '56070', '72762', '19348', '72145', '79110',
    '56348', '55585', '44867', '54472', '57642', '75397', '56269', '18439', '55288',
    '31084', '66851', '72141', '06888', '14476', '56370', '06369', '55232', '66887',
    '66999', '22457', '17322', '79395', '72657', '54456', '54340', '76848', '66484',
    '56307', '55437', '98559', '56379', '31079', '88662', '06842', '67661', '12685',
    '67724', '55595', '37247', '21502', '29364', '15345', '97618', '06772', '71069',
    '91093', '41061', '56753', '33330', '95503', '01855', '30159', '50170', '69181',
    '17039', '97638', '73497', '01257', '82401', '72296', '72663', '18317', '78628',
    '25718', '52222', '73257', '54597', '34289', '25845', '91338', '37691', '17449',
    '15518', '23946', '06862', '55278', '15831', '56283', '17237', '39448', '67067',
    '38644', '74670', '22609', '12623', '72250', '79595', '97348', '55765', '44623',
    '44801', '54578', '28329', '66996', '91341', '22889', '55471', '06647', '25859',
    '88379', '27330', '19372', '07551', '92266', '21723', '54411', '01069', '06528',
    '90411', '12679', '56761', '55599', '56332', '04603', '67759', '18581', '78166',
    '39599', '07318', '89584', '56867', '79108', '67468', '08523', '21516', '54552',
    '99198', '09437', '27578', '76855', '56220', '74532', '66871', '37085', '67693',
    '93197', '39517', '89168', '67482', '78465', '07389', '89542', '64646', '22415',
    '93109', '15236', '76887', '99102', '54533', '34399', '66957', '66909', '69412',
    '22767', '88512', '79115', '24891', '55234', '74321', '27498', '29396', '71063',
    '55452', '79423', '23769', '55767', '63801', '89081', '19055', '59425', '25849',
    '73107', '81927', '95694', '06268', '63936', '67489', '54426', '37445', '25869',
    '02627', '48432', '07778', '67480', '18211', '67377', '09600', '90471', '56271',
    '16306'
]

duplication_zip_code_cities = {}


with open('../data/postleitzahlen-deutschland.json') as json_file:
    zip_records = json.load(json_file)
    # print(type(zip_records))
    print(f"{len(zip_records)} records.\n")

    batch_to_be_added = []

    for zip_record in tqdm(zip_records):
        try:
            zip_code = zip_record["fields"]["plz"]
            city = zip_record["fields"]["note"]

            if zip_code in duplication_zip_codes:
                duplication_zip_code_cities.update({zip_code: city})
                continue

            lat = round(zip_record["fields"]["geo_point_2d"][0], 7)
            lng = round(zip_record["fields"]["geo_point_2d"][1], 7)

            # print(json.dumps(zip_record, indent=4))
            # print({"zip_code": zip_code, "city": city, "lat": lat, "lng": lng})

            batch_to_be_added.append(mongodb_functions.format_zip_record_dict(zip_code, city, lat, lng))

            if len(batch_to_be_added) == 100:
                mongodb_functions.mongodb_add_zip_record_dict_batch(batch_to_be_added)
                batch_to_be_added = []
        except KeyError as e:
            print(e)
            print(json.dumps(zip_record, indent=4))

    if len(batch_to_be_added) != 0:
        mongodb_functions.mongodb_add_zip_record_dict_batch(batch_to_be_added)
        batch_to_be_added = []


for zip_code in tqdm(duplication_zip_codes):
    geocode_result = geo_functions.get_geocode_location(zip_code=zip_code)

    if geocode_result["status"] == "ok":
        city = duplication_zip_code_cities[zip_code]
        lat = geocode_result["lat"]
        lng = geocode_result["lng"]
        batch_to_be_added.append(mongodb_functions.format_zip_record_dict(zip_code, city, lat, lng))
    else:
        geocode_result.update({"zip_code": zip_code})
        print(geocode_result)

mongodb_functions.mongodb_add_zip_record_dict_batch(batch_to_be_added)





"""
Not location with:
    32351 Stemwede
    32369 Rahden


GCP Geocode Result:

    32351 Stemwede, Deutschland:
        request: https://maps.googleapis.com/maps/api/geocode/json?address=32351+Stemwede,Deutschland&key=<KEY>
        lat: 52.4204498
        lng:  8.4766636
        
    32369 Rahden, Deutschland:
        request: https://maps.googleapis.com/maps/api/geocode/json?address=32369+Rahden,Deutschland&key=<KEY>
        lat: 52.4543743
        lng:  8.6008636


Inserting into DB:
    {
        "_id": {
            "$oid": <id>
        },
        "zip_code": "32351",
        "city": "Stemwede",
        "lat": 52.4204498,
        "lng":  8.4766636,
        "adjacent_zip_codes": []
    }
    {
        "_id": {
            "$oid": <id>
        },
        "zip_code": "32369",
        "city": "Rahden",
        "lat": 52.4543743,
        "lng":  8.6008636,
        "adjacent_zip_codes": []
    }


"""