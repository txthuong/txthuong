#!/bin/env python
# _*_ coding: utf-8 _*_


#----------------------------------------------------------------------------
# Name:			VarGlobal.py
#
# Goal:			Contains all shared variables by modules Test, ComModuleAPI and MainFrame
#
# Author:		refer below
#
# Version:		refer below
#
# Date:			refer below
#
# Property:		SagemComm
#----------------------------------------------------------------------------


#date              who                 version                 modification
#04->09-2007       Bingxun HOU         1.0                     creation
#22-09-2011        JF Weiss            1.8.1                   add comments and light modifications
#                                                              add GlobalIsSystemStopWhenhComFails
#                                                              add DEBUG_LEVEL for printing (or not) debug logs on autotest
#                                                              a logger should be implemented quickly
#28-02-2012        JM Seillon          1.8.2                   use VERSION fo GNSS
#Avril 2012         JM Seillon          1.8.3                  Add global variables MRM, GNSS_flag
#xx-05-2012        JM Seillon           1.8.6                  change VERSION
#28-06-2012        JM Seillon           1.8.7                  change VERSION
#26-07-2012        JM Seillon           1.9.0                  change VERSION
#26-07-2012        JM Seillon           1.9.1                  change VERSION
#13-09-2012        SII (MR)             1.9.2                  change VERSION
#18-12-2012        JFWeiss              1.9.3                  change VERSION
#02-04-2013        JFWeiss              1.9.4  
#26-04-2013        EBARRE               1.9.5                 change VERSION
#xx-03-2013        Gary Zhang          1.9.6                   advanced MUX
#
#
#import ExcelDoc
import os

# Variable pour process
process_stat = ''

VERSION = "1.9.6.28"

#v1.8.1 CR2816 variable IsSystemStopWhenhComFails
#This varaible has been added for Femto team ; they don't wish the system stop is hCom fails to be opened
#To avoid adding another argument when launching Autotest, a new method is added in API and Femto team must use it
#first
IsSystemStopsWhenhComFails = True

MRM = None
GNSS_flag = False
#+ Advanced mode support
AdvancedMode = False
#- Advanced mode support

# Variable for log
numOfCommand = 0.0
numOfTest = 0.0
numOfSuccessfulTest = 0.0 
numOfFailedTest = 0.0
numOfCommand = 0.0
numOfResponse = 0.0
numOfSuccessfulResponse = 0.0 
numOfFailedResponse = 0.0

# Variable for excel
excelDoc = None 
statOfItem = ''
excelComment = ''
excelCommentGlobal = ''
#VarGlobal.excelComment
#VarGlobal.excelCommentGlobal

# Array to memorize test position in log_tc
posInLog = []

# variable to memorize current directory
directory = os.getcwd()

# Constant for execution type : Normal, Demo
NORMAL_MODE = 0
DEMO_MODE = 1
MODE = NORMAL_MODE	# normal mode

#debug level for printing (or not) debug logs in  autotest window
#DEBUG_LEVEL = "DEBUG"
DEBUG_LEVEL = "ERROR"

