def process_command(line):
    print('(Processing command: ' + line.strip() + ')')

def event_keydown(key): # running in main_greenlet
    # jump into g_processor, sending it the key
    word = g_processor.switch(key)


def gui_mainloop():
   # The user types "hello"
   for c in 'hello\n':
       event_keydown(c)
   # The user types "quit"
   for c in 'quit\n':
       event_keydown(c)
   # The user responds to the prompt with 'y'
   event_keydown('y')

def read_next_char(): # running in g_processor
    # jump to the main greenlet, where the GUI event
    # loop is running, and wait for the next key
    next_char = main_greenlet.switch('blocking in read_next_char')
    return next_char

def echo_user_input(user_input):
    print('    <<< ' + user_input.strip())
    return user_input

def process_commands():
   while True:
       line = ''
       while not line.endswith('\n'):
           line += read_next_char()
       echo_user_input(line)
       if line == 'quit\n':
           print("Are you sure?")
           if echo_user_input(read_next_char()) != 'y':
               continue    # ignore the command
           print("(Exiting loop.)")
           break # stop the command loop
       process_command(line)


from greenlet import greenlet
g_processor = greenlet(process_commands)

main_greenlet = greenlet.getcurrent()

g_processor.switch()

gui_mainloop()