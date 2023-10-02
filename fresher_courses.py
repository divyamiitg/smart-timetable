from typing import final
import numpy as np
import pandas as pd
import re
import string

# created Python modules
import ocr
import helper

def get_fresher_tt_slots():
    #Get tt json
    tt_json = helper.read_tt()

    #Adding tutorial slots
    tt_json['b']['Friday'] = "8:00 - 8:55 AM"
    tt_json['a']['Monday'] = "8:00 - 8:55 AM"
    tt_json['e']['Tuesday'] = "8:00 - 8:55 AM"
    tt_json['d']['Wednesday'] = "8:00 - 8:55 AM"
    tt_json['c']['Thursday'] = "8:00 - 8:55 AM"
    return tt_json

def get_designfresher_courses(roll_number):
    data_map=ocr.get_fresher_DF(roll_number)
    print(data_map)
    # Correct for div 3
    courses=[
        {
            'course':'Engineering Drawing',
            'code':'CE 101',
            'slot':'A',
            'venue':'L2',
            'instructor': 'CE101',
            'ltpc':' ',
            'midsem':'',
            'endsem':''
        },
        {
            'course':'Mathematics - I',
            'code':'MA 101',
            'slot':'B',
            'venue':'L2',
            'instructor': 'MA101',
      "midsem": "2023-09-19T14:00:00.000Z",
      "endsem": "2023-11-20T14:00:00.000Z"
        },
    ]
    if data_map['Division']=='III' or data_map['Division']=='IV':
        for c in courses:
            c['slot']=c['slot']+'1'
    if data_map['Division']=='II' or data_map['Division']=='IV':
        for c in courses:
            c['venue']='L4'
    tutorial=[
        {
            'course':'MA 101 Tutorial',
            'code':'MA 101',
            'slot':'b',
            'instructor':data_map['Location'],
            'venue':'',
            'ltpc':' ',
            'midsem':'',
            'endsem':''
        },
    ]
    lab=[
        {
            'course':'Engineering Drawing Lab',
            'code':'CE 110',
            'slot':'AL' if data_map['Division'] in ['III','IV'] else 'ML',
            'instructor':'CE110',
            'venue':'Engineering Drawing (Practical): 1203 and 1204, Academic Complex (AC)',
            'ltpc':' ',
            'midsem':'',
            'endsem':''
        },
    ]

    # Gettting lab slots
    if data_map['Lab']=='L6' or data_map['Lab']=='L2':
        lab[0]['slot']=lab[0]['slot']+'1'
        lab[1]['slot']=lab[1]['slot']+'4'
        lab[2]['slot']=lab[2]['slot']+'2'
    elif data_map['Lab']=='L7' or data_map['Lab']=='L2':
        lab[0]['slot']=lab[0]['slot']+'3'
        lab[1]['slot']=lab[1]['slot']+'1'
        lab[2]['slot']=lab[2]['slot']+'4'
    elif data_map['Lab']=='L8' or data_map['Lab']=='L3':
        lab[0]['slot']=lab[0]['slot']+'5'
        lab[1]['slot']=lab[1]['slot']+'3'
        lab[2]['slot']=lab[2]['slot']+'1'
    elif data_map['Lab']=='L9' or data_map['Lab']=='L4':
        lab[0]['slot']=lab[0]['slot']+'2'
        lab[1]['slot']=lab[1]['slot']+'5'
        lab[2]['slot']=lab[2]['slot']+'3'
    elif data_map['Lab']=='L20' or data_map['Lab']=='L5':
        lab[0]['slot']=lab[0]['slot']+'4'
        lab[1]['slot']=lab[1]['slot']+'2'
        lab[2]['slot']=lab[2]['slot']+'5'
    # for i in range(len(courses)):
    #     courses[i]['midsem'] = helper.get_midsem_time(courses[i]['slot'])
    #     courses[i]['endsem'] = helper.get_endsem_time(courses[i]['slot'])  

    #Get tt json
    tt_json = get_fresher_tt_slots()

    # adding timings to tut, lab and courses
    for c in courses:
        c['timings'] = tt_json[c['slot']]
    
    for t in tutorial:
        t['timings'] = tt_json[t['slot']]

    for l in lab:
        l['timings'] = tt_json[l['slot']]
 
    midsem_venues = ocr.fetch_venues_DF("midsem")
    endsem_venues = ocr.fetch_venues_DF("endsem")
    final_courses = courses+tutorial+lab
    for course in final_courses:
        midsem_row = midsem_venues[midsem_venues["code"]==course["code"]]
        endsem_row = endsem_venues[endsem_venues["code"]==course["code"]]
        course["midsem_venue"] = helper.return_venue(midsem_row, roll_number)
        course["endsem_venue"] = helper.return_venue(endsem_row, roll_number)

    return {
        'roll_number':roll_number,
        'courses': final_courses
    }

