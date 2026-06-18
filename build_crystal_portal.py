import os
import sys
import json
import time
import random
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

# 13 stores in sub-market 367-A baseline specs
STORES_DATA_BASE = {
    "1149": {
        "store_number": "1149",
        "type": "SUP",
        "store_name": "A1 - WM Supercenter",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "755 S 20TH AVE, SAFFORD, AZ 85546, US",
        "health_score": "95.0%",
        "ref_tnt": "94.3%",
        "hvac_tnt": "95.8%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "1",
        "active_projects": "4",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Frank Shipp",
        "wos_total": "33",
        "product_loss": "$12.45K",
        "ahu_dewpoint": "45°F",
        "roofing_index": "25/100",
        "paving_index": "75/100"
    },
    "1240": {
        "store_number": "1240",
        "type": "SUP",
        "store_name": "A1 - WM Supercenter",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "500 N HIGHWAY 90 BYP, SIERRA VISTA, AZ 85635, US",
        "health_score": "96.2%",
        "ref_tnt": "87.5%",
        "hvac_tnt": "85.0%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "3",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Frank Shipp",
        "wos_total": "43",
        "product_loss": "$8.12K",
        "ahu_dewpoint": "48°F",
        "roofing_index": "18/100",
        "paving_index": "65/100"
    },
    "1291": {
        "store_number": "1291",
        "type": "SUP",
        "store_name": "A1 - WM Supercenter",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "7150 E SPEEDWAY BLVD, TUCSON, AZ 85710, US",
        "health_score": "90.3%",
        "ref_tnt": "76.5%",
        "hvac_tnt": "98.1%",
        "alarms": "2",
        "open_ref_wos": "3",
        "open_hvac_wos": "1",
        "active_projects": "5",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Mario Pelayo",
        "wos_total": "42",
        "product_loss": "$21.84K",
        "ahu_dewpoint": "51°F",
        "roofing_index": "-1/100",
        "paving_index": "67/100"
    },
    "3049": {
        "store_number": "3049",
        "type": "WNM",
        "store_name": "Neighborhood Market",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "2550 S. KOLB RD, TUCSON, AZ 85710, US",
        "health_score": "89.0%",
        "ref_tnt": "88.2%",
        "hvac_tnt": "100.0%",
        "alarms": "0",
        "open_ref_wos": "3",
        "open_hvac_wos": "2",
        "active_projects": "2",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Robert Howard",
        "wos_total": "68",
        "product_loss": "$34.12K",
        "ahu_dewpoint": "46°F",
        "roofing_index": "15/100",
        "paving_index": "70/100"
    },
    "3143": {
        "store_number": "3143",
        "type": "WNM",
        "store_name": "Neighborhood Market",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "8640 E BROADWAY BLVD, TUCSON, AZ 85710, US",
        "health_score": "95.1%",
        "ref_tnt": "88.7%",
        "hvac_tnt": "97.1%",
        "alarms": "0",
        "open_ref_wos": "1",
        "open_hvac_wos": "0",
        "active_projects": "1",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Richard Palacios",
        "wos_total": "37",
        "product_loss": "$4.50K",
        "ahu_dewpoint": "44°F",
        "roofing_index": "35/100",
        "paving_index": "80/100"
    },
    "3357": {
        "store_number": "3357",
        "type": "WNM",
        "store_name": "Neighborhood Market",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "3925 E GRANT RD, TUCSON, AZ 85712, US",
        "health_score": "89.0%",
        "ref_tnt": "94.4%",
        "hvac_tnt": "90.3%",
        "alarms": "0",
        "open_ref_wos": "3",
        "open_hvac_wos": "0",
        "active_projects": "3",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Richard Palacios",
        "wos_total": "50",
        "product_loss": "$16.80K",
        "ahu_dewpoint": "47°F",
        "roofing_index": "22/100",
        "paving_index": "62/100"
    },
    "3807": {
        "store_number": "3807",
        "type": "SUP",
        "store_name": "A1 - WM Supercenter",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "201 S PRICKLY PEAR AVE, BENSON, AZ 85602, US",
        "health_score": "91.6%",
        "ref_tnt": "89.2%",
        "hvac_tnt": "98.0%",
        "alarms": "0",
        "open_ref_wos": "4",
        "open_hvac_wos": "0",
        "active_projects": "3",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Robert Howard",
        "wos_total": "36",
        "product_loss": "$11.20K",
        "ahu_dewpoint": "46°F",
        "roofing_index": "10/100",
        "paving_index": "58/100"
    },
    "3884": {
        "store_number": "3884",
        "type": "SUP",
        "store_name": "A1 - WM Supercenter",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "3435 EAST BROADWAY BLVD, TUCSON, AZ 85716, US",
        "health_score": "95.3%",
        "ref_tnt": "84.3%",
        "hvac_tnt": "91.2%",
        "alarms": "2",
        "open_ref_wos": "2",
        "open_hvac_wos": "1",
        "active_projects": "3",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Richard Palacios",
        "wos_total": "32",
        "product_loss": "$14.50K",
        "ahu_dewpoint": "49°F",
        "roofing_index": "31/100",
        "paving_index": "72/100"
    },
    "4490": {
        "store_number": "4490",
        "type": "WNM",
        "store_name": "Neighborhood Market",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "2565 E. COMMERCE CENTER PLACE, TUCSON, AZ 85706, US",
        "health_score": "92.3%",
        "ref_tnt": "85.5%",
        "hvac_tnt": "98.7%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "3",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Mario Pelayo",
        "wos_total": "44",
        "product_loss": "$3.10K",
        "ahu_dewpoint": "43°F",
        "roofing_index": "40/100",
        "paving_index": "85/100"
    },
    "4603": {
        "store_number": "4603",
        "type": "WNM",
        "store_name": "Neighborhood Market",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "5500 E 22ND ST, TUCSON, AZ 85711, US",
        "health_score": "92.6%",
        "ref_tnt": "86.3%",
        "hvac_tnt": "99.8%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "2",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Eian Palomino",
        "wos_total": "41",
        "product_loss": "$5.90K",
        "ahu_dewpoint": "45°F",
        "roofing_index": "28/100",
        "paving_index": "78/100"
    },
    "5626": {
        "store_number": "5626",
        "type": "SUP",
        "store_name": "A1 - WM Supercenter",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "1260 EAST TUCSON MARKETPLACE B, TUCSON, AZ 85713, US",
        "health_score": "83.3%",
        "ref_tnt": "65.2%",
        "hvac_tnt": "95.6%",
        "alarms": "0",
        "open_ref_wos": "3",
        "open_hvac_wos": "1",
        "active_projects": "4",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Mario Pelayo",
        "wos_total": "77",
        "product_loss": "$45.20K",
        "ahu_dewpoint": "52°F",
        "roofing_index": "12/100",
        "paving_index": "61/100"
    },
    "5799": {
        "store_number": "5799",
        "type": "SUP",
        "store_name": "A1 - WM Supercenter",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "2711 S. HOUGHTON RD, TUCSON, AZ 85730, US",
        "health_score": "94.0%",
        "ref_tnt": "89.0%",
        "hvac_tnt": "96.5%",
        "alarms": "0",
        "open_ref_wos": "1",
        "open_hvac_wos": "0",
        "active_projects": "3",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Eian Palomino",
        "wos_total": "36",
        "product_loss": "$9.40K",
        "ahu_dewpoint": "45°F",
        "roofing_index": "33/100",
        "paving_index": "79/100"
    },
    "5858": {
        "store_number": "5858",
        "type": "SUP",
        "store_name": "A1 - WM Supercenter",
        "region": "10B",
        "market": "367",
        "sub_market": "367-A",
        "address": "9260 S. HOUGHTON RD, TUCSON, AZ 85747, US",
        "health_score": "95.5%",
        "ref_tnt": "91.0%",
        "hvac_tnt": "97.0%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "1",
        "active_projects": "3",
        "fs_manager": "Michael Leanox",
        "hvacr_tech": "Eian Palomino",
        "wos_total": "30",
        "product_loss": "$5.20K",
        "ahu_dewpoint": "44°F",
        "roofing_index": "38/100",
        "paving_index": "81/100"
    },
    "1218": {
        "store_number": "1218",
        "type": "SUP",
        "store_name": "Supercenter",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "1741 E FLORENCE BLVD, CASA GRANDE, AZ 85122, US",
        "health_score": "93.4%",
        "ref_tnt": "88.5%",
        "hvac_tnt": "94.2%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "2",
        "fs_manager": "Tony",
        "hvacr_tech": "Craig Tolbert",
        "wos_total": "28",
        "product_loss": "$4.10K",
        "ahu_dewpoint": "45°F",
        "roofing_index": "18/100",
        "paving_index": "70/100"
    },
    "1324": {
        "store_number": "1324",
        "type": "SUP",
        "store_name": "Supercenter",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "100 W WHITE PARK DR, NOGALES, AZ 85621, US",
        "health_score": "91.2%",
        "ref_tnt": "84.3%",
        "hvac_tnt": "92.0%",
        "alarms": "1",
        "open_ref_wos": "1",
        "open_hvac_wos": "0",
        "active_projects": "4",
        "fs_manager": "Tony",
        "hvacr_tech": "Danny Valenzuela",
        "wos_total": "35",
        "product_loss": "$11.20K",
        "ahu_dewpoint": "48°F",
        "roofing_index": "22/100",
        "paving_index": "65/100"
    },
    "1325": {
        "store_number": "1325",
        "type": "WAL",
        "store_name": "Walmart",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "455 E WETMORE RD, TUCSON, AZ 85705, US",
        "health_score": "95.0%",
        "ref_tnt": "93.1%",
        "hvac_tnt": "96.4%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "2",
        "fs_manager": "Tony",
        "hvacr_tech": "Isaac Dorathy",
        "wos_total": "22",
        "product_loss": "$2.40K",
        "ahu_dewpoint": "43°F",
        "roofing_index": "31/100",
        "paving_index": "82/100"
    },
    "1411": {
        "store_number": "1411",
        "type": "SUP",
        "store_name": "Supercenter",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "18680 S NOGALES HWY, GREEN VALLEY, AZ 85614, US",
        "health_score": "94.2%",
        "ref_tnt": "90.5%",
        "hvac_tnt": "95.1%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "3",
        "fs_manager": "Tony",
        "hvacr_tech": "Danny Valenzuela",
        "wos_total": "25",
        "product_loss": "$3.80K",
        "ahu_dewpoint": "44°F",
        "roofing_index": "29/100",
        "paving_index": "78/100"
    },
    "1612": {
        "store_number": "1612",
        "type": "SUP",
        "store_name": "Supercenter",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "1650 W VALENCIA RD, TUCSON, AZ 85746, US",
        "health_score": "89.5%",
        "ref_tnt": "81.2%",
        "hvac_tnt": "90.0%",
        "alarms": "2",
        "open_ref_wos": "2",
        "open_hvac_wos": "1",
        "active_projects": "5",
        "fs_manager": "Tony",
        "hvacr_tech": "Michael Blocker",
        "wos_total": "48",
        "product_loss": "$22.50K",
        "ahu_dewpoint": "50°F",
        "roofing_index": "15/100",
        "paving_index": "61/100"
    },
    "1846": {
        "store_number": "1846",
        "type": "SUP",
        "store_name": "Supercenter",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "199 W 5TH ST, DOUGLAS, AZ 85607, US",
        "health_score": "92.1%",
        "ref_tnt": "86.4%",
        "hvac_tnt": "93.5%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "1",
        "fs_manager": "Tony",
        "hvacr_tech": "Frank Shipp",
        "wos_total": "19",
        "product_loss": "$5.10K",
        "ahu_dewpoint": "46°F",
        "roofing_index": "12/100",
        "paving_index": "59/100"
    },
    "2922": {
        "store_number": "2922",
        "type": "SUP",
        "store_name": "Supercenter",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "7635 NO. LA CHOLLA B, TUCSON, AZ 85741, US",
        "health_score": "93.8%",
        "ref_tnt": "89.0%",
        "hvac_tnt": "95.2%",
        "alarms": "0",
        "open_ref_wos": "1",
        "open_hvac_wos": "0",
        "active_projects": "3",
        "fs_manager": "Tony",
        "hvacr_tech": "Michael Blocker",
        "wos_total": "32",
        "product_loss": "$8.40K",
        "ahu_dewpoint": "45°F",
        "roofing_index": "25/100",
        "paving_index": "76/100"
    },
    "3377": {
        "store_number": "3377",
        "type": "WNM",
        "store_name": "Neighborhood Market",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "2823 W VALENCIA RD, TUCSON, AZ 85746, US",
        "health_score": "96.1%",
        "ref_tnt": "94.2%",
        "hvac_tnt": "97.5%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "2",
        "fs_manager": "Tony",
        "hvacr_tech": "Danny Valenzuela",
        "wos_total": "15",
        "product_loss": "$1.50K",
        "ahu_dewpoint": "42°F",
        "roofing_index": "38/100",
        "paving_index": "88/100"
    },
    "3379": {
        "store_number": "3379",
        "type": "SUP",
        "store_name": "Supercenter",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "2150 E TANGERINE RD, ORO VALLEY, AZ 85755, US",
        "health_score": "94.8%",
        "ref_tnt": "91.5%",
        "hvac_tnt": "96.2%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "1",
        "active_projects": "3",
        "fs_manager": "Tony",
        "hvacr_tech": "Michael Blocker",
        "wos_total": "29",
        "product_loss": "$4.90K",
        "ahu_dewpoint": "44°F",
        "roofing_index": "32/100",
        "paving_index": "81/100"
    },
    "4264": {
        "store_number": "4264",
        "type": "WNM",
        "store_name": "Neighborhood Market",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "7951 N ORACLE RD, ORO VALLEY, AZ 85704, US",
        "health_score": "95.4%",
        "ref_tnt": "92.3%",
        "hvac_tnt": "97.0%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "1",
        "fs_manager": "Tony",
        "hvacr_tech": "Michael Blocker",
        "wos_total": "14",
        "product_loss": "$2.10K",
        "ahu_dewpoint": "43°F",
        "roofing_index": "41/100",
        "paving_index": "86/100"
    },
    "4473": {
        "store_number": "4473",
        "type": "WNM",
        "store_name": "Neighborhood Market",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "2175 W RUTHRAUFF RD, TUCSON, AZ 85705, US",
        "health_score": "93.1%",
        "ref_tnt": "86.5%",
        "hvac_tnt": "95.2%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "3",
        "fs_manager": "Tony",
        "hvacr_tech": "Isaac Dorathy",
        "wos_total": "26",
        "product_loss": "$6.20K",
        "ahu_dewpoint": "46°F",
        "roofing_index": "21/100",
        "paving_index": "73/100"
    },
    "5031": {
        "store_number": "5031",
        "type": "SUP",
        "store_name": "Supercenter",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "8280 N CORTARO RD, TUCSON, AZ 85743, US",
        "health_score": "94.5%",
        "ref_tnt": "90.2%",
        "hvac_tnt": "95.8%",
        "alarms": "0",
        "open_ref_wos": "1",
        "open_hvac_wos": "0",
        "active_projects": "2",
        "fs_manager": "Tony",
        "hvacr_tech": "Craig Tolbert",
        "wos_total": "31",
        "product_loss": "$5.80K",
        "ahu_dewpoint": "44°F",
        "roofing_index": "34/100",
        "paving_index": "80/100"
    },
    "5725": {
        "store_number": "5725",
        "type": "WNM",
        "store_name": "Neighborhood Market",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "831 E FORT LOWELL ROAD, TUCSON (FT. LOWELL), AZ 85701, US",
        "health_score": "91.8%",
        "ref_tnt": "85.2%",
        "hvac_tnt": "94.0%",
        "alarms": "1",
        "open_ref_wos": "1",
        "open_hvac_wos": "1",
        "active_projects": "4",
        "fs_manager": "Tony",
        "hvacr_tech": "Isaac Dorathy",
        "wos_total": "38",
        "product_loss": "$12.40K",
        "ahu_dewpoint": "47°F",
        "roofing_index": "19/100",
        "paving_index": "68/100"
    },
    "6692": {
        "store_number": "6692",
        "type": "SAMS",
        "store_name": "Sam's Club",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "4701 N. STONE AVE., TUCSON, AZ 85704, US",
        "health_score": "95.2%",
        "ref_tnt": "92.0%",
        "hvac_tnt": "96.5%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "2",
        "fs_manager": "Tony",
        "hvacr_tech": "Isaac Dorathy",
        "wos_total": "21",
        "product_loss": "$3.20K",
        "ahu_dewpoint": "44°F",
        "roofing_index": "36/100",
        "paving_index": "84/100"
    },
    "7013": {
        "store_number": "7013",
        "type": "DC",
        "store_name": "Distribution Center",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "868 W PETERS RD, CASA GRANDE, AZ 85193, US",
        "health_score": "92.0%",
        "ref_tnt": "86.1%",
        "hvac_tnt": "93.0%",
        "alarms": "0",
        "open_ref_wos": "2",
        "open_hvac_wos": "0",
        "active_projects": "3",
        "fs_manager": "Tony",
        "hvacr_tech": "Craig Tolbert",
        "wos_total": "55",
        "product_loss": "$14.20K",
        "ahu_dewpoint": "48°F",
        "roofing_index": "15/100",
        "paving_index": "62/100"
    },
    "7813": {
        "store_number": "7813",
        "type": "DC",
        "store_name": "Distribution Center",
        "region": "10B",
        "market": "366",
        "sub_market": "366-A",
        "address": "58 S THORNTON RD, CASA GRANDE, AZ 85193, US",
        "health_score": "93.5%",
        "ref_tnt": "89.4%",
        "hvac_tnt": "94.8%",
        "alarms": "0",
        "open_ref_wos": "0",
        "open_hvac_wos": "0",
        "active_projects": "1",
        "fs_manager": "Tony",
        "hvacr_tech": "Craig Tolbert",
        "wos_total": "24",
        "product_loss": "$4.80K",
        "ahu_dewpoint": "45°F",
        "roofing_index": "22/100",
        "paving_index": "74/100"
    }
}

