from csv import DictReader
import os
import re
from datetime import datetime

from django.template.defaultfilters import slugify

from django.db import models
from django.core.exceptions import ValidationError

from congregation.models import Person, Household, Mailbox


def record_person(p):

    #Basic clean-up and formatting removes numeric/non-letters from names, cleans up dates to standard format
    #all unknown dates stored as '??/??/YYYY' converted to '01/01/YYYY'
    p['First name'] = re.sub('\W','',p['First name'])
    p['Last name'] = re.sub('\W','',p['Last name'])
    p['Preferred name'] = re.sub('\W','',p['Preferred name'])
    p['Household #'] = int(p['Household #'])
    if p['Birth date']:
        p['Birth date'] = re.sub('\?{2}','01', p['Birth date'])
    if p['Baptism Date']:
        p['Baptism Date'] = re.sub('\?{2}','01', p['Baptism Date'])
    if p['Membership date']:
        p['Membership date'] = re.sub('\?{2}','01', p['Membership date'])

    #initialize temporary Person t
    t = Person()

    #Household Association
    n = 1
    try:
        #if the household already exists, checks to see if the Household.name needs updated with the 
        #primary (head of household) salutation
        h = Household.objects.get(bslc_household=p['Household #'])
        if p['Directory/report order'] == 'Primary':
            h.name = u'%s %s' % (p['Salutation'],p['Last name'])
            h.slug = slugify(h.name)
            h.save()
    except:
        #if it does not exist, initialize temporary Household h
        h = Household()
        h.name = u'%s %s' % (p['Salutation'],p['Last name'])

        #if the slug already exists, iterates an integer value until it's unique
        tslug = slugify(h.name)
        while True:
            try:
                Household.objects.get(slug=tslug)
                tslug += u'%s' % n
                n += 1
            except:
                break
        h.slug = tslug

        #h.apartment not used in auto-load due to differences in how it's handled in the source
        #zipcode is not set to accept the extra '<zip>-xxxx', and in source the City/State are not separated
        h.address = p['Address1']
        h.zipcode = p['Zip code'][0:5]
        cutout = len(p['City State'])
        h.state = p['City State'][cutout-2:cutout]

        #temporary phone number r
        #strip formatting from phone numbers, if no area code present, assumed to be 913
        r = re.sub("[^0-9]", "", p['Home phone'])
        if len(r) == 7:
            r = '%s-%s-%s' % ('913',r[0:3],r[3:7])
        else:
            r = '%s-%s-%s' % (r[0:3], r[3:6], r[6:10])            
        h.household_phone = r

        if p['Unlisted home phone'] == 'No':
            h.unlisted_number = False
        else:
            h.unlisted_number = True
        print "BSLC Household # - %s" % (p['Household #'])
        h.bslc_household = p['Household #']
        h.save()
        

    if p['Gender'] == 'Male':
        t.gender = 'm'
    else:
        t.gender = 'f'

    #date values are stored as datetime objects unless the source contains incorrect # of #'s or inconsistent format
    if p['Birth date']:
        try:
            t.birth_date = datetime.strptime(p['Birth date'],"%m/%d/%Y").date()
        except:
            print "Birthday Error"

    if p['Baptism Date']:
        try:
            t.baptism_date = datetime.strptime(p['Baptism Date'],"%m/%d/%Y").date()
        except:
            print "Baptism Date Error"

    t.first_name = p['First name']
    if p['Use pref name'] == 'Yes':
        t.preferred_first_name = p['Preferred name']    
    t.middle_name = p['Middle name']
    t.last_name = p['Last name']
    if p['Suffix']:
        t.suffix = p['Suffix']

    #slug is concatenation of <preferred or >first-last
    if p['Use pref name'] == 'Yes':
        t.slug = slugify(p['Preferred name']+' '+p['Last name'])
    else:
        t.slug = slugify(p['First name']+' '+p['Last name'])

    #if there is a slug conflict, the older person gets the smaller integer, 
    #this cascades accross all conflicts
    n = 1
    while True:
        try:
            doppel = Person.objects.get(slug=t.slug)
            #To do a date-based increment both must have a birth-day
            if t.birth_date: 
                if doppel.birth_date:
                    if t.birth_date > doppel.birth_date:
                        doppel.slug += u'%s' % n
                        t.slug += u'%s' % (n+1)
                        doppel.save()
                        n += 1
                    else:
        
                        t.slug += u'%s' % n
                        doppel.slug += u'%s' % (n+1)
                        doppel.save()
                        n += 1
                else:
                    doppel.slug += u'%s' % n
                    t.slug += u'%s' % (n+1)
                    doppel.save()
                    n += 1

        except:
            break

    #opting into directory is a condition for processing, so set to True
    t.opt_in_directory = True

    #All children, for example, will have report_order of 3.  In queries, have the results order first by 
    #directory report order and then by birthday
    if p['Directory/report order'] == 'Primary':
        t.directory_report_order = 1
    elif p['Directory/report order'] == 'Secondary':
        t.directory_report_order = 2
    else:
        t.directory_report_order = 3

    if p['Membership date']:
        try:
            t.joined = datetime.strptime(p['Membership date'],"%m/%d/%Y").date()
        except:
            print "Membership Date Error"

    t.email = p['E-Mail']

    #temporary phone number r
    #strip formatting from phone numbers, if no area code present, assumed to be 913
    #done for both landline and cell phone
    r = re.sub("[^0-9]", "", p['Home phone'])
    if len(r) == 7:
        r = '%s-%s-%s' % ('913',r[0:3],r[3:7])
    else:
        r = '%s-%s-%s' % (r[0:3], r[3:6], r[6:10]) 
    t.landline = r

    if p['cel phone']:
        r = re.sub("[^0-9]", "", p['cel phone'])
        if len(r) == 7:
            r = '%s-%s-%s' % ('913',r[0:3],r[3:7])
        else:
            r = '%s-%s-%s' % (r[0:3], r[3:6], r[6:10]) 
        t.cellphone = r

    print "INDIVID # = %s" % p['Indiv #']
    t.bslc_individual = p['Indiv #']
    t.save()
    
    #add the newly saved person to the household
    h.person_set.add(t)
    if p['Mailbox #']:
        try:
            m = Mailbox.objects.get(number=int(p['Mailbox #']))
            t.mailbox_set.add(m)
        except:
            m = Mailbox(number = int(p['Mailbox #']))
            m.save()
            t.mailbox_set.add(m)


    #The following fields are not part of the initial import script
    #t.user 
    #t.active 
    #t.member 
    #t.role     
    #t.left 
    #t.talents 
    #t.relations 
    #t.bio 
    #t.picture 
    #t.deceased 

def number1():
    filename = '/home/apt9online/src/bslcks/jtest.csv'
    cong = DictReader(open(filename))

    while True:
        p = cong.next()
        print cong.line_num
        if p['Include on directory'] == 'Yes':
          if p['Family relation'] <> 'Duplicate':
            try:
                Person.objects.get(bslc_individual=p['Indiv #'])
                print "%s %s already exists in the DB" % (p['First name'],p['Last name'])
            except:
                record_person(p)