def get_fresher_courses(roll_number):
    data_map=ocr.get_fresher_DF(roll_number)
    print("apple")
    # Correct for div 3
    courses=[
        {
            'course':'Engineering Drawing',
            'code':'CE 101',
            'slot':'A',
            'venue':'L2',
            'instructor': 'CE101',
            'midsem':'',
            'endsem':''
        },
        {
            'course':'Mathematics - I',
            'code':'MA 101',
            'slot':'B',
            'venue':'L2',
            'instructor': 'MA101',
            'ltpc':' ',
      "midsem": "2023-09-19T14:00:00.000Z",
      "endsem": "2023-11-20T14:00:00.000Z"
        },
        {
            'course':'Basic Electronics',
            'code':'EE 101',
            'slot':'C',
            'venue':'L2',
            'instructor': 'EE101',
            'ltpc':' ',
              "midsem": "2023-09-20T14:00:00.000Z",
      "endsem": "2023-11-21T14:00:00.000Z"
        },
        {
            'course':'Chemistry',
            'code':'CH 101',
            'slot':'D',
            'venue':'L2',
            'instructor': 'CH101',
            "midsem": "2023-09-21T14:00:00.000Z",
            "endsem": "2023-11-22T14:00:00.000Z"
        },
        {
            'course':'Physics - I',
            'code':'PH 101',
            'slot':'E',
            'venue':'L2',
            'instructor': 'PH101',
       "midsem": "2023-09-22T14:00:00.000Z",
      "endsem": "2023-11-23T14:00:00.000Z"
        }
    ]
    if data_map['Division']=='I' or data_map['Division']=='II':
        for c in courses:
            c['slot']=c['slot']+'1'
    if data_map['Division']=='II' or data_map['Division']=='IV':
        for c in courses:
            c['venue']='L4'
    tutorial=[
        {
            'course':'MA 101 Tutorial',
            'code':'MA 101',
            'slot':'b',
            'instructor':data_map['Location'],
            'venue': '',
            'midsem':'',
            'endsem':''
        },
        {
            'course':'EE 101 Tutorial',
            'code':'EE 101',
            'slot':'c',
            'venue': '',
            'instructor':data_map['Location'],
            'midsem':'',
            'endsem':''
        },
        {
            'course':'CH 101 Tutorial',
            'code':'CH 101',
            'venue': '',
            'slot':'d',
            'instructor':data_map['Location'],
            'midsem':'',
            'endsem':''
        },
        {
            'course':'PH 101 Tutorial',
            'code':'PH 101',
            'slot':'e',
            'venue': '',
            'instructor':data_map['Location'],
            'midsem':'',
            'endsem':''
        },
    ]
    lab=[
        {
            'course':'Chemistry Laboratory',
            'code':'CH 110',
            'slot':'ML' if data_map['Division'] in ['II','I'] else 'AL',
            'instructor': 'CH110',
            'venue':'Chemistry Laboratory: Department of Chemistry, Academic Complex (AC) ',
            'midsem':'',
            'endsem':''
        },
        {
            'course':'Physics Laboratory' if data_map['Division'] in ['II','I'] else 'Workshop I',
            'code':'PH 110' if data_map['Division'] in ['II','I'] else 'ME110',
            'slot':'AL' if data_map['Division'] in ['III','IV'] else 'ML',
            'instructor': 'PH110' if data_map['Division'] in ['II','I'] else 'ME110',
            'venue':'Department of Physics, Academic Complex (AC)' if data_map['Division'] in ['II','I'] else 'Workshop (on the western side of Academic Complex (AC))',
            'midsem':'',
            'endsem':''
        },
        {
            'course':'Engineering Drawing Lab',
            'code':'CE 110',
            'slot':'AL' if data_map['Division'] in ['III','IV'] else 'ML',
            'instructor': 'CE110',
            'venue':'Engineering Drawing (Practical): 1203 and 1204, Academic Complex (AC)',
            'midsem':'',
            'endsem':''
        },
    ]
    if data_map['Lab']=='L6' or data_map['Lab']=='L2':
        lab[0]['slot']=lab[0]['slot']+'1'
        lab[1]['slot']=lab[1]['slot']+'4'
        lab[2]['slot']=lab[2]['slot']+'2'
    elif data_map['Lab']=='L7' or data_map['Lab']=='L2':
        lab[0]['slot']=lab[0]['slot']+'3'
        lab[1]['slot']=lab[1]['slot']+'1'
        lab[2]['slot']=lab[2]['slot']+'4'
    elif data_map['Lab']=='L8' or data_map['Lab']=='L3':
        lab[0]['slot']=lab[0]['slot']+'5'
        lab[1]['slot']=lab[1]['slot']+'3'
        lab[2]['slot']=lab[2]['slot']+'1'
    elif data_map['Lab']=='L9' or data_map['Lab']=='L4':
        lab[0]['slot']=lab[0]['slot']+'2'
        lab[1]['slot']=lab[1]['slot']+'5'
        lab[2]['slot']=lab[2]['slot']+'3'
    elif data_map['Lab']=='L20' or data_map['Lab']=='L5':
        lab[0]['slot']=lab[0]['slot']+'4'
        lab[1]['slot']=lab[1]['slot']+'2'
        lab[2]['slot']=lab[2]['slot']+'5'
    
    # for i in range(len(courses)):
    #     courses[i]['midsem'] = helper.get_midsem_time(courses[i]['slot'])
    #     courses[i]['endsem'] = helper.get_endsem_time(courses[i]['slot'])

    #Get tt json
    tt_json = get_fresher_tt_slots()

    # adding timings to tut, lab and courses
    for c in courses:
        c['timings'] = tt_json[c['slot']]
    
    for t in tutorial:
        t['timings'] = tt_json[t['slot']]

    for l in lab:
        l['timings'] = tt_json[l['slot']]

    midsem_venues = ocr.fetch_venues_DF("midsem")
    endsem_venues = ocr.fetch_venues_DF("endsem")
    final_courses = courses+tutorial+lab
    for course in final_courses:
        midsem_row = midsem_venues[midsem_venues["code"]==course["code"]]
        endsem_row = endsem_venues[endsem_venues["code"]==course["code"]]
        course["midsem_venue"] = helper.return_venue(midsem_row, roll_number)
        course["endsem_venue"] = helper.return_venue(endsem_row, roll_number)

    return {
        'roll_number':roll_number,
        'courses': final_courses
        # 'courses':courses+tutorial+lab
    }