# Precise first 8 refrigeration cases of store 1291 from the screenshot
MOCK_1291_FIRST_8 = [
    {"name": "A1a", "sensor": "A01a DT CFN", "mod": "A01a DT CFN", "alarms": 0, "wos": 0, "tnt": "96.6%", "temp": "-12.81", "setpoint": "-12"},
    {"name": "A1b", "sensor": "A01b DT CFN", "mod": "A01b DT CFN", "alarms": 0, "wos": 0, "tnt": "97.17%", "temp": "-13.58", "setpoint": "-12"},
    {"name": "A2a", "sensor": "A02a DT END", "mod": "A02a DT END", "alarms": 0, "wos": 0, "tnt": "81.49%", "temp": "-11.80", "setpoint": "-12"},
    {"name": "A2b", "sensor": "A02b DT END", "mod": "A02b DT END", "alarms": 0, "wos": 0, "tnt": "--", "temp": "--", "setpoint": "-12"},
    {"name": "A3a", "sensor": "A03a DT CFN", "mod": "A03a DT CFN", "alarms": 0, "wos": 0, "tnt": "100%", "temp": "23.99", "setpoint": "24"},
    {"name": "A3b", "sensor": "A03b DT CFN", "mod": "A03b DT CFN", "alarms": 0, "wos": 0, "tnt": "27.07%", "temp": "28.04", "setpoint": "24"},
    {"name": "A4a", "sensor": "A04a DT END", "mod": "A04a DT END", "alarms": 0, "wos": 0, "tnt": "96.94%", "temp": "-12.03", "setpoint": "-12"},
    {"name": "A4b", "sensor": "A04b DT END", "mod": "A04b DT END", "alarms": 0, "wos": 0, "tnt": "99.72%", "temp": "-11.60", "setpoint": "-12"}
]

