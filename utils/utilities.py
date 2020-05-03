import libevdev


def print_event(e):
    """A utility function for printing event details.

    Args:
        e: The event to print out.
    """
    print("Event: time {}.{:06d}, ".format(e.sec, e.usec), end='')
    if e.matches(libevdev.EV_SYN):
        if e.matches(libevdev.EV_SYN.SYN_MT_REPORT):
            print("++++++++++++++ {} ++++++++++++".format(e.code.name))
        elif e.matches(libevdev.EV_SYN.SYN_DROPPED):
            print(">>>>>>>>>>>>>> {} >>>>>>>>>>>>".format(e.code.name))
        else:
            print("-------------- {} ------------".format(e.code.name))
    else:
        print(
            "type {:02x} {} code {:03x} {:20s} value {:4d}".format(e.type.value, e.type.name, e.code.value, e.code.name,
                                                                   e.value))
