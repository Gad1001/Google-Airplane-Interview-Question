airports = ["BGI","CDG","DEL","DOH","DSM","EWR","EYW","HND","ICN","JFK","LGA","LHR","ORD","SAN","SFO","SIN","TLV","BUD"]
routes = [
    ["DSM","ORD"],
    ["ORD","BGI"],
    ["BGI","LGA"],
    ["SIN","CDG"],
    ["CDG","SIN"],
    ["CDG","BUD"],
    ["DEL","DOH"],
    ["DEL","CDG"],
    ["TLV","DEL"],
    ["EWR","HND"],
    ["HND","ICN"],
    ["HND","JFK"],
    ["ICN","JFK"],
    ["JFK","LGA"],
    ["EYW","LHR"],
    ["LHR","SFO"],
    ["SFO","SAN"],
    ["SFO","DSM"],
    ["SAN","EYW"],
    ]
startingAirport = "LGA"



def GetAllDestOfSource(source,routes):
    dests = set()
    for route in routes:
        if(source == route[0]):
            dests.add(route[1])
    return dests

def addDest(dest,allSubDest,routes):
    if dest not in allSubDest:
        allSubDest.add(dest)
        topTreeDest = GetAllDestOfSource(dest,routes)
        for innerdest in topTreeDest:
            addDest(innerdest,allSubDest,routes)

def GetMissingRoutes(airports,routes,startingAirport):
    sourcesOfRoutes = set()
    for route in routes:
        sourcesOfRoutes.add(route[0])

    groups = {}
    for source in sourcesOfRoutes:
        groups[source]=set()
    
    for source,allSubDest in groups.items():
        addDest(source,allSubDest,routes)

    #right now we got a dictionary of groups where each value of a key group in groups is a set of all sub-destinations we need to check for connection between groups
    #the code here is a bit messy beacuse we cannot pop from dictionary while looping on it so we loop and if we need to pop we break and then start over
    need_repeat = True
    while(need_repeat):
        need_repeat = False
        did_break = False
        tmp_source = ""
        for source,allSubDest in groups.items():
            if (not (source == startingAirport)):
                #We don't want to filter out a group whom start at the startingAirport because of reasons that i will explain at end of code
                for inner_loop_source,inner_loop_allSubDest in groups.items():
                    if (not (source == inner_loop_source)):
                        #if they are the same we look at ourself group so no point checking this
                        if source in inner_loop_allSubDest:
                            #this "tree" is already inside another group no nedd for it
                            did_break = True
                            break
                if(did_break):
                    tmp_source = source
                    break
        if(did_break):
            need_repeat = True
            groups.pop(tmp_source)
    
    #now we got filtered groups with no connection. BUT we have to add all airports with no routes at all (wierd but just to make sure)
    combinedSubDest = set()
    for source,allSubDest in groups.items():
        combinedSubDest.update(allSubDest)
    
    for airport in airports:
        if airport not in combinedSubDest:
            groups[airport] = set()

    #now we got filtered groups with no connection all we have to do is to return the sources of the groups minus the group whom source is startingAirport(if exist)
    answer = set()
    for source in groups:
        answer.add(source)
    answer.discard(startingAirport)
    
    return answer

print(GetMissingRoutes(airports,routes,startingAirport))