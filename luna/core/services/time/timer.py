def adjust_timer(message):
    if "cancel" in message:
        return #cancel timer and send feedback
    elif "set" in message:
        print('hiya')
        return # determine time and set timer
    elif "change" in message:
        return #change timer
    elif "left" in message:
        return # read out remaining time       