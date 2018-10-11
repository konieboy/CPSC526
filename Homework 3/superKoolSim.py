# 100 users
# 10 services
# 30 min expire time
# hl = .25
# y = 1 - e^(hlx) for x
import random

ticketList = []
# Time is in min
expireTime = 30
currentTime = 0
eightDaysInMin = 8 * 24 * 60 #11520
#eightDaysInMin = 100
numOfServices = 10
numOfUsers = 100
ticketsCreated = 0
lambd = 0.5
requests = 0

class Ticket(object):
    timeCreated = 0
    user = 0
    service = 0


def make_ticket(time, user, service):
    ticket = Ticket()
    ticket.timeCreated = time
    ticket.user = user
    ticket.service = service
    return ticket


# Generate users

# Check if ticket is valid
def checkTicket (user, service): 
    global ticketsCreated 
    #print (ticketList)
    for ticket in ticketList:
        if (ticket.user == user and ticket.service == service):
            # Check if ticket is expired
            if((currentTime - ticket.timeCreated) > expireTime):
                # Remove old ticket
                ticketList.remove(ticket)
                # Ticket found but expired, create new ticket
                print("Expired ticket found, creating new ticket")
                print("Current Time:", currentTime , "Ticket time: ", ticket.timeCreated)
                ticketList.append(make_ticket(currentTime, user, service))
                ticketsCreated += 1
                return 0
            else: 
                print("Valid ticket found!")
                # Unexpired ticket found, return
                return 0
    # No ticket found, make new ticket
    print ("No ticket found, creating new ticket")
    ticketList.append(make_ticket(currentTime, user, service))
    ticketsCreated += 1
    return 0


# START
while (currentTime < eightDaysInMin):
    
    minBetween = int(round(random.expovariate(lambd)))
    #print minBetween
    currentTime += minBetween

    user = int(round(random.uniform(1, numOfUsers)))
    service = int(round(random.uniform(1, numOfServices)))

    # Todo - Only ask for ticket once every random distribution
    checkTicket(user,service)
    requests += 1

# Print diagnostic information
print("Number of tickets created: ", ticketsCreated)
print("Average tickets per person: ", ticketsCreated / numOfUsers)
print("Average tickets per day: ", ticketsCreated / 8)
print("Ticket Requests: ", requests)