# PLMN list
PLMN_dict = {6320: "Digicel", 36301: "SETAR GSM", 41201: "AF AWCC", 41240: "AREEBA", 41250: "Etisalat Af", 41220: "ROSHAN", 63102: "UNITEL", 365840: "Cable&Wireless",
			27601: "AL AMC", 27602: "vodafone AL", 21303: "AND M-AND", 36269: "Digicel", 362951: "CHIPPIE", 36251: "Telcell GSM", 42403: "du", 42402: "ETISALAT",
			722310: "CTI Argentina", 72234: "AR TP", 72207: "movistar", 28301: "Beeline AM", 28305: "RA 05", 344030: "APUA-PCS", 344930: "Cingular",
			344920: "Cable&Wireless", 50506: "3TELSTRA", 50502: "YES OPTUS", 50501: "Telstra", 50503: "vodafone AU", 23210: "3 AT", 23201: "A1", 23205: "one",
			23212: "one", 23203: "T-Mobile A", 40001: "AZERCELL", 40004: "AZ Nar", 40002: "BAKCELL GSM", 64202: "SAFARIS", 64201: "SPACETEL", 64203: "ONATEL BDI",
			64282: "Telecel BDI", 20620: "BASE", 20601: "BEL PROXIMUS", 20610: "B mobistar", 61604: "BBCOM", 61603: "BJ BENINCELL", 61602: "Telecel",
			61302: "BF CELTEL", 47001: "GRAMEEN", 47003: "Banglalink", 47004: "BGD bMobile", 47002: "BGD AKTEL", 47007: "WARID BD", 28403: "vivatel",
			28405: "BG GLOBUL", 28401: "M-Tel", 42601: "BHR M.PLUS", 42602: "zain BH", 36439: "BaTelCel", 21890: "BH GSMBIH", 21805: "MOBI'S", 25704: "BeST BY",
			25701: "BY VELCOM", 25702: "MTS GSM", 70267: "BTL", 35002: "MOBILITY", 35010: "Cingular", 73602: "BOMOV", 73601: "VIVA", 73603: "Telecel",
			72416: "Brasil Telecom", 72424: "AMAZONIA", 72405: "Claro", 72434: "CTBC", 72433: "CTBC", 72432: "CTBC", 72415: "BRA SCTL", 72423: "VIVO", 72403: "TIM",
			72402: "TIM", 72404: "TIM", 72431: "Oi", 72406: "VIVO", 72410: "VIVO", 72411: "VIVO", 342600: "Cable&Wireless", 342750: "Digicel", 52802: "b-mobile",
			52811: "BRU-DSTCom", 40211: "B-Mobile", 65201: "BW MASCOM", 65202: "Orange", 62302: "Telecel", 302370: "Fido", 302720: "Rogers", 22807: "In&Phone",
			22803: "orange CH", 22801: "Swisscom", 22802: "sunrise", 22808: "T2", 90115: "OnAir", 73003: "Claro", 73010: "ENTEL PCS", 73001: "ENTEL PCS",
			73002: "movistar", 46000: "China Mobile", 46001: "China Unicom", 61202: "ACELL-CI", 61204: "KoZ", 61205: "MTN CI", 61203: "Orange", 62401: "MTN",
			62402: "Orange", 63002: "CELTEL ", 63089: "CD OASIS", 63001: "VODACOM CD", 62901: "CELTEL ", 63010: "MTN-CG", 62907: "WARID RC", 63086: "DRC and CCT",
			62905: "SCELL", 54801: "CK KOKANET", 732111: "OLA", 732103: "TIGO COL", 732101: "COMCEL 3 GSM", 732123: "COL Movistar", 654001: "HURI",
			62501: "CPV MOVEL", 62502: "CPV T+", 71201: "I.C.E.", 71202: "I.C.E.", 36801: "CUBACEL", 346140: "Cable&Wireless", 28010: "MTN", 28001: "CYP CYTA",
			23001: "T-Mobile CZ", 23002: "EuroTel-Cz", 23003: "OSKAR", 26203: "E-Plus", 26207: "o2 - de", 26208: "o2 - de", 26201: "T-Mobile D", 26202: "Vodafone.de",
			63801: "DJ EVATIS", 366110: "Cable&Wireless", 366020: "Cingular", 23806: "3 DK", 23802: "DK SONOFON", 23801: "TDC MOBIL", 23820: "TELIA DK",
			37002: "CLARO DOM", 37001: "orange", 60301: "ALG MOBILE", 60302: "OTA NET", 60303: "NEDJMA", 74001: "PORTA GSM", 74000: "movistar", 60201: "MobiNiL",
			60203: "etisalat", 60202: "Vodafone EG", 21403: "Orange", 21407: "movistar", 21402: "movistar", 21401: "vodafone ES", 21404: "Yoigo", 24801: "EE EMT",
			24802: "elisa", 24803: "EE Q GSM", 63601: "ETH MTN", 24414: "FI AMT", 24403: "dna", 24412: "dna", 24412: "dna", 24405: "FL elisa", 24405: "FL elisa",
			24491: "FI SONERA", 54201: "FJ VODA", 75001: "C&W FLK", 20820: "BOUYGTEL", 20801: "Orange F", 20810: "F SFR", 34020: "Digicel", 34001: "Orange",
			54720: "F VINI", 28801: "FT-GSM", 28802: "KALL", 55001: "FSM Telecom", 62802: "Telecel", 62803: "CELTEL GA", 62801: "Libertis", 23455: "C&W",
			23420: "3 UK", 23450: "JT-Wave", 23458: "Manx Pronto", 23410: "O2 - UK", 23416: "Opal UK", 23433: "Orange", 23430: "T-Mobile UK", 23431: "T-Mobile UK",
			23432: "T-Mobile UK", 23401: "PMN", 23409: "PMN", 23415: "vodafone UK", 23450: "JT-Wave", 28801: "FT-GSM", 28802: "KALL", 28804: "BEELINE",
			62002: "GH ONEtouch", 62003: "tiGO", 62001: "GH MTN", 26601: "GIB GIBTEL", 61104: "CKY-Areeba", 61101: "Orange GN", 61102: "GN LAGUI", 34008: "AMIGO",
			60702: "AFRICELL", 60703: "GM COMIUM", 60701: "GAMCEL", 63207: "GTM", 63203: "Orange BS", 62701: "GETESA", 20201: "GR COSMOTE", 20205: "Vodafone GR",
			20210: "TIM", 352110: "Cable&Wireless", 352030: "Digicel", 29001: "TELE GRL", 70402: "TIGO", 70401: "Claro", 70403: "movistar", 34002: "ONLY",
			73802: "GUY CLNK PLS", 73801: "Digicel", 45412: "PEOPLES", 45400: "CSL", 45402: "CSL", 45418: "HK CSL", 45400: "CSL", 45402: "CSL", 45418: "HK CSL",
			45403: "3 HK", 45404: "3", 45410: "NEW WORLD", 45416: "PCCW", 45419: "PCCW", 45406: "SmarTone", 45415: "SmarTone", 70830: "HT - 200", 70801: "Claro",
			70802: "TIGO", 21901: "T-Mobile HR", 21902: "TELE2", 21910: "HR VIPnet", 37201: "COMCEL", 21630: "T-Mobile H", 21601: "pannon", 21601: "pannon",
			21670: "vodafone HU", 51011: "IND XL", 51089: "3", 51089: "3", 51001: "INDOSAT", 51021: "INDOSAT", 51008: "LIPPO TEL", 51010: "IND TSEL", 40441: "AIRCEL",
			40442: "AIRCEL", 40479: "CellOne", 40475: "CellOne", 40481: "CellOne", 40434: "CellOne", 40462: "CellOne", 40472: "CellOne", 40466: "CellOne",
			40474: "CellOne", 40454: "CellOne", 40455: "CellOne", 40480: "CellOne", 40459: "CellOne", 40453: "CellOne", 40476: "CellOne", 40477: "CellOne",
			40458: "CellOne", 40471: "CellOne", 40451: "CellOne", 40457: "CellOne", 40464: "CellOne", 40473: "CellOne", 40438: "CellOne", 40449: "AirTel",
			40410: "AirTel", 40431: "AirTel", 40403: "AirTel", 40440: "AIRTEL", 40402: "AirTel", 40493: "AirTel", 40495: "AirTel", 40497: "AirTel", 40496: "AirTel",
			40494: "AirTel", 40492: "AirTel", 40490: "AirTel", 40445: "AirTel", 40498: "AirTel", 40470: "INDH1", 40421: "Hutch", 40425: "AIRCEL", 40428: "AIRCEL",
			40437: "AIRCEL", 40435: "AIRCEL", 40433: "AIRCEL", 40417: "AIRCEL", 40429: "AIRCEL", 40482: "IDEA", 40489: "IDEA", 40487: "IDEA", 40424: "IDEA",
			40422: "IDEA", 40407: "IDEA", 40478: "IDEA", 40404: "IDEA", 40412: "IDEA", 40456: "IDEA", 40419: "IDEA", 40468: "DOLPHIN", 40469: "DOLPHIN",
			40444: "INA SPICE", 40414: "INA MODICO", 40427: "Vodafone IN", 40446: "Vodafone IN", 40443: "Vodafone IN", 40460: "Vodafone IN", 40501: "Vodafone",
			40415: "Vodafone IN", 40430: "Vodafone IN", 40405: "Vodafone IN", 40420: "Vodafone IN", 40411: "Vodafone IN", 40413: "Vodafone IN",
			40484: "Vodafone IN", 40486: "Vodafone IN", 40488: "Vodafone IN", 40556: "Airtel", 40551: "AIRTEL", 40554: "AIRTEL", 40553: "AIRTEL", 40555: "AIRTEL",
			40552: "AIRTEL", 40550: "Reliance", 40567: "Vodafone IN", 40566: "Vodafone IN", 27205: "3 IRL", 27203: "METEOR", 27202: "O2 - IRL", 27202: "O2 - IRL",
			27201: "Vodafone IE", 43214: "IR KISH", 43211: "TCI", 43219: "IR MTCE", 43232: "Taliya", 41800: "ASIACELL", 41805: "ASIACELL", 41820: "zain IQ",
			41830: "IRAQNA", 41808: "SanaTel", 41802: "SanaTel", 27407: "IS-IceCell", 27404: "Viking", 27411: "NOVA IS", 27402: "Og Vodafone", 27403: "Og Vodafone",
			27401: "Siminn", 27408: "On-waves", 42502: "Cellcom", 42502: "Cellcom", 42505: "JAWWAL", 42501: "Orange", 42503: "IL Pelephone", 22299: "3 ITA",
			22201: "I TIM", 22210: "vodafone IT", 22288: "WIND", 338180: "Cable&Wireless", 33805: "Digicel", 23403: "ATL-VOD", 23455: "C&W", 90117: "Navitas",
			41601: "zain JO", 41677: "Orange JO", 41603: "UMNIAH", 44000: "JPN EMOBILE", 44010: "JP DoCoMo", 44020: "SoftBank", 40102: "K'cell",
			40101: "Beeline KZ", 63903: "CELTEL", 63902: "Safaricom", 43705: "MEGACOM", 43701: "BITEL KGZ", 45605: "STAR CELL", 45618: "CAMSHIN",
			45601: "KHM MT-KHM", 45602: "KHM-SAMART", 54509: "KI-FRIG", 356110: "Cable&Wireless", 45002: "KR KTF", 45008: "KR KTF", 45005: "SKT", 42001: "AL JAWAL",
			41902: "ZAIN-KW", 41903: "KT WATANIYA", 40177: "NEO-KZ", 45702: "ETL MOBILE", 45703: "LATMIL", 45701: "LAO GSM", 45708: "TIGO LAO", 41501: "alfa",
			41503: "RL MTC Lebanon", 61802: "LIBERCEL", 61807: "Celcom", 61801: "LBR OMEGA", 60601: "Libya Al Madar", 60600: "Libyana", 358110: "Cable&Wireless",
			358050: "Digicel", 29505: "FL1", 29505: "FL1", 29502: "Orange FL", 29501: "FL GSM", 29577: "LI TANGO", 41308: "Hutch", 65102: "EZI-CEL",
			65101: "Vodacom-LS", 24601: "OMNITEL-LT", 24602: "BITE", 24603: "TELE2", 27001: "L LUXGSM", 27077: "L TANGO", 27099: "VOX.LU", 27099: "VOX.LU",
			24701: "LV LMT", 24701: "LV LMT", 24705: "BITE LV", 24705: "BITE LV", 24702: "LV B-COM", 45501: "CTM", 45504: "CTM", 45503: "Hutchison",
			45500: "SmarTone", 21210: "MONACO", 25904: "MDA EVENTIS", 25902: "MD MOLDCELL", 25901: "Orange MD", 64601: "MG CT", 64602: "ANTARIS", 64604: "TELMA",
			47201: "MV DHIMOBILE", 47202: "WMOBILE", 33403: "movistar", 33420: "TELCEL GSM", 29402: "COSMOFON", 29401: "T-Mobile MK", 61001: "MALITEL ML",
			61002: "ORANGE ML", 27821: "go mobile", 27801: "vodafone MT", 41401: "MPTGSM", 22004: "T-Mobile CG", 42899: "MN MobiCom", 42888: "UNTLMN", 60401: "IAM",
			60400: "Meditel", 64301: "MOZ-mCel", 64304: "VodaCom-MZ", 60901: "MR MATTEL", 61701: "CELLPLUS", 61710: "EMTEL", 354860: "Cable&Wireless",
			65010: "CELTEL MW", 65001: "MW CP 900", 50219: "MY CELCOM", 50213: "TMTOUCH", 50216: "DIGI", 50212: "MY MAXIS", 50200: "TIME3G", 50201: "TIME3G",
			64901: "NAM MPC", 64903: "Cell One", 54601: "NCL MOBILIS", 61402: "NE CELTEL", 61401: "SAHELCOM", 61403: "NE TELECEL", 62120: "Celtel NIG",
			62150: "Glo NG", 62130: "MTN-NG", 62140: "NG Mtel", 71073: "Claro", 71021: "Claro", 710300: "movistar", 20408: "NL KPN", 20420: "Orange NL",
			20416: "T-Mobile NL", 20412: "NL Telfort", 20404: "Vodafone NL", 24205: "NetworkN", 24202: "N NetCom", 24201: "N TELE-MOBIL", 24203: "Teletopia 3",
			53001: "vodafone NZ", 42202: "OMAN MOBILE", 42203: "nawras", 41001: "Mobilink", 41003: "PK-UFONE", 41004: "PAKTEL", 41006: "TELENOR", 41007: "WaridTel",
			71401: "PANCW", 71420: "movistar", 71402: "Movistar", 714020: "movistar", 71610: "Claro", 71606: "movistar", 51505: "SUN", 51502: "PH GLOBE",
			51501: "PH ISLACOM", 51503: "PH SMART", 55280: "PLWPMC", 53730: "Digicel", 53701: "BMobile", 26001: "Plus", 26002: "ERA PL", 26003: "Orange",
			46703: "KP SUN", 26803: "P OPTIMUS", 26806: "P TMN", 26801: "vodafone P", 74402: "CTI Movil PRY", 74401: "VOX", 74405: "PY Personal", 74404: "Telecel",
			42701: "Qat - Qtel", 64700: "Orange re", 64702: "ONLY", 64710: "F SRR", 22603: "COSMOTE", 22610: "ORANGE", 22601: "Vodafone RO", 25012: "FarEast",
			25012: "FarEast", 25007: "RUS SMARTS", 25020: "TELE2", 25019: "RUS.INDIGO", 25010: "RUS DTC", 25028: "RUS Beeline", 25012: "FarEast", 25017: "Utel",
			25039: "Utel", 25013: "MTS GSM", 25020: "TELE2", 25035: "MOTIV", 25002: "MegaFon", 25001: "MTS GSM", 25016: "NTC", 25002: "MegaFon", 25012: "FarEast",
			25099: "Beeline", 25092: "Primtel", 25020: "TELE2", 25005: "ETK RUS", 25020: "TELE2", 25004: "RUS_SCN", 25020: "TELE2", 25012: "FarEast",
			25020: "TELE2", 25039: "Utel", 25020: "TELE2", 25005: "ETK RUS", 25007: "RUS SMARTS", 25015: "SMARTS", 25002: "MegaFon", 63510: "R-CELL",
			42003: "mobily-KSA", 42003: "mobily-KSA", 22002: "ProMonte", 22003: "YUG 03", 63401: "SDN Mobitel", 63402: "MTN", 60802: "SENTEL", 60801: "ALIZE",
			63310: "SEZ AIRTEL", 52503: "SGP-M1-3GSM", 52502: "SingTel-G18", 52501: "SingTel", 52505: "StarHub", 54001: "BREEZE", 61901: "CELTEL SL",
			61902: "MILLICOM", 70601: "Claro", 70602: "Digicel", 70604: "movistar", 70603: "TIGO", 29266: "SMT", 63730: "Som Golis", 63704: "SOMAFONE",
			63782: "telsom", 63701: "SOMTELESOM", 30802: "SPM-PROSODIE", 30801: "AMERIS", 22003: "YUG 03", 22001: "Telenor SRB", 22005: "Vip SRB", 22005: "Vip SRB",
			41302: "SRI DIALOG", 41301: "MOBITEL", 41303: "SRI - Tigo", 62601: "STP CSTmovel", 74603: "Digicel", 74603: "Digicel", 74602: "TeleG",
			23101: "Orange SK", 23102: "T-Mobile SK", 23106: "O2 - SK", 29341: "MOBITEL", 29340: "SI vodafone", 29364: "T-2", 29370: "SI TUSMOBIL", 24002: "3 SE",
			24004: "vodafone SE", 24010: "S COMVIQ", 24010: "S COMVIQ", 24005: "Sweden 3G", 24008: "Telenor SE", 24004: "vodafone SE", 24008: "Telenor SE",
			24001: "TELIA S", 24005: "Sweden 3G", 65310: "Swazi-MTN", 65301: "C&W SEY", 41702: "MTN", 41709: "SYR MOB", 41701: "SYRIATEL", 376350: "Is.Com TCI",
			376350: "Is.Com TCI", 62201: "CELTEL TCD", 61503: "TELECEL-TOGO", 61501: "TG-TOGO CELL", 52015: "ACT-1900", 52001: "TH GSM", 52023: "GSM 1800",
			52018: "DTAC", 52099: "VRAI", 43604: "Babilon-M", 43602: "INDIGO-T", 43612: "INDIGO-3G", 43601: "Somoncom", 43605: "BEELINE", 43603: "TJK MLT",
			43801: "MTS TM", 43802: "TM CELL", 51402: "TLS-TT", 53901: "U-CALL", 37412: "TSTT", 60503: "TUNISIANA", 60502: "TUNTEL", 28603: "AVEA",
			28601: "TR TURKCELL", 28602: "VODAFONE TR", 46692: "Chunghwa", 46692: "Chunghwa", 46601: "Far EasTone", 46688: "KGT-Online", 46693: "TWN MOBITAI",
			46697: "TW mobile", 46699: "TransAsia", 46699: "TransAsia", 46689: "VIBO", 64005: "celtel", 64002: "MOBITEL - TZ", 64004: "VodaCom", 64003: "ZANTEL-TZ",
			42402: "ETISALAT", 64111: "UTL", 64101: "UG CELTEL", 64110: "MTN-UGANDA", 64122: "WaridTel", 25506: "ASTELIT", 25505: "UA GT-BCS", 25503: "UA-KYIVSTAR",
			25501: "MTS UKR", 25502: "Beeline UA", 74807: "Movistar", 74810: "CTI Movil URY", 310880: "USAACSI", 310640: "Einstein PCS", 310190: "Alaska Wireless ",
			310590: "Western Wireless", 310710: "USA ASTAC", 310170: "AT&T", 310410: "AT&T", 310150: "AT&T", 310030: "Centennial", 310630: "AmeriLink",
			310040: "Concho Wireless", 310740: "Telemetrix", 310080: "Corr Wireless", 310700: "USABIGFOOT", 310560: "Cell One", 310100: "Plateau", 310900: "TXCELL",
			310340: "WestLink", 310770: "i wireless", 310032: "IT&E", 310650: "Jasper", 310870: "Kaplan", 310530: "WVW", 310690: "IMMIX", 310570: "Chinook",
			310100: "Plateau", 310450: "Viaero", 310790: "Pinpoint", 310320: "Cellular One", 310910: "FCSI", 310260: "T-Mobile", 310270: "T-Mobile",
			310250: "T-Mobile", 310200: "T-Mobile", 31031: "T-Mobile", 310220: "T-Mobile", 310160: "T-Mobile ", 310660: "T-Mobile", 310240: "T-Mobile",
			310230: "T-Mobile", 310210: "T-Mobile", 31026: "T-Mobile", 310900: "TXCELL", 310100: "Plateau", 31046: "SIMMETRY", 310390: "Yorkville",
			310020: "UnionTel", 310400: "USA i CAN", 310890: "Unicell", 310950: "XIT", 311130: "C1AMARIL", 311190: "C1ECI", 311040: "Commnet", 311240: "USACWCI",
			311070: "EASTER", 311210: "Farmers Cellular", 311370: "GCI", 311110: "HPW", 311030: "Indigo", 311310: "LamarCel", 311090: "USASXLP", 31100: "WILKES",
			311170: "PetroCom", 311080: "PINECell", 311360: "STELERA", 311250: "iCAN_GSM", 31101: "WILKES", 31105: "WILKES", 31100: "WILKES", 43405: "UZB COSCOM",
			43407: "UZB MTS", 43407: "UZB MTS", 43404: "Beeline UZ", 360110: "Cable&Wireless", 360070: "Digicel", 73401: "DIGITEL", 73402: "DIGITEL",
			73403: "DIGITEL", 73404: "movistar", 348170: "Cable&Wireless", 348570: "CCTBVI", 45204: "VIETTEL", 45202: "VINAPHONE", 45201: "MOBIFONE",
			54101: "VUT SMILE", 54927: "Samoatel GO", 42102: "MTN", 42101: "SabaFon", 65507: "Cell C", 65510: "SA MTN", 65501: "SA VODA", 64501: "ZM CELTEL",
			64502: "TELECEL ZM", 64804: "ECONET", 64801: "ZW NET*ONE", 64803: "TELECEL ZW", 311260: "SLO Cellular", 46668: "ACeS", 51000: "ACeS", 51511: "ACeS",
			52020: "ACeS", 90610: "MAURITEL", 732111: "OLA", 90114: "AeroMob", 90112: "MCP", 90121: "Seanet", 90105: "Thuraya", 90106: "Thuraya"
			}

