from django.contrib.auth.models import User
from congregation.models import *
from photologue.models import *
from random import *
import string

def mailbox_update():
    withboxes = Person.objects.exclude(mailbox__isnull=True)

    for person in withboxes:
        boxes = person.mailbox_set.iterator()
        family = person.household.person_set.iterator()
        for member in family:
            if not member.mailbox_set.values():
                print '%s has no box' % member
                for box in boxes:
                    member.mailbox_set.add(box)

def mailbox_update_noboxes():
    withoutboxes = Person.objects.filter(mailbox__isnull=True)
    for person in withoutboxes:
        print '%s has no box\n    Household - %s' % (person, person.household)
        if person.household:
            family = person.household.person_set.iterator()
            for member in family:
                    if member.mailbox_set.values():
                        print '    Potential Mailbox Found'
                        for box in member.mailbox_set.iterator():
                            if box.id:
                                print '    Found box # %s for %s' % (box.number, member)
                                person.mailbox_set.add(box)

def pwd_generator():
    chars = string.ascii_letters + string.digits
    return "".join(choice(chars) for x in range(randint(8, 16)))

def create_user(username, password):
    temp = User()
    temp.username = username
    temp.set_password(password)

def user_generator():
    mboxes = Mailbox.objects.all().order_by('number')
    for mbox in mboxes:
        print '\nBox #%s\nTry out our new website at its test environment: www.bslcks.info\nYou can change your password after logging in.  \nSometime in the next couple weeks we\'ll move from the testing location over to the usual bslcks.org \nYour account will work there too.\n\t<username>:<password>' % mbox.number
        occupants = mbox.occupants.all().order_by('directory_report_order', 'birth_date')
        for person in occupants:
            if person.user:
                print '\t%s already has a user account' % person
                continue
            else:
                username = person.slug
                password = pwd_generator()
                print '\t%s:%s' % (username, password)
        
                     
def hh_pic_assign():
    pics = Photo.objects.all()
    hh = Household.objects.all()

    for pic in pics:
        title = pic.title[0:-4].split('-')
        try:
            h = hh.filter(name__icontains=title[0]).filter(name__icontains=title[1])
            if len(h) == 1:
                h = h[0]
                if h.picture:
                    print '%s ALREADY HAS A PICTURE' % h
                else:
                    h.picture = pic
                    h.save()
                    print '%s :  %s' % (h, pic)
            else:
                print 'POTENTIAL MULTIPLES FOR %s' % pic
        except:
            print 'NO MATCH FOUND FOR %s' % pic

