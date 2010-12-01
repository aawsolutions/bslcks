from congregation.models import *


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

def noboxes():
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
                 