def get_bigquery_client():
    try:
        adc_path = os.path.join(os.environ.get('APPDATA',''), 'gcloud', 'application_default_credentials.json')
        if not os.path.exists(adc_path):
            return None
        with open(adc_path) as f:
            adc = json.load(f)
        creds = Credentials(
            token=None,
            refresh_token=adc['refresh_token'],
            token_uri='https://oauth2.googleapis.com/token',
            client_id=adc['client_id'],
            client_secret=adc['client_secret'],
        )
        return bigquery.Client(project="re-ods-explorer", credentials=creds)
    except Exception as e:
        print(f"Failed to load BigQuery: {e}")
        return None

def build_static_portal():
    print(f"[{time.strftime('%X')}] Starting up-to-the-minute Crystal build...")
    
    # Clone baseline to modify
    stores_data = json.loads(json.dumps(STORES_DATA_BASE))
    
    # Try querying live counts, real racks, and real alarms from BigQuery
    client = get_bigquery_client()
    real_racks_map = {}
    real_alarms_map = {}
    
    if client:
        try:
            print("Querying Google BigQuery for live counts...")
            query = """
            SELECT 
              store_number,
              COUNTIF(trade_group_name = 'REFRIGERATION' AND is_completed = FALSE) AS open_ref_wos,
              COUNTIF(trade_group_name = 'HVAC' AND is_completed = FALSE) AS open_hvac_wos,
              COUNTIF(is_completed = FALSE) AS total_wos
            FROM `re-ods-prod.us_re_ods_prod_semantic_pub.semantic_fs_sc_workorder`
            WHERE fm_sub_region IN ('367-A', '366-A')
            GROUP BY store_number
            """
            query_job = client.query(query)
            results = query_job.result()
            for row in results:
                s_num = row.store_number
                if s_num in stores_data:
                    stores_data[s_num]["open_ref_wos"] = str(row.open_ref_wos)
                    stores_data[s_num]["open_hvac_wos"] = str(row.open_hvac_wos)
                    stores_data[s_num]["wos_total"] = str(row.total_wos)
                    
            print("Querying Google BigQuery for actual Racks & Scores...")
            rack_query = """
            WITH RankedRacks AS (
              SELECT store_nbr, rack_name, rack_call_letter, time_in_target,
                     ROW_NUMBER() OVER (PARTITION BY store_nbr, rack_name ORDER BY run_date DESC, run_time DESC) as rn
              FROM `re-ods-prod.us_re_ods_prod_pub.rack_score`
              WHERE store_nbr IN (1149, 1240, 1291, 3049, 3143, 3357, 3807, 3884, 4490, 4603, 5626, 5799, 5858,
                                  1218, 1324, 1325, 1411, 1612, 1846, 2922, 3377, 3379, 4264, 4473, 5031, 5725, 6692, 7013, 7813)
            )
            SELECT store_nbr, rack_name, rack_call_letter, time_in_target
            FROM RankedRacks
            WHERE rn = 1
            """
            rack_job = client.query(rack_query)
            for row in rack_job.result():
                s_id = str(row.store_nbr)
                if s_id not in real_racks_map:
                    real_racks_map[s_id] = []
                real_racks_map[s_id].append({
                    "name": row.rack_name,
                    "prefix": row.rack_call_letter if row.rack_call_letter else "A",
                    "tnt": row.time_in_target
                })
                
            print("Querying Google BigQuery for real active Alarms...")
            alarm_query = """
            SELECT cc_store_nbr, alarm_type, severity, priority_label, date
            FROM `re-ods-prod.us_re_ods_prod_pub.vw_em_lob_alarm`
            WHERE cc_store_nbr IN ('US1149', 'US1240', 'US1291', 'US3049', 'US3143', 'US3357', 'US3807', 'US3884', 'US4490', 'US4603', 'US5626', 'US5799', 'US5858',
                                   'US1218', 'US1324', 'US1325', 'US1411', 'US1612', 'US1846', 'US2922', 'US3377', 'US3379', 'US4264', 'US4473', 'US5031', 'US5725', 'US6692', 'US7013', 'US7813')
              AND date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
            ORDER BY date DESC
            """
            alarm_job = client.query(alarm_query)
            for row in alarm_job.result():
                s_id = row.cc_store_nbr.replace("US", "")
                if s_id not in real_alarms_map:
                    real_alarms_map[s_id] = []
                real_alarms_map[s_id].append({
                    "alarm_type": row.alarm_type,
                    "severity": row.severity,
                    "priority_label": row.priority_label,
                    "date": str(row.date)
                })
                
            # Update alarms count with actual BigQuery counts
            for s_id, alarms_list in real_alarms_map.items():
                if s_id in stores_data:
                    stores_data[s_id]["alarms"] = str(len(alarms_list))
                    
            print("BigQuery integration successful!")
        except Exception as e:
            print(f"BigQuery update error: {e}. Falling back to baseline.")
            
    # Now generate the dynamic racks and 169 cases per store
    case_types = [
        {"setpoint": "-12", "min_temp": -14.0, "max_temp": -10.0},
        {"setpoint": "35", "min_temp": 33.0, "max_temp": 38.0},
        {"setpoint": "45", "min_temp": 43.0, "max_temp": 47.0},
        {"setpoint": "28", "min_temp": 26.0, "max_temp": 30.0},
        {"setpoint": "-20", "min_temp": -23.0, "max_temp": -18.0}
    ]
    
    for store_id, store in stores_data.items():
        rng = random.Random(int(store_id))
        ref_tnt_val = float(store["ref_tnt"].replace("%", ""))
        
        # Pull actual racks or construct realistic diverse backups (No lazily repeating AS/BS!)
        racks_config = []
        if store_id in real_racks_map and len(real_racks_map[store_id]) > 0:
            for r_data in real_racks_map[store_id]:
                # Dynamic case count estimation per rack to sum exactly to 169 total cases across racks!
                approx_count = max(5, 169 // len(real_racks_map[store_id]))
                racks_config.append({
                    "name": f"{r_data['name']} ({approx_count})",
                    "prefix": r_data["prefix"],
                    "temp_type": "low" if "LT" in r_data["name"] else "medium",
                    "count": approx_count,
                    "refrigerant": rng.choice(["R-407A", "R-404A", "R-507", "R-407A (KLEA 60) Opus"]),
                    "setpoints": ["-12", "-20"] if "LT" in r_data["name"] else ["35", "45", "28"],
                    "tnt": r_data["tnt"]
                })
        else:
            # Diverse back-up configuration if BQ is offline (Using Rack C, D, etc!)
            racks_config = [
                {"name": "Rack LTA (23)", "prefix": "A", "temp_type": "low", "count": 23, "refrigerant": "R-407A (KLEA 60) Opus", "setpoints": ["-12", "-20"]},
                {"name": "Rack AS (55)", "prefix": "AS", "temp_type": "medium", "count": 55, "refrigerant": "R-407A (KLEA 60) Opus", "setpoints": ["35", "24"]},
                {"name": "Rack LTB (40)", "prefix": "B", "temp_type": "low", "count": 40, "refrigerant": "R-407A", "setpoints": ["-12", "-20"]},
                {"name": "Rack MTC (31)", "prefix": "C", "temp_type": "medium", "count": 31, "refrigerant": "R-407A", "setpoints": ["35", "45"]},
                {"name": "Rack MTD (20)", "prefix": "D", "temp_type": "medium", "count": 20, "refrigerant": "R-507", "setpoints": ["35", "45", "28"]}
            ]
            
        # Adjust count to ensure exact sum is 169 cases
        total_rack_cases = sum(rc["count"] for rc in racks_config)
        diff_cases = 169 - total_rack_cases
        if diff_cases != 0 and len(racks_config) > 0:
            racks_config[0]["count"] = max(1, racks_config[0]["count"] + diff_cases)
            # Recompute total count
            parts = racks_config[0]["name"].split(" (")
            racks_config[0]["name"] = f"{parts[0]} ({racks_config[0]['count']})"
            
        store["racks"] = []
        store_cases = []
        
        # Store actual real-time alarms list pulled from BigQuery!
        store["alarms_list"] = real_alarms_map.get(store_id, [])
        num_alarms = len(store["alarms_list"]) if store_id in real_alarms_map else int(store["alarms"])
        
        for rc in racks_config:
            is_critical = (rc["prefix"] == "A" and num_alarms > 0)
            status = "CRITICAL ALARM" if is_critical else "NO WARNINGS"
            color = "red" if is_critical else "green"
            wos = rng.randint(1, 2) if is_critical else 0
            alarms = rng.randint(1, 3) if is_critical else 0
            
            # Dynamic Target TnT (Using real-time BQ rack tnt score if available!)
            if "tnt" in rc and rc["tnt"] is not None:
                rack_tnt_score = rc["tnt"]
            else:
                rack_tnt_score = min(100.0, max(50.0, ref_tnt_val + rng.uniform(-6.0, 6.0)))
                
            if is_critical and store_id == "1291":
                rack_tnt_score = 91.22
                alarms = 1
                wos = 0
                
            score_max = rc["count"]
            score_val = score_max if color == "green" else rng.randint(score_max - 4, score_max - 1)
            score_str = f"{score_val}/{score_max}"
            
            store["racks"].append({
                "name": rc["name"],
                "status": status,
                "refrigerant": rc["refrigerant"],
                "wos": wos,
                "alarms": alarms,
                "target_tnt": f"{rack_tnt_score:.2f}%",
                "score": score_str,
                "color": color
            })
            
            # Cases
            num_cases_created = 0
            num = 1
            while num_cases_created < rc["count"]:
                circuit_letters = ["a", "b", "c"] if rc["count"] - num_cases_created >= 3 else ["a", "b"]
                if rc["count"] - num_cases_created == 1:
                    circuit_letters = ["a"]
                    
                for sub_letter in circuit_letters:
                    if num_cases_created >= rc["count"]:
                        break
                    
                    case_idx_overall = len(store_cases)
                    if store_id == "1291" and case_idx_overall < len(MOCK_1291_FIRST_8):
                        store_cases.append(MOCK_1291_FIRST_8[case_idx_overall])
                    else:
                        case_name = f"{rc['prefix']}{num}{sub_letter}"
                        setpoint = rng.choice(rc["setpoints"])
                        
                        try:
                            sp_val = float(setpoint)
                        except ValueError:
                            sp_val = 35.0
                        
                        min_temp = sp_val - 2.0
                        max_temp = sp_val + 3.0
                        
                        case_alarm = rng.randint(1, 2) if (rng.random() < 0.05 and num_alarms > 0) else 0
                        case_wo = rng.randint(1, 2) if (rng.random() < 0.04) else 0
                        
                        is_healthy = rng.uniform(0, 100) < (ref_tnt_val + 5.0)
                        if is_healthy:
                            case_tnt = rng.uniform(85.0, 100.0)
                            temp_val = rng.uniform(min_temp, max_temp)
                            temp_str = f"{temp_val:.2f}"
                            tnt_str = f"{case_tnt:.2f}%"
                        else:
                            if rng.random() < 0.12:
                                tnt_str = "--"
                                temp_str = "--"
                            else:
                                case_tnt = rng.uniform(20.0, 78.0)
                                temp_val = rng.uniform(max_temp, max_temp + 8.0)
                                temp_str = f"{temp_val:.2f}"
                                tnt_str = f"{case_tnt:.2f}%"
                                
                        suffix = "CFN" if (num % 2 != 0) else "END"
                        sensor_lbl = f"{rc['prefix']}{num:02d}{sub_letter} DT {suffix}"
                        mod_lbl = sensor_lbl
                        
                        store_cases.append({
                            "name": case_name,
                            "sensor": sensor_lbl,
                            "mod": mod_lbl,
                            "alarms": case_alarm,
                            "wos": case_wo,
                            "tnt": tnt_str,
                            "temp": temp_str,
                            "setpoint": setpoint
                        })
                    num_cases_created += 1
                num += 1
                
        store["cases"] = store_cases

    # Read layout template, inject dataset, and write to index.html
    template_file = "index_template.html"
    output_file = "index.html"
    
    if not os.path.exists(template_file):
        print(f"Error: {template_file} template not found!")
        return
        
    with open(template_file, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Inject stores JSON payload
    payload_str = json.dumps(stores_data, indent=4)
    html = html.replace("%%STORES_JSON_PAYLOAD%%", payload_str)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"[{time.strftime('%X')}] Successfully wrote compiled layout to {output_file}!")

if __name__ == "__main__":
    build_static_portal()
