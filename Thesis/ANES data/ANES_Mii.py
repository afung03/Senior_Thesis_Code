import matplotlib.pyplot as plt
import numpy as np
import random as rng
import pandas as pd
import csv
import seaborn as sb


# need [coding of most impt issue, coding of weight, highest coding - 1]

ANES_names = {
    'NES1980.dta' : ['V800979', None, 1000, 1980], # no weights
    'NES1982.dta' : ['V820299', None, 1000, 1982],
    'NES1984.dta' : ['V840993', None, 1000, 1984],
    'NES1986.dta' : ['V860306', None, 1000, 1986], # used most impt natl issue instead of most impt problem to you
    'NES1988.dta' : ['V880702', None, 1000, 1988],
    'NES1990.dta' : ['V900326', None, 1000, 1990], # also asked to list other problems, but does not indicate quantity of importance? (not all surveys list other types of problems)
    'NES1992.dta' : ['V900326', 'V927000', 1000, 1992],   # start using weights
    'NES1994.dta' : ['V940706', 'V940006a', 1000, 1994],
    'NES1996.dta' : ['V961141', 'V960005', 1000, 1996],
    'NES1998.dta' : ['V980346', 'V980002', 1000, 1998],
    'NES2000.dta' : ['V000436', 'V000002', 1000, 2000]
}

# issue name : [issue code, year, file name, weight code, income code]
bills = {
    '''
    'Sanction_SA' :         ['V860490', 1986, 'year_dta_files/NES1986.dta', None, 'V860733'], #Happened, likely?
    'forces_to_PG' :        ['V912408', 1992, 'year_dta_files/NES1992.dta', 'V927000', 'V924104'], #Happened
    'Gulf_war' :            ['V912500', 1992, 'year_dta_files/NES1992.dta', 'V927000', 'V924104'], #Happened
    'aid_postcommunist' :   ['V912401', 1992, 'year_dta_files/NES1992.dta', 'V927000', 'V900694'], #Happened
    'Clinton_crime_bill' :  ['V941040', 1994, 'year_dta_files/NES1994.dta', 'V940006a', 'V941404'], #Happened, likely? 
    'School_prayer' :       ['V941020', 1994, 'year_dta_files/NES1994.dta', 'V940006a', 'V941404'],
    'term_limits' :         ['V960412', 1996, 'year_dta_files/NES1996.dta', 'V960005', 'V960701'],
    'fed_death_penalty' :   ['V961197', 1996, 'year_dta_files/NES1996.dta', 'V960005', 'V960701'], #Happened, likely?
    '2yr_welf_limit' :      ['V961323', 1996, 'year_dta_files/NES1996.dta', 'V960005', 'V960701'],
    'ban_late_abortion' :   ['V980511', 1998, 'year_dta_files/NES1998.dta', 'V980002', 'V980652'],
    'ban_partial_birth' :   ['V000703', 2000, 'year_dta_files/NES2000.dta', 'V000002', 'V001040'],
    'school_vouchers' :     ['V000742', 2000, 'year_dta_files/NES2000.dta', 'V000002', 'V001040']
    '''


}

lowball_dict = {
    'NAFTA' :           [493.0, 495.0, 497.0], # restricted to international trade related concerns
    'Aid_Russia1' :     [530.0, 531.0, 532.0, 533.0, 539.0, 560.0], # restricted to specific mentions of Russian relations or foreign aid to Eastern Europe
    'Aid_Russia2' :     [530.0, 531.0, 532.0, 533.0, 539.0, 540.0, 560.0, 585.0], # restricted to specific mentions of Russian relations or foreign aid to Eastern Europe
    'Lift_Embargo' :    [530.0, 550.0], # restrict to general references to "Eastern Bloc" and relations or arms sales
    'Stem_Cells' :      [46.0], # only had anti-abortion
    'School_Vouchers' : [20.0], # only had genreal refernce to school and financial assistance thereof
    'Nuclear_Power' :   [160.0], # specific mention of development of energy resources
    'Ban_TV':           [380.0], # only general mentions of moral decay
    'Defense_Spending': [700, 713, 760] # only specific reference to military strength/benefits
}