# text colour
colorLsit = ["dark blue", "coral", "forest green", "medium aquamarine",
			"purple", "sky blue", "blue", "brown", "black", "red", "dark slate blue", "orange"]
msgType = 8
myColor = ""
# 0  text intro : "DARK BLUE"
# 1  config : "coral"
# 2  nom du fichier test : "forest green"
# 3  Test description : "medium aquamarine"
# 4  OPEN / CLOSE port com : "purple"
# 5  ECHO : "sky blue"
# 6  Send : "blue"
# 7  Receive : "brown"
# 8  Default : "black"
# 9  Error : "red"
# 10 MUX : "dark slate blue"
# 11 Debug : "orange"
'''
color = ['aquamrine', 'black', 'blue', 'blue violet', 'brown', 'cadet blue', "coral", 'cornflower bleu', 'cyan', 'dark gray', 
         'dark green', 'dark olive green', 'dark orchid', 'dark slate blue', 'dark slate gray', 'dark turquoise',
         'dim gray', 'firebrik', 'forest green', 'gold', 'goldenrod', 'gray', 'green', 'green yellow', 'indian red',
         'khaki', 'light blue', 'light gray', 'light steel blue', 'lime green', 'magenta', 'maroon', 'medium aquamarine',
         'medium blue', 'medium forest green', 'medium goldenrod', 'medium orchid', 'medium sea green', 'medium slate bleu',
         'medium spring green', 'medium turquoise', 'medium violet red', 'midnight blue', 'navy', 'orange', 'orange red',
         'orchid', 'pale green', 'pink', 'plum', 'purple', 'red', 'salmon', 'sea green', 'sienna', 'sky blue']
'''

