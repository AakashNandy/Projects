# This function caklls on the other function in the program to determine things like if the user is tired or will get a star, etc. It then determines the number of health points and hedons the user has. More in depth explanations below.
def perform_activity(activity, duration):
    global activity1
    global duration1
    x = activity1
    y = duration1
    activity1 = activity
    duration1 = duration

# This checks if the same activity was completed the last time perform_activity() was run. If it was then the durations have to be 'pushed forward' by that amount, this time by detting the variable z = to the previous value duration.
    global health
    if x == activity:
        z = y
    else:
        z = 0

# This determines the number of health points the user gets by checking the duration of the activity and what the activity is. It also takes into account if the activity is being carried over from the last time perform_activity() was run using the z variable which was assigned a value above.
    if activity == 'running':
        if duration <= (180 - z):
            health = health + (3 * duration)
        else:
            health = health + (3 * (180 - z)) + (duration - (180 - z))
    elif activity == 'textbooks':
        health = health + (2 * duration)
    elif activity == 'resting':
        health = health
    else:
        print('Not a valid activity.')

# Runs a function to check if the user performed activities 'running' or 'textbooks' in the last 120 minutes. In-depth explanation is in the check_tired() function.
    global tired
    check_tired()

# Runs a function to check if the user can take a star for the activity that was chosen when perform_activity() was run. In-depth explanation is in the star_can_be_taken(). function.
    global star
    global activity2
    star_can_be_taken(activity)

# Adds or subtracts hedons from the user's amount based on the activity being performed, if a star is available(determined by using star_can_be_taken()) and if the user is tired(determined by using check_tired()).
    global hedons
    if activity == 'resting':
        star = 0
    elif tired == 0 and star == 0:
        if activity == 'running':
            if duration <= 10:
                hedons = hedons + (2 * duration)
            elif duration > 10:
                hedons = hedons + (2 * 10) + ((duration - 10) * -2)
        elif activity == 'textbooks':
            if duration <= 20:
                hedons = hedons + duration
            else:
                hedons = hedons + 20 - (duration - 20)
    elif tired == 1 and star == 0:
        if activity == 'running' or activity == 'textbooks':
            hedons = hedons + (duration * -2)
    elif tired == 0 and star == 1:
        if activity == 'running':
            if duration <= 10:
                hedons = hedons + (5 * duration)
            else:
                hedons = hedons + (5 * 10) + (duration - 10)
        elif activity == 'textbooks':
            if duration <= 20:
                hedons = hedons + (duration * 4)
            else:
                hedons = hedons + 80 + ((duration - 20) * 2)
        star = 0
    elif tired == 1 and star ==1:
        if activity == 'running' or activity == 'textbooks':
            if duration <= 10:
                hedons = hedons + duration
            elif duration >= 10:
                hedons = hedons + 10 - (2*(duration - 10))
        star = 0
    else:
        print('Not a valid activity.')
    activity2 = 0



def check_tired():
    global activity1
    global duration1
    global tired
    global mem
    global time_pass_tired
# This function checks if the user is tired by appending the durations of the activities and the activities themselves into a list. It then checks if the duration is over or under 120 minutes. If over, it clears the list or removes elements of the list that tracks durations until that the sum of all those elements is less than 120. It also checks if one of the elements of the list trackking activities is running or textbooks. If it is, then it sets the variable tired = 1 to indicate that the user is tired.
    if duration1 >= 120:
        time_pass_tired.clear()
        if 'running' in mem or 'textbooks' in mem:
            tired = 1
        else:
            tired = 0
        mem.clear()
        mem.append(activity1)
    elif duration1 < 120:
        time_pass_tired.append(duration1)
        if sum(time_pass_tired) >= 120:
            time_pass_tired.pop(0)
            if 'running' in mem or 'textbooks' in mem:
                tired = 1
            else:
                tired = 0
            mem.pop(0)
            mem.append(activity1)
        elif sum(time_pass_tired) < 120:
            if 'running' in mem or 'textbooks' in mem:
                tired = 1
            else:
                tired = 0
            mem.append(activity1)


def star_can_be_taken(activity):
    global activity2
    global duration1
    global star
    global bored
    global time_pass_star
#This function works similarly to the check_tired() function by appending the durations into a list. If the sum of the duration in the list is over 120 it removes elements. If the bored variable - which is added to by one each time a star is offered - reaches 3 before the list while the sum of the duration list is still less than 120 then the star cannot be taken because the user is bored of stars.
    if activity2 == 'running' or activity2 == 'textbooks':
        if activity == activity2:
            right_activity = 1
        else:
            right_activity = 0

        if duration1 >= 120:
            time_pass_star.clear()
            bored = 1
        elif duration1 < 120:
            time_pass_star.append(duration1)
            if sum(time_pass_star) >= 120:
                time_pass_star.pop(0)
                bored = 1
            elif sum(time_pass_star) < 120:
                bored = bored + 1
        if right_activity == 1 and bored == 1:
            star = 1
            return True
        elif right_activity == 1 and bored == 2:
            star = 1
            return True
        else:
            star = 0
            return False
        activity2 = 0
    else:
        star = 0
        activity2 = 0


# Offers a star for the activity and then globals that activity so that it can be checked using the star_can_be_taken() function.
def offer_star(activity):
    global activity2
    activity2 = activity

# Checks the number of hedons.
def get_cur_hedons():
     global hedons
     return hedons

# Checks the number of health points.
def get_cur_health():
    global health
    return health


def most_fun_activity_minute():
    global tired
    global activity2
    global star
    global bored
    global previous_bored
    previous_bored = bored
# Checks the activity that gives the most hedons in that moment by running the check_tired() and star_can_be_taken() functions but doesn't update values like if the user is bored like it does when these two functions are run in the perform_activity() function.
    check_tired()
    if tired == 0:
        return 'running'
    elif tired == 1:
        star_can_be_taken('running')
        bored = previous_bored
        if star == 1:
            return 'running'
        elif star == 0:
            star_can_be_taken('textbooks')
            bored = previous_bored
            if star == 1:
                return 'textbooks'
            elif star == 0:
                return 'resting'

# Defines all global variables and lists
def initialize():
    global hedons
    hedons = 0
    global health
    health = 0
    global star
    star = 0
    global tired
    tired = 0
    global bored
    bored = 0
    global activity1
    activity1 = 0
    global duration1
    duration1 = 0
    global activity2
    activity2 = 0
    global mem
    mem = []
    global time_pass_tired
    time_pass_tired = []
    global time_pass_star
    time_pass_star = []
    global previous_bored
    previous_bored = 0

