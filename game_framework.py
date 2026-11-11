import time

running = False
stack = []


def change_mode(mode):
    if stack:
        stack.pop().finish()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    if stack:
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    if stack:
        stack.pop().finish()
    if stack:
        stack[-1].resume()
    else:
        quit()


def quit():
    global running
    running = False


frame_time = 0.0

def run(start_mode):

    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()
    global frame_time
    frame_time = 0.0
    previous_time = time.perf_counter()
    try:
        while running:
            current_time = time.perf_counter()
            frame_time = max(current_time - previous_time, 1e-9)
            previous_time = current_time
            stack[-1].handle_events()
            stack[-1].update()
            stack[-1].render()
    finally:
        running = False
        while stack:
            stack.pop().finish()
