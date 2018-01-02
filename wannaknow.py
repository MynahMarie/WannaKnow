import curses
import time
from math import ceil, floor
from curses import wrapper
from stats import getStats
from renders import proc_row, conn_row, usr_row, pck_row
from renders import usr_head, proc_head, pck_head, net_head, usage

def main(stdscr):

    # Clear screen
    stdscr.clear()
    # Curses Settings // DO NOT CHANGE
    curses.curs_set(False)
    stdscr.nodelay(True)

    black = curses.COLOR_BLACK
    curses.init_pair(1, curses.COLOR_WHITE, black)
    curses.init_pair(2, curses.COLOR_RED, black)
    curses.init_pair(3, curses.COLOR_GREEN, black)
    curses.init_pair(4, curses.COLOR_BLUE, black)
    curses.init_pair(5, curses.COLOR_YELLOW, black)
    curses.init_pair(6, curses.COLOR_CYAN, black)
    curses.init_pair(7, curses.COLOR_MAGENTA, black)

    curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_WHITE)
    curses.init_pair(9, black, curses.COLOR_BLUE)

    while True:
        stats = getStats()
        stdscr.clear() # Dont Change!

        # Define section specific variables
        interfaces = stats['network']['interfaces']
        connections = stats['network']['connections']
        num_connects = len(connections.items())
        num_closed = 0
        for i in range(0, num_connects):
            if connections[i]['status'] == 'CLOSE_WAIT':
                num_closed += 1

        procs = stats['processes']
        num_procs = len(stats['processes'].items())

        # Manipulate row numbers according to user input
        try:
            row_conn
        except NameError:
            row_conn = 0

        try:
            row_proc
        except NameError:
            row_proc = 0

        k = stdscr.getch()
        if k == ord('a'):
            if num_connects > connect_height:
                row_conn = connect_height
            curses.flushinp()

        elif k == ord('s'):
            if num_connects > connect_height * 2:
                row_conn = connect_height * 2
            curses.flushinp()

        elif k == ord('d'):
            if num_connects >= connect_height * 3:
                row_c = connect_height * 3
            curses.flushinp()

        elif k == ord('x'):
            row_conn = 0
            curses.flushinp()

        elif k == ord('j'):
            if num_procs >= term_size[0] * 2 - 2:
                row_proc = term_size[0] * 2
            curses.flushinp()

        elif k == ord('k'):
            if num_procs >= term_size[0] * 4 - 2:
                row_proc = term_size[0] * 4
            curses.flushinp()

        elif k == ord('l'):
            if num_procs >= term_size[0] * 6 - 2:
                row_proc = term_size[0] * 6
            curses.flushinp()

        elif k == ord('i'):
            if num_procs >= term_size[0] * 8 - 2:
                row_proc = term_size[0] * 8
            curses.flushinp()

        elif k == ord('m'):
            if num_procs >= term_size[0] * 10 - 2:
                row_proc = term_size[0] * 10
            curses.flushinp()

        elif k == ord('b'):
            row_proc = 0
            curses.flushinp()

        if row_proc >= num_procs - 1:
            row_proc = 0

        # Define max width and height
        term_size = stdscr.getmaxyx()

        # Create sub-windows
        win_width = term_size[1] / 3

        term_1 = stdscr.subwin(term_size[0], floor(win_width) - 2, 0, 0)
        term_2 = stdscr.subwin(term_size[0], floor(win_width), 0, floor(win_width) - 3)
        term_3 = stdscr.subwin(term_size[0], floor(win_width), 0, floor(win_width * 2) - 3)

        # Left column of terminal screen (term_1)
        curr = term_1.getyx()

        col_2 = (curr[0], curr[1] + (floor(win_width/5)) - 5)
        col_3 = (curr[0], curr[1] + (floor((win_width/5)*2)) - 4)
        col_4 = (curr[0], curr[1] + (floor((win_width/5)*3)) - 7)
        col_5 = (curr[0], curr[1] + (floor((win_width/5)*4)) - 3)

        usr_head(term_1, col_2, col_3, col_4, col_5, 4)

        for c in range(0, len(stats['users'].items())):
            user = stats['users'][c]

            curr = term_1.getyx()

            col_2 = (curr[0], curr[1] + (floor(win_width/5)) - 2)
            col_3 = (curr[0], curr[1] + (floor((win_width/5)*2)) - 1)
            col_4 = (curr[0], curr[1] + (floor((win_width/5)*3)) - 5)
            col_5 = (curr[0], curr[1] + floor((win_width/5)*4))

            usr_row(term_1, user, col_2, col_3, col_4, col_5, 3, 1)

        # Network Info Display (Packets)
        curr = term_1.getyx()
        col_2 = (curr[0], curr[1] + floor(win_width/5))

        # Save the current location as coordinates to print the usage later on.
        col_instruct = (col_2[0] + 1, col_2[1] + floor((win_width/5))*2 - 3)

        pck_head(term_1, col_2, 8, 4, win_width)

        for i in range(0, len(interfaces.items())):
            curr = term_1.getyx()

            col_2 = (curr[0], curr[1] + floor(win_width/5))
            pck_row(term_1, interfaces, col_2, i, 3, 2)

        net_head(term_1, num_connects, num_closed)

        curr = term_1.getyx()
        connect_height = term_size[0] - curr[0] - 1
        col_2 = (curr[0], curr[1] + (floor(win_width/5)) - 5)

        if row_conn > 0:
            row_c = row_conn
        else:
            row_c = 0

        for c in range(curr[0], term_size[0] - 1):
            cur = term_1.getyx()
            col_2 = (cur[0], cur[1] + (floor(win_width/5)) - 4)
            col_3 = (cur[0], cur[1] + (floor((win_width/5)*2)) + 1)
            col_4 = (cur[0], cur[1] + (floor((win_width/5)*3)) - 3)

            conn_row(term_1, connections, col_2, col_3, col_4, row_c, 3, 1, 4, 5, 9)
            row_c += 1
            if row_c == num_connects - 1:
                break

        # Print instructions
        usage(term_1, col_instruct)

        term_1.refresh()

        # Middle column of terminal screen (term_2)
        #Processes
        curr = term_2.getyx()
        col_2 = (curr[0], curr[1] + (floor(win_width/5)) - 5)
        col_3 = (curr[0], curr[1] + (floor((win_width/5)*3)))

        proc_head(term_2, col_2, col_3, 7, 8)

        curr = term_2.getyx()

        if row_proc > 0:
            row_p = row_proc
        else:
            row_p = 0

        h1 = term_size[0] - 1
        remains = num_procs - row_p
        if h1 > remains:
            h1 = remains

        for c in range(curr[0], h1):
            curr = term_2.getyx()
            col_2 = (curr[0], curr[1] + (floor(win_width/5)) - 6)
            col_3 = (curr[0], curr[1] + (floor((win_width/5)*3)))
            col_4 = (curr[0], curr[1] + (floor((win_width/5)*4)) + 3)

            if procs[row_p]['user'] == 'root':
                proc_row(term_2, procs, col_2, col_3, col_4, row_p, 2)

            elif procs[row_p]['user'] == stats['users'][0]['name']:
                proc_row(term_2, procs, col_2, col_3, col_4, row_p, 6)

            else:
                proc_row(term_2, procs, col_2, col_3, col_4, row_p, 5)
            row_p += 1

        term_2.refresh()

        # Right column of terminal screen (term_3)
        curr = term_3.getyx()
        col_2 = (curr[0], curr[1] + (floor(win_width/5)) - 5)
        col_3 = (curr[0], curr[1] + (floor((win_width/5)*3)))

        proc_head(term_3, col_2, col_3, 7, 8)

        curr = term_3.getyx()

        h2 = term_size[0] - 1
        remains = num_procs - row_p
        if h2 > remains:
            h2 = remains

        for a in range(curr[0], h2):
            curr = term_3.getyx()
            col_2 = (curr[0], curr[1] + (floor(win_width/5)) - 6)
            col_3 = (curr[0], curr[1] + (floor((win_width/5)*3)))
            col_4 = (curr[0], curr[1] + (floor((win_width/5)*4)) + 3)

            if procs[row_p]['user'] == 'root':
                proc_row(term_3, procs, col_2, col_3, col_4, row_p, 2)

            elif procs[row_p]['user'] == stats['users'][0]['name']:
                proc_row(term_3, procs, col_2, col_3, col_4, row_p, 6)
            else:
                proc_row(term_3, procs, col_2, col_3, col_4, row_p, 5)
            row_p += 1

        term_3.refresh()

        #DO NOT CHANGE BELOW THIS LINE
        # stdscr.refresh()
        time.sleep(0.3)

wrapper(main)
