#  if name in ['unknown_person', 'no_persons_found']:
#                 util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
#             else:
#                 util.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
#                 with open(self.log_path, 'a') as f:
#                     f.write('{},{},in\n'.format(name, datetime.datetime.now()))
#                     f.close()

#         else:
#             util.msg_box('Hey, you are a spoofer!', 'You are fake !')