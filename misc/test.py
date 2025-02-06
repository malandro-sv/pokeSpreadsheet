import time

def newQuery(maxPages):

    count = 0
    timex = "time.time()"
    condition = (count < maxPages) if maxPages\
                else timex
    while count < maxPages if maxPages else timex:
        print(count, condition, maxPages)
        count += 1
        time.sleep(.5)
        #condition = count < maxPages