# Sierra Wireless
SndRcvTimestamp = False
RcvTimespent = False

# ascii conversion 

# for ascii2print(), mode="symbol"
ascii_symbol = {}
ascii_symbol['\x00'] = "<NULL>"
ascii_symbol['\x01'] = "<SOH>"
ascii_symbol['\x02'] = "<STX>"
ascii_symbol['\x03'] = "<ETX>"
ascii_symbol['\x04'] = "<EOT>"
ascii_symbol['\x05'] = "<ENQ>"
ascii_symbol['\x06'] = "<ACK>"
ascii_symbol['\x07'] = "<BEL>"
ascii_symbol['\x08'] = "<BS>"
ascii_symbol['\x09'] = "<TAB>"
ascii_symbol['\x0a'] = "<LF>"
ascii_symbol['\x0b'] = "<VT>"
ascii_symbol['\x0c'] = "<FF>"
ascii_symbol['\x0d'] = "<CR>"
ascii_symbol['\x0e'] = "<SO>"
ascii_symbol['\x0f'] = "<SI>"
ascii_symbol['\x10'] = "<DLE>"
ascii_symbol['\x11'] = "<DC1>"
ascii_symbol['\x12'] = "<DC2>"
ascii_symbol['\x13'] = "<DC3>"
ascii_symbol['\x14'] = "<DC4>"
ascii_symbol['\x15'] = "<NAK>"
ascii_symbol['\x16'] = "<SYN>"
ascii_symbol['\x17'] = "<ETB>"
ascii_symbol['\x18'] = "<CAN>"
ascii_symbol['\x19'] = "<EM>"
ascii_symbol['\x1a'] = "<SUB>"
ascii_symbol['\x1b'] = "<ESC>"
ascii_symbol['\x1c'] = "<FS>"
ascii_symbol['\x1d'] = "<GS>"
ascii_symbol['\x1e'] = "<RS>"
ascii_symbol['\x1f'] = "<US>"

ascii_symbol['\x7f'] = "<DEL>"

ascii_symbol['\x80'] = "<0x80>"
ascii_symbol['\x81'] = "<0x81>"
ascii_symbol['\x82'] = "<0x82>"
ascii_symbol['\x83'] = "<0x83>"
ascii_symbol['\x84'] = "<0x84>"
ascii_symbol['\x85'] = "<0x85>"
ascii_symbol['\x86'] = "<0x86>"
ascii_symbol['\x87'] = "<0x87>"
ascii_symbol['\x88'] = "<0x88>"
ascii_symbol['\x89'] = "<0x89>"
ascii_symbol['\x8A'] = "<0x8A>"
ascii_symbol['\x8B'] = "<0x8B>"
ascii_symbol['\x8C'] = "<0x8C>"
ascii_symbol['\x8D'] = "<0x8D>"
ascii_symbol['\x8E'] = "<0x8E>"
ascii_symbol['\x8F'] = "<0x8F>"
ascii_symbol['\x90'] = "<0x90>"
ascii_symbol['\x91'] = "<0x91>"
ascii_symbol['\x92'] = "<0x92>"
ascii_symbol['\x93'] = "<0x93>"
ascii_symbol['\x94'] = "<0x94>"
ascii_symbol['\x95'] = "<0x95>"
ascii_symbol['\x96'] = "<0x96>"
ascii_symbol['\x97'] = "<0x97>"
ascii_symbol['\x98'] = "<0x98>"
ascii_symbol['\x99'] = "<0x99>"
ascii_symbol['\x9A'] = "<0x9A>"
ascii_symbol['\x9B'] = "<0x9B>"
ascii_symbol['\x9C'] = "<0x9C>"
ascii_symbol['\x9D'] = "<0x9D>"
ascii_symbol['\x9E'] = "<0x9E>"
ascii_symbol['\x9F'] = "<0x9F>"
ascii_symbol['\xA0'] = "<0xA0>"
ascii_symbol['\xA1'] = "<0xA1>"
ascii_symbol['\xA2'] = "<0xA2>"
ascii_symbol['\xA3'] = "<0xA3>"
ascii_symbol['\xA4'] = "<0xA4>"
ascii_symbol['\xA5'] = "<0xA5>"
ascii_symbol['\xA6'] = "<0xA6>"
ascii_symbol['\xA7'] = "<0xA7>"
ascii_symbol['\xA8'] = "<0xA8>"
ascii_symbol['\xA9'] = "<0xA9>"
ascii_symbol['\xAA'] = "<0xAA>"
ascii_symbol['\xAB'] = "<0xAB>"
ascii_symbol['\xAC'] = "<0xAC>"
ascii_symbol['\xAD'] = "<0xAD>"
ascii_symbol['\xAE'] = "<0xAE>"
ascii_symbol['\xAF'] = "<0xAF>"
ascii_symbol['\xB0'] = "<0xB0>"
ascii_symbol['\xB1'] = "<0xB1>"
ascii_symbol['\xB2'] = "<0xB2>"
ascii_symbol['\xB3'] = "<0xB3>"
ascii_symbol['\xB4'] = "<0xB4>"
ascii_symbol['\xB5'] = "<0xB5>"
ascii_symbol['\xB6'] = "<0xB6>"
ascii_symbol['\xB7'] = "<0xB7>"
ascii_symbol['\xB8'] = "<0xB8>"
ascii_symbol['\xB9'] = "<0xB9>"
ascii_symbol['\xBA'] = "<0xBA>"
ascii_symbol['\xBB'] = "<0xBB>"
ascii_symbol['\xBC'] = "<0xBC>"
ascii_symbol['\xBD'] = "<0xBD>"
ascii_symbol['\xBE'] = "<0xBE>"
ascii_symbol['\xBF'] = "<0xBF>"
ascii_symbol['\xC0'] = "<0xC0>"
ascii_symbol['\xC1'] = "<0xC1>"
ascii_symbol['\xC2'] = "<0xC2>"
ascii_symbol['\xC3'] = "<0xC3>"
ascii_symbol['\xC4'] = "<0xC4>"
ascii_symbol['\xC5'] = "<0xC5>"
ascii_symbol['\xC6'] = "<0xC6>"
ascii_symbol['\xC7'] = "<0xC7>"
ascii_symbol['\xC8'] = "<0xC8>"
ascii_symbol['\xC9'] = "<0xC9>"
ascii_symbol['\xCA'] = "<0xCA>"
ascii_symbol['\xCB'] = "<0xCB>"
ascii_symbol['\xCC'] = "<0xCC>"
ascii_symbol['\xCD'] = "<0xCD>"
ascii_symbol['\xCE'] = "<0xCE>"
ascii_symbol['\xCF'] = "<0xCF>"
ascii_symbol['\xD0'] = "<0xD0>"
ascii_symbol['\xD1'] = "<0xD1>"
ascii_symbol['\xD2'] = "<0xD2>"
ascii_symbol['\xD3'] = "<0xD3>"
ascii_symbol['\xD4'] = "<0xD4>"
ascii_symbol['\xD5'] = "<0xD5>"
ascii_symbol['\xD6'] = "<0xD6>"
ascii_symbol['\xD7'] = "<0xD7>"
ascii_symbol['\xD8'] = "<0xD8>"
ascii_symbol['\xD9'] = "<0xD9>"
ascii_symbol['\xDA'] = "<0xDA>"
ascii_symbol['\xDB'] = "<0xDB>"
ascii_symbol['\xDC'] = "<0xDC>"
ascii_symbol['\xDD'] = "<0xDD>"
ascii_symbol['\xDE'] = "<0xDE>"
ascii_symbol['\xDF'] = "<0xDF>"
ascii_symbol['\xE0'] = "<0xE0>"
ascii_symbol['\xE1'] = "<0xE1>"
ascii_symbol['\xE2'] = "<0xE2>"
ascii_symbol['\xE3'] = "<0xE3>"
ascii_symbol['\xE4'] = "<0xE4>"
ascii_symbol['\xE5'] = "<0xE5>"
ascii_symbol['\xE6'] = "<0xE6>"
ascii_symbol['\xE7'] = "<0xE7>"
ascii_symbol['\xE8'] = "<0xE8>"
ascii_symbol['\xE9'] = "<0xE9>"
ascii_symbol['\xEA'] = "<0xEA>"
ascii_symbol['\xEB'] = "<0xEB>"
ascii_symbol['\xEC'] = "<0xEC>"
ascii_symbol['\xED'] = "<0xED>"
ascii_symbol['\xEE'] = "<0xEE>"
ascii_symbol['\xEF'] = "<0xEF>"
ascii_symbol['\xF0'] = "<0xF0>"
ascii_symbol['\xF1'] = "<0xF1>"
ascii_symbol['\xF2'] = "<0xF2>"
ascii_symbol['\xF3'] = "<0xF3>"
ascii_symbol['\xF4'] = "<0xF4>"
ascii_symbol['\xF5'] = "<0xF5>"
ascii_symbol['\xF6'] = "<0xF6>"
ascii_symbol['\xF7'] = "<0xF7>"
ascii_symbol['\xF8'] = "<0xF8>"
ascii_symbol['\xF9'] = "<0xF9>"
ascii_symbol['\xFA'] = "<0xFA>"
ascii_symbol['\xFB'] = "<0xFB>"
ascii_symbol['\xFC'] = "<0xFC>"
ascii_symbol['\xFD'] = "<0xFD>"
ascii_symbol['\xFE'] = "<0xFE>"
ascii_symbol['\xFF'] = "<0xFF>"