# TODO: recode to be more thorough, including consequences of policies.
highball_dict = {
    'NAFTA' :           [10.0, 13.0, 200.0, 424.0, 440.0, 441.0, 442.0, 491.0, 492.0, 493.0, 495.0, 496.0, 497.0], # including concerns about corporate power, economic inequality, economy unspecified, unemployment(!), unions
    'Aid_Russia1' :     [500.0, 530.0, 531.0, 532.0, 533.0, 539.0, 560.0, 710.0, 711.0, 712, 713, 714, 750.0], # added general reference to American prestige abroad, nuclear disarmament, defense spending waste
    'Aid_Russia2' :     [500.0, 530.0, 531.0, 532.0, 533.0, 539.0, 540.0, 560.0, 585.0, 710.0, 711.0, 712, 713, 714, 750.0], # added general reference to American prestige abroad
    'Lift_Embargo' :    [500.0, 530.0, 550.0, 585.0], # added concern for peace, general reference to foreign policy
    'Stem_Cells' :      [46.0], # only had anti-abortion
    'School_Vouchers' : [20.0], # only had genreal refernce to school and financial assistance thereof
    'Nuclear_Power' :   [150.0, 151.0, 153.0, 154.0, 160.0, 199.0], # added any reference to environmental protection, radioactive waste disposal
    'Ban_TV':           [340.0, 380.0], # add compaints about real life crime and violence
    'Defense_Spending': [700, 713, 760, 833, 837, 838, 840] # add complaints about government waste/bloat/spending
}

def code_lowball(issue_name, code):
    if code in lowball_dict[issue_name]:
        return 1
    else:
        return 0

def code_highball(issue_name, code):
    if code in highball_dict[issue_name]:
        return 1
    else:
        return 0


# issue name : [file name, income code, weight code, most impt. issue code]
# consider adding negative wealthy win??
# weight code - excludes single people - doesn't cut that many cases
issues = {
    'NAFTA'             :   ['NES1992.dta', 'V924104', 'V927000', 'V900326'], # note large jump in importance in 1994 survey, taken in 1993 while NAFTA being proposed.
    'Aid_Russia1'       :   ['NES1992.dta', 'V924104', 'V927000', 'V900326'],
    'Aid_Russia2'       :   ['NES1994.dta', 'V941404', 'V940006a','V940706'],
    'Lift_Embargo'      :   ['NES1994.dta', 'V941404', 'V940006a','V940706'],
    'Stem_Cells'        :   ['NES2000.dta', 'V001040', 'V000002', 'V000436'],
    'School_Vouchers'   :   ['NES2000.dta', 'V001040', 'V000002', 'V000436'],
    'Nuclear_Power'     :   ['NES1996.dta', 'V960701', 'V960005', 'V961141'],
    'Ban_TV'            :   ['NES1994.dta', 'V941404', 'V940006a','V940706'],#['NES1992.dta', 'V924104', 'V927000', 'V900326'],
    'Defense_Spending'  :   ['NES1998.dta', 'V980652', 'V980002', 'V980346']
    # removed since GP poll only asks about one aspect of the sweeping bill
    #'Reagan_Taxes'     :   ['NES1984.dta', 'V840680', None, 'V840993']
}

rates_by_class = {}

rates = {}

for key, value in issues.items():
    total_addends = []
    limpt_pop = 0
    himpt_pop = 0

    current_df = 'year_dta_files/' + value[0]
    data = pd.read_stata(current_df)
    total_pop = data[value[2]].sum()

    by_issue = data.groupby(value[3])

    for code in lowball_dict[key]:
        limpt_pop += data[data[value[3]] == code][value[2]].sum()
    
    for code in highball_dict[key]:
        himpt_pop += data[data[value[3]] == code][value[2]].sum()
        total_addends.append(data[data[value[3]] == code][value[2]].sum())

    lbie = str(limpt_pop/total_pop)

    hbie = str(himpt_pop/total_pop)
    
    print(key +': lowball importance est - ' + lbie + '. Highball importance est - ' + hbie)