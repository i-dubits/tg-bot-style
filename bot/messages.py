


help_start_message = 'Hi! This is Style transfer bot. You can use NST (type /nst) or CycleGan (/cycle) to process your image. \n' \
                     'You can /reset process at any time \n'

NST_init = 'Please upload content image for NST \n'
NST_first_image = 'Please upload style image for NST \n'
NST_sec_image = 'Your images are being proccessed. It will take about 5 minutes \n'

cycle_init = 'Please upload content image for CycleGan \n'
cycle_first_image = 'Your image is being proccessed. It will take a few minutes \n'

reset_state = 'Process has been reseted \n'

MESSAGES = {
    'start': help_start_message,
    'help': help_start_message,
    'NST_init': NST_init,
    'NST_first_image': NST_first_image,
    'NST_sec_image': NST_sec_image,
    'reset_state': reset_state,
    'cycle_init': cycle_init,
    'cycle_first_image': cycle_first_image,
}