# for ascii2print(), mode="hexstring"

# hardcode for ascii2hexstring  >> very fast
# symbol
ascii2hexstring_symbol = {}
ascii2hexstring_symbol['\x00'] = "<0x00>"
ascii2hexstring_symbol['\x01'] = "<0x01>"
ascii2hexstring_symbol['\x02'] = "<0x02>"
ascii2hexstring_symbol['\x03'] = "<0x03>"
ascii2hexstring_symbol['\x04'] = "<0x04>"
ascii2hexstring_symbol['\x05'] = "<0x05>"
ascii2hexstring_symbol['\x06'] = "<0x06>"
ascii2hexstring_symbol['\x07'] = "<0x07>"
ascii2hexstring_symbol['\x08'] = "<0x08>"
ascii2hexstring_symbol['\x09'] = "<0x09>"
ascii2hexstring_symbol['\x0A'] = "<0x0A>"
ascii2hexstring_symbol['\x0B'] = "<0x0B>"
ascii2hexstring_symbol['\x0C'] = "<0x0C>"
ascii2hexstring_symbol['\x0D'] = "<0x0D>"
ascii2hexstring_symbol['\x0E'] = "<0x0E>"
ascii2hexstring_symbol['\x0F'] = "<0x0F>"
ascii2hexstring_symbol['\x10'] = "<0x10>"
ascii2hexstring_symbol['\x11'] = "<0x11>"
ascii2hexstring_symbol['\x12'] = "<0x12>"
ascii2hexstring_symbol['\x13'] = "<0x13>"
ascii2hexstring_symbol['\x14'] = "<0x14>"
ascii2hexstring_symbol['\x15'] = "<0x15>"
ascii2hexstring_symbol['\x16'] = "<0x16>"
ascii2hexstring_symbol['\x17'] = "<0x17>"
ascii2hexstring_symbol['\x18'] = "<0x18>"
ascii2hexstring_symbol['\x19'] = "<0x19>"
ascii2hexstring_symbol['\x1A'] = "<0x1A>"
ascii2hexstring_symbol['\x1B'] = "<0x1B>"
ascii2hexstring_symbol['\x1C'] = "<0x1C>"
ascii2hexstring_symbol['\x1D'] = "<0x1D>"
ascii2hexstring_symbol['\x1E'] = "<0x1E>"
ascii2hexstring_symbol['\x1F'] = "<0x1F>"

#printable
ascii2hexstring_printable = {}
ascii2hexstring_printable['\x20'] = "<0x20>"
ascii2hexstring_printable['\x21'] = "<0x21>"
ascii2hexstring_printable['\x22'] = "<0x22>"
ascii2hexstring_printable['\x23'] = "<0x23>"
ascii2hexstring_printable['\x24'] = "<0x24>"
ascii2hexstring_printable['\x25'] = "<0x25>"
ascii2hexstring_printable['\x26'] = "<0x26>"
ascii2hexstring_printable['\x27'] = "<0x27>"
ascii2hexstring_printable['\x28'] = "<0x28>"
ascii2hexstring_printable['\x29'] = "<0x29>"
ascii2hexstring_printable['\x2A'] = "<0x2A>"
ascii2hexstring_printable['\x2B'] = "<0x2B>"
ascii2hexstring_printable['\x2C'] = "<0x2C>"
ascii2hexstring_printable['\x2D'] = "<0x2D>"
ascii2hexstring_printable['\x2E'] = "<0x2E>"
ascii2hexstring_printable['\x2F'] = "<0x2F>"
ascii2hexstring_printable['\x30'] = "<0x30>"
ascii2hexstring_printable['\x31'] = "<0x31>"
ascii2hexstring_printable['\x32'] = "<0x32>"
ascii2hexstring_printable['\x33'] = "<0x33>"
ascii2hexstring_printable['\x34'] = "<0x34>"
ascii2hexstring_printable['\x35'] = "<0x35>"
ascii2hexstring_printable['\x36'] = "<0x36>"
ascii2hexstring_printable['\x37'] = "<0x37>"
ascii2hexstring_printable['\x38'] = "<0x38>"
ascii2hexstring_printable['\x39'] = "<0x39>"
ascii2hexstring_printable['\x3A'] = "<0x3A>"
ascii2hexstring_printable['\x3B'] = "<0x3B>"
ascii2hexstring_printable['\x3C'] = "<0x3C>"
ascii2hexstring_printable['\x3D'] = "<0x3D>"
ascii2hexstring_printable['\x3E'] = "<0x3E>"
ascii2hexstring_printable['\x3F'] = "<0x3F>"
ascii2hexstring_printable['\x40'] = "<0x40>"
ascii2hexstring_printable['\x41'] = "<0x41>"
ascii2hexstring_printable['\x42'] = "<0x42>"
ascii2hexstring_printable['\x43'] = "<0x43>"
ascii2hexstring_printable['\x44'] = "<0x44>"
ascii2hexstring_printable['\x45'] = "<0x45>"
ascii2hexstring_printable['\x46'] = "<0x46>"
ascii2hexstring_printable['\x47'] = "<0x47>"
ascii2hexstring_printable['\x48'] = "<0x48>"
ascii2hexstring_printable['\x49'] = "<0x49>"
ascii2hexstring_printable['\x4A'] = "<0x4A>"
ascii2hexstring_printable['\x4B'] = "<0x4B>"
ascii2hexstring_printable['\x4C'] = "<0x4C>"
ascii2hexstring_printable['\x4D'] = "<0x4D>"
ascii2hexstring_printable['\x4E'] = "<0x4E>"
ascii2hexstring_printable['\x4F'] = "<0x4F>"
ascii2hexstring_printable['\x50'] = "<0x50>"
ascii2hexstring_printable['\x51'] = "<0x51>"
ascii2hexstring_printable['\x52'] = "<0x52>"
ascii2hexstring_printable['\x53'] = "<0x53>"
ascii2hexstring_printable['\x54'] = "<0x54>"
ascii2hexstring_printable['\x55'] = "<0x55>"
ascii2hexstring_printable['\x56'] = "<0x56>"
ascii2hexstring_printable['\x57'] = "<0x57>"
ascii2hexstring_printable['\x58'] = "<0x58>"
ascii2hexstring_printable['\x59'] = "<0x59>"
ascii2hexstring_printable['\x5A'] = "<0x5A>"
ascii2hexstring_printable['\x5B'] = "<0x5B>"
ascii2hexstring_printable['\x5C'] = "<0x5C>"
ascii2hexstring_printable['\x5D'] = "<0x5D>"
ascii2hexstring_printable['\x5E'] = "<0x5E>"
ascii2hexstring_printable['\x5F'] = "<0x5F>"
ascii2hexstring_printable['\x60'] = "<0x60>"
ascii2hexstring_printable['\x61'] = "<0x61>"
ascii2hexstring_printable['\x62'] = "<0x62>"
ascii2hexstring_printable['\x63'] = "<0x63>"
ascii2hexstring_printable['\x64'] = "<0x64>"
ascii2hexstring_printable['\x65'] = "<0x65>"
ascii2hexstring_printable['\x66'] = "<0x66>"
ascii2hexstring_printable['\x67'] = "<0x67>"
ascii2hexstring_printable['\x68'] = "<0x68>"
ascii2hexstring_printable['\x69'] = "<0x69>"
ascii2hexstring_printable['\x6A'] = "<0x6A>"
ascii2hexstring_printable['\x6B'] = "<0x6B>"
ascii2hexstring_printable['\x6C'] = "<0x6C>"
ascii2hexstring_printable['\x6D'] = "<0x6D>"
ascii2hexstring_printable['\x6E'] = "<0x6E>"
ascii2hexstring_printable['\x6F'] = "<0x6F>"
ascii2hexstring_printable['\x70'] = "<0x70>"
ascii2hexstring_printable['\x71'] = "<0x71>"
ascii2hexstring_printable['\x72'] = "<0x72>"
ascii2hexstring_printable['\x73'] = "<0x73>"
ascii2hexstring_printable['\x74'] = "<0x74>"
ascii2hexstring_printable['\x75'] = "<0x75>"
ascii2hexstring_printable['\x76'] = "<0x76>"
ascii2hexstring_printable['\x77'] = "<0x77>"
ascii2hexstring_printable['\x78'] = "<0x78>"
ascii2hexstring_printable['\x79'] = "<0x79>"
ascii2hexstring_printable['\x7A'] = "<0x7A>"
ascii2hexstring_printable['\x7B'] = "<0x7B>"
ascii2hexstring_printable['\x7C'] = "<0x7C>"
ascii2hexstring_printable['\x7D'] = "<0x7D>"
ascii2hexstring_printable['\x7E'] = "<0x7E>"
ascii2hexstring_printable['\x7F'] = "<0x7F>"

# extendec ascii
ascii2hexstring_extended = {}
ascii2hexstring_extended['\x80'] = "<0x80>"
ascii2hexstring_extended['\x81'] = "<0x81>"
ascii2hexstring_extended['\x82'] = "<0x82>"
ascii2hexstring_extended['\x83'] = "<0x83>"
ascii2hexstring_extended['\x84'] = "<0x84>"
ascii2hexstring_extended['\x85'] = "<0x85>"
ascii2hexstring_extended['\x86'] = "<0x86>"
ascii2hexstring_extended['\x87'] = "<0x87>"
ascii2hexstring_extended['\x88'] = "<0x88>"
ascii2hexstring_extended['\x89'] = "<0x89>"
ascii2hexstring_extended['\x8A'] = "<0x8A>"
ascii2hexstring_extended['\x8B'] = "<0x8B>"
ascii2hexstring_extended['\x8C'] = "<0x8C>"
ascii2hexstring_extended['\x8D'] = "<0x8D>"
ascii2hexstring_extended['\x8E'] = "<0x8E>"
ascii2hexstring_extended['\x8F'] = "<0x8F>"
ascii2hexstring_extended['\x90'] = "<0x90>"
ascii2hexstring_extended['\x91'] = "<0x91>"
ascii2hexstring_extended['\x92'] = "<0x92>"
ascii2hexstring_extended['\x93'] = "<0x93>"
ascii2hexstring_extended['\x94'] = "<0x94>"
ascii2hexstring_extended['\x95'] = "<0x95>"
ascii2hexstring_extended['\x96'] = "<0x96>"
ascii2hexstring_extended['\x97'] = "<0x97>"
ascii2hexstring_extended['\x98'] = "<0x98>"
ascii2hexstring_extended['\x99'] = "<0x99>"
ascii2hexstring_extended['\x9A'] = "<0x9A>"
ascii2hexstring_extended['\x9B'] = "<0x9B>"
ascii2hexstring_extended['\x9C'] = "<0x9C>"
ascii2hexstring_extended['\x9D'] = "<0x9D>"
ascii2hexstring_extended['\x9E'] = "<0x9E>"
ascii2hexstring_extended['\x9F'] = "<0x9F>"
ascii2hexstring_extended['\xA0'] = "<0xA0>"
ascii2hexstring_extended['\xA1'] = "<0xA1>"
ascii2hexstring_extended['\xA2'] = "<0xA2>"
ascii2hexstring_extended['\xA3'] = "<0xA3>"
ascii2hexstring_extended['\xA4'] = "<0xA4>"
ascii2hexstring_extended['\xA5'] = "<0xA5>"
ascii2hexstring_extended['\xA6'] = "<0xA6>"
ascii2hexstring_extended['\xA7'] = "<0xA7>"
ascii2hexstring_extended['\xA8'] = "<0xA8>"
ascii2hexstring_extended['\xA9'] = "<0xA9>"
ascii2hexstring_extended['\xAA'] = "<0xAA>"
ascii2hexstring_extended['\xAB'] = "<0xAB>"
ascii2hexstring_extended['\xAC'] = "<0xAC>"
ascii2hexstring_extended['\xAD'] = "<0xAD>"
ascii2hexstring_extended['\xAE'] = "<0xAE>"
ascii2hexstring_extended['\xAF'] = "<0xAF>"
ascii2hexstring_extended['\xB0'] = "<0xB0>"
ascii2hexstring_extended['\xB1'] = "<0xB1>"
ascii2hexstring_extended['\xB2'] = "<0xB2>"
ascii2hexstring_extended['\xB3'] = "<0xB3>"
ascii2hexstring_extended['\xB4'] = "<0xB4>"
ascii2hexstring_extended['\xB5'] = "<0xB5>"
ascii2hexstring_extended['\xB6'] = "<0xB6>"
ascii2hexstring_extended['\xB7'] = "<0xB7>"
ascii2hexstring_extended['\xB8'] = "<0xB8>"
ascii2hexstring_extended['\xB9'] = "<0xB9>"
ascii2hexstring_extended['\xBA'] = "<0xBA>"
ascii2hexstring_extended['\xBB'] = "<0xBB>"
ascii2hexstring_extended['\xBC'] = "<0xBC>"
ascii2hexstring_extended['\xBD'] = "<0xBD>"
ascii2hexstring_extended['\xBE'] = "<0xBE>"
ascii2hexstring_extended['\xBF'] = "<0xBF>"
ascii2hexstring_extended['\xC0'] = "<0xC0>"
ascii2hexstring_extended['\xC1'] = "<0xC1>"
ascii2hexstring_extended['\xC2'] = "<0xC2>"
ascii2hexstring_extended['\xC3'] = "<0xC3>"
ascii2hexstring_extended['\xC4'] = "<0xC4>"
ascii2hexstring_extended['\xC5'] = "<0xC5>"
ascii2hexstring_extended['\xC6'] = "<0xC6>"
ascii2hexstring_extended['\xC7'] = "<0xC7>"
ascii2hexstring_extended['\xC8'] = "<0xC8>"
ascii2hexstring_extended['\xC9'] = "<0xC9>"
ascii2hexstring_extended['\xCA'] = "<0xCA>"
ascii2hexstring_extended['\xCB'] = "<0xCB>"
ascii2hexstring_extended['\xCC'] = "<0xCC>"
ascii2hexstring_extended['\xCD'] = "<0xCD>"
ascii2hexstring_extended['\xCE'] = "<0xCE>"
ascii2hexstring_extended['\xCF'] = "<0xCF>"
ascii2hexstring_extended['\xD0'] = "<0xD0>"
ascii2hexstring_extended['\xD1'] = "<0xD1>"
ascii2hexstring_extended['\xD2'] = "<0xD2>"
ascii2hexstring_extended['\xD3'] = "<0xD3>"
ascii2hexstring_extended['\xD4'] = "<0xD4>"
ascii2hexstring_extended['\xD5'] = "<0xD5>"
ascii2hexstring_extended['\xD6'] = "<0xD6>"
ascii2hexstring_extended['\xD7'] = "<0xD7>"
ascii2hexstring_extended['\xD8'] = "<0xD8>"
ascii2hexstring_extended['\xD9'] = "<0xD9>"
ascii2hexstring_extended['\xDA'] = "<0xDA>"
ascii2hexstring_extended['\xDB'] = "<0xDB>"
ascii2hexstring_extended['\xDC'] = "<0xDC>"
ascii2hexstring_extended['\xDD'] = "<0xDD>"
ascii2hexstring_extended['\xDE'] = "<0xDE>"
ascii2hexstring_extended['\xDF'] = "<0xDF>"
ascii2hexstring_extended['\xE0'] = "<0xE0>"
ascii2hexstring_extended['\xE1'] = "<0xE1>"
ascii2hexstring_extended['\xE2'] = "<0xE2>"
ascii2hexstring_extended['\xE3'] = "<0xE3>"
ascii2hexstring_extended['\xE4'] = "<0xE4>"
ascii2hexstring_extended['\xE5'] = "<0xE5>"
ascii2hexstring_extended['\xE6'] = "<0xE6>"
ascii2hexstring_extended['\xE7'] = "<0xE7>"
ascii2hexstring_extended['\xE8'] = "<0xE8>"
ascii2hexstring_extended['\xE9'] = "<0xE9>"
ascii2hexstring_extended['\xEA'] = "<0xEA>"
ascii2hexstring_extended['\xEB'] = "<0xEB>"
ascii2hexstring_extended['\xEC'] = "<0xEC>"
ascii2hexstring_extended['\xED'] = "<0xED>"
ascii2hexstring_extended['\xEE'] = "<0xEE>"
ascii2hexstring_extended['\xEF'] = "<0xEF>"
ascii2hexstring_extended['\xF0'] = "<0xF0>"
ascii2hexstring_extended['\xF1'] = "<0xF1>"
ascii2hexstring_extended['\xF2'] = "<0xF2>"
ascii2hexstring_extended['\xF3'] = "<0xF3>"
ascii2hexstring_extended['\xF4'] = "<0xF4>"
ascii2hexstring_extended['\xF5'] = "<0xF5>"
ascii2hexstring_extended['\xF6'] = "<0xF6>"
ascii2hexstring_extended['\xF7'] = "<0xF7>"
ascii2hexstring_extended['\xF8'] = "<0xF8>"
ascii2hexstring_extended['\xF9'] = "<0xF9>"
ascii2hexstring_extended['\xFA'] = "<0xFA>"
ascii2hexstring_extended['\xFB'] = "<0xFB>"
ascii2hexstring_extended['\xFC'] = "<0xFC>"
ascii2hexstring_extended['\xFD'] = "<0xFD>"
ascii2hexstring_extended['\xFE'] = "<0xFE>"
ascii2hexstring_extended['\xFF'] = "<0xFF>"

# for mode="hexstring", fast convertion for printable ascii , ord()+128
ascii2hexstring_printable_tempsymbol = {}
ascii2hexstring_printable_tempsymbol['\x20'] = "\xBC\xB0\xF8\xA0\xBE"
ascii2hexstring_printable_tempsymbol['\x21'] = "\xBC\xB0\xF8\xA1\xBE"
ascii2hexstring_printable_tempsymbol['\x22'] = "\xBC\xB0\xF8\xA2\xBE"
ascii2hexstring_printable_tempsymbol['\x23'] = "\xBC\xB0\xF8\xA3\xBE"
ascii2hexstring_printable_tempsymbol['\x24'] = "\xBC\xB0\xF8\xA4\xBE"
ascii2hexstring_printable_tempsymbol['\x25'] = "\xBC\xB0\xF8\xA5\xBE"
ascii2hexstring_printable_tempsymbol['\x26'] = "\xBC\xB0\xF8\xA6\xBE"
ascii2hexstring_printable_tempsymbol['\x27'] = "\xBC\xB0\xF8\xA7\xBE"
ascii2hexstring_printable_tempsymbol['\x28'] = "\xBC\xB0\xF8\xA8\xBE"
ascii2hexstring_printable_tempsymbol['\x29'] = "\xBC\xB0\xF8\xA9\xBE"
ascii2hexstring_printable_tempsymbol['\x2A'] = "\xBC\xB0\xF8\xAA\xBE"
ascii2hexstring_printable_tempsymbol['\x2B'] = "\xBC\xB0\xF8\xAB\xBE"
ascii2hexstring_printable_tempsymbol['\x2C'] = "\xBC\xB0\xF8\xAC\xBE"
ascii2hexstring_printable_tempsymbol['\x2D'] = "\xBC\xB0\xF8\xAD\xBE"
ascii2hexstring_printable_tempsymbol['\x2E'] = "\xBC\xB0\xF8\xAE\xBE"
ascii2hexstring_printable_tempsymbol['\x2F'] = "\xBC\xB0\xF8\xAF\xBE"
ascii2hexstring_printable_tempsymbol['\x30'] = "\xBC\xB0\xF8\xB0\xBE"
ascii2hexstring_printable_tempsymbol['\x31'] = "\xBC\xB0\xF8\xB1\xBE"
ascii2hexstring_printable_tempsymbol['\x32'] = "\xBC\xB0\xF8\xB2\xBE"
ascii2hexstring_printable_tempsymbol['\x33'] = "\xBC\xB0\xF8\xB3\xBE"
ascii2hexstring_printable_tempsymbol['\x34'] = "\xBC\xB0\xF8\xB4\xBE"
ascii2hexstring_printable_tempsymbol['\x35'] = "\xBC\xB0\xF8\xB5\xBE"
ascii2hexstring_printable_tempsymbol['\x36'] = "\xBC\xB0\xF8\xB6\xBE"
ascii2hexstring_printable_tempsymbol['\x37'] = "\xBC\xB0\xF8\xB7\xBE"
ascii2hexstring_printable_tempsymbol['\x38'] = "\xBC\xB0\xF8\xB8\xBE"
ascii2hexstring_printable_tempsymbol['\x39'] = "\xBC\xB0\xF8\xB9\xBE"
ascii2hexstring_printable_tempsymbol['\x3A'] = "\xBC\xB0\xF8\xBA\xBE"
ascii2hexstring_printable_tempsymbol['\x3B'] = "\xBC\xB0\xF8\xBB\xBE"
ascii2hexstring_printable_tempsymbol['\x3C'] = "\xBC\xB0\xF8\xBC\xBE"
ascii2hexstring_printable_tempsymbol['\x3D'] = "\xBC\xB0\xF8\xBD\xBE"
ascii2hexstring_printable_tempsymbol['\x3E'] = "\xBC\xB0\xF8\xBE\xBE"
ascii2hexstring_printable_tempsymbol['\x3F'] = "\xBC\xB0\xF8\xBF\xBE"
ascii2hexstring_printable_tempsymbol['\x40'] = "\xBC\xB0\xF8\xC0\xBE"
ascii2hexstring_printable_tempsymbol['\x41'] = "\xBC\xB0\xF8\xC1\xBE"
ascii2hexstring_printable_tempsymbol['\x42'] = "\xBC\xB0\xF8\xC2\xBE"
ascii2hexstring_printable_tempsymbol['\x43'] = "\xBC\xB0\xF8\xC3\xBE"
ascii2hexstring_printable_tempsymbol['\x44'] = "\xBC\xB0\xF8\xC4\xBE"
ascii2hexstring_printable_tempsymbol['\x45'] = "\xBC\xB0\xF8\xC5\xBE"
ascii2hexstring_printable_tempsymbol['\x46'] = "\xBC\xB0\xF8\xC6\xBE"
ascii2hexstring_printable_tempsymbol['\x47'] = "\xBC\xB0\xF8\xC7\xBE"
ascii2hexstring_printable_tempsymbol['\x48'] = "\xBC\xB0\xF8\xC8\xBE"
ascii2hexstring_printable_tempsymbol['\x49'] = "\xBC\xB0\xF8\xC9\xBE"
ascii2hexstring_printable_tempsymbol['\x4A'] = "\xBC\xB0\xF8\xCA\xBE"
ascii2hexstring_printable_tempsymbol['\x4B'] = "\xBC\xB0\xF8\xCB\xBE"
ascii2hexstring_printable_tempsymbol['\x4C'] = "\xBC\xB0\xF8\xCC\xBE"
ascii2hexstring_printable_tempsymbol['\x4D'] = "\xBC\xB0\xF8\xCD\xBE"
ascii2hexstring_printable_tempsymbol['\x4E'] = "\xBC\xB0\xF8\xCE\xBE"
ascii2hexstring_printable_tempsymbol['\x4F'] = "\xBC\xB0\xF8\xCF\xBE"
ascii2hexstring_printable_tempsymbol['\x50'] = "\xBC\xB0\xF8\xD0\xBE"
ascii2hexstring_printable_tempsymbol['\x51'] = "\xBC\xB0\xF8\xD1\xBE"
ascii2hexstring_printable_tempsymbol['\x52'] = "\xBC\xB0\xF8\xD2\xBE"
ascii2hexstring_printable_tempsymbol['\x53'] = "\xBC\xB0\xF8\xD3\xBE"
ascii2hexstring_printable_tempsymbol['\x54'] = "\xBC\xB0\xF8\xD4\xBE"
ascii2hexstring_printable_tempsymbol['\x55'] = "\xBC\xB0\xF8\xD5\xBE"
ascii2hexstring_printable_tempsymbol['\x56'] = "\xBC\xB0\xF8\xD6\xBE"
ascii2hexstring_printable_tempsymbol['\x57'] = "\xBC\xB0\xF8\xD7\xBE"
ascii2hexstring_printable_tempsymbol['\x58'] = "\xBC\xB0\xF8\xD8\xBE"
ascii2hexstring_printable_tempsymbol['\x59'] = "\xBC\xB0\xF8\xD9\xBE"
ascii2hexstring_printable_tempsymbol['\x5A'] = "\xBC\xB0\xF8\xDA\xBE"
ascii2hexstring_printable_tempsymbol['\x5B'] = "\xBC\xB0\xF8\xDB\xBE"
ascii2hexstring_printable_tempsymbol['\x5C'] = "\xBC\xB0\xF8\xDC\xBE"
ascii2hexstring_printable_tempsymbol['\x5D'] = "\xBC\xB0\xF8\xDD\xBE"
ascii2hexstring_printable_tempsymbol['\x5E'] = "\xBC\xB0\xF8\xDE\xBE"
ascii2hexstring_printable_tempsymbol['\x5F'] = "\xBC\xB0\xF8\xDF\xBE"
ascii2hexstring_printable_tempsymbol['\x60'] = "\xBC\xB0\xF8\xE0\xBE"
ascii2hexstring_printable_tempsymbol['\x61'] = "\xBC\xB0\xF8\xE1\xBE"
ascii2hexstring_printable_tempsymbol['\x62'] = "\xBC\xB0\xF8\xE2\xBE"
ascii2hexstring_printable_tempsymbol['\x63'] = "\xBC\xB0\xF8\xE3\xBE"
ascii2hexstring_printable_tempsymbol['\x64'] = "\xBC\xB0\xF8\xE4\xBE"
ascii2hexstring_printable_tempsymbol['\x65'] = "\xBC\xB0\xF8\xE5\xBE"
ascii2hexstring_printable_tempsymbol['\x66'] = "\xBC\xB0\xF8\xE6\xBE"
ascii2hexstring_printable_tempsymbol['\x67'] = "\xBC\xB0\xF8\xE7\xBE"
ascii2hexstring_printable_tempsymbol['\x68'] = "\xBC\xB0\xF8\xE8\xBE"
ascii2hexstring_printable_tempsymbol['\x69'] = "\xBC\xB0\xF8\xE9\xBE"
ascii2hexstring_printable_tempsymbol['\x6A'] = "\xBC\xB0\xF8\xEA\xBE"
ascii2hexstring_printable_tempsymbol['\x6B'] = "\xBC\xB0\xF8\xEB\xBE"
ascii2hexstring_printable_tempsymbol['\x6C'] = "\xBC\xB0\xF8\xEC\xBE"
ascii2hexstring_printable_tempsymbol['\x6D'] = "\xBC\xB0\xF8\xED\xBE"
ascii2hexstring_printable_tempsymbol['\x6E'] = "\xBC\xB0\xF8\xEE\xBE"
ascii2hexstring_printable_tempsymbol['\x6F'] = "\xBC\xB0\xF8\xEF\xBE"
ascii2hexstring_printable_tempsymbol['\x70'] = "\xBC\xB0\xF8\xF0\xBE"
ascii2hexstring_printable_tempsymbol['\x71'] = "\xBC\xB0\xF8\xF1\xBE"
ascii2hexstring_printable_tempsymbol['\x72'] = "\xBC\xB0\xF8\xF2\xBE"
ascii2hexstring_printable_tempsymbol['\x73'] = "\xBC\xB0\xF8\xF3\xBE"
ascii2hexstring_printable_tempsymbol['\x74'] = "\xBC\xB0\xF8\xF4\xBE"
ascii2hexstring_printable_tempsymbol['\x75'] = "\xBC\xB0\xF8\xF5\xBE"
ascii2hexstring_printable_tempsymbol['\x76'] = "\xBC\xB0\xF8\xF6\xBE"
ascii2hexstring_printable_tempsymbol['\x77'] = "\xBC\xB0\xF8\xF7\xBE"
ascii2hexstring_printable_tempsymbol['\x78'] = "\xBC\xB0\xF8\xF8\xBE"
ascii2hexstring_printable_tempsymbol['\x79'] = "\xBC\xB0\xF8\xF9\xBE"
ascii2hexstring_printable_tempsymbol['\x7A'] = "\xBC\xB0\xF8\xFA\xBE"
ascii2hexstring_printable_tempsymbol['\x7B'] = "\xBC\xB0\xF8\xFB\xBE"
ascii2hexstring_printable_tempsymbol['\x7C'] = "\xBC\xB0\xF8\xFC\xBE"
ascii2hexstring_printable_tempsymbol['\x7D'] = "\xBC\xB0\xF8\xFD\xBE"
ascii2hexstring_printable_tempsymbol['\x7E'] = "\xBC\xB0\xF8\xFE\xBE"
ascii2hexstring_printable_tempsymbol['\x7F'] = "\xBC\xB0\xF8\xFF\xBE"

ascii2hexstring_printable_revert = {}
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA0\xBE'] = "<0x20>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA1\xBE'] = "<0x21>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA2\xBE'] = "<0x22>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA3\xBE'] = "<0x23>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA4\xBE'] = "<0x24>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA5\xBE'] = "<0x25>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA6\xBE'] = "<0x26>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA7\xBE'] = "<0x27>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA8\xBE'] = "<0x28>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xA9\xBE'] = "<0x29>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAA\xBE'] = "<0x2A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAB\xBE'] = "<0x2B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAC\xBE'] = "<0x2C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAD\xBE'] = "<0x2D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAE\xBE'] = "<0x2E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xAF\xBE'] = "<0x2F>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB0\xBE'] = "<0x30>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB1\xBE'] = "<0x31>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB2\xBE'] = "<0x32>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB3\xBE'] = "<0x33>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB4\xBE'] = "<0x34>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB5\xBE'] = "<0x35>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB6\xBE'] = "<0x36>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB7\xBE'] = "<0x37>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB8\xBE'] = "<0x38>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xB9\xBE'] = "<0x39>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBA\xBE'] = "<0x3A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBB\xBE'] = "<0x3B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBC\xBE'] = "<0x3C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBD\xBE'] = "<0x3D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBE\xBE'] = "<0x3E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xBF\xBE'] = "<0x3F>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC0\xBE'] = "<0x40>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC1\xBE'] = "<0x41>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC2\xBE'] = "<0x42>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC3\xBE'] = "<0x43>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC4\xBE'] = "<0x44>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC5\xBE'] = "<0x45>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC6\xBE'] = "<0x46>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC7\xBE'] = "<0x47>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC8\xBE'] = "<0x48>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xC9\xBE'] = "<0x49>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCA\xBE'] = "<0x4A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCB\xBE'] = "<0x4B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCC\xBE'] = "<0x4C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCD\xBE'] = "<0x4D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCE\xBE'] = "<0x4E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xCF\xBE'] = "<0x4F>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD0\xBE'] = "<0x50>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD1\xBE'] = "<0x51>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD2\xBE'] = "<0x52>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD3\xBE'] = "<0x53>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD4\xBE'] = "<0x54>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD5\xBE'] = "<0x55>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD6\xBE'] = "<0x56>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD7\xBE'] = "<0x57>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD8\xBE'] = "<0x58>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xD9\xBE'] = "<0x59>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDA\xBE'] = "<0x5A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDB\xBE'] = "<0x5B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDC\xBE'] = "<0x5C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDD\xBE'] = "<0x5D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDE\xBE'] = "<0x5E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xDF\xBE'] = "<0x5F>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE0\xBE'] = "<0x60>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE1\xBE'] = "<0x61>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE2\xBE'] = "<0x62>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE3\xBE'] = "<0x63>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE4\xBE'] = "<0x64>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE5\xBE'] = "<0x65>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE6\xBE'] = "<0x66>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE7\xBE'] = "<0x67>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE8\xBE'] = "<0x68>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xE9\xBE'] = "<0x69>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xEA\xBE'] = "<0x6A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xEB\xBE'] = "<0x6B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xEC\xBE'] = "<0x6C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xED\xBE'] = "<0x6D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xEE\xBE'] = "<0x6E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xEF\xBE'] = "<0x6F>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF0\xBE'] = "<0x70>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF1\xBE'] = "<0x71>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF2\xBE'] = "<0x72>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF3\xBE'] = "<0x73>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF4\xBE'] = "<0x74>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF5\xBE'] = "<0x75>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF6\xBE'] = "<0x76>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF7\xBE'] = "<0x77>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF8\xBE'] = "<0x78>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xF9\xBE'] = "<0x79>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFA\xBE'] = "<0x7A>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFB\xBE'] = "<0x7B>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFC\xBE'] = "<0x7C>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFD\xBE'] = "<0x7D>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFE\xBE'] = "<0x7E>"
ascii2hexstring_printable_revert['\xBC\xB0\xF8\xFF\xBE'] = "<0x7F>"
