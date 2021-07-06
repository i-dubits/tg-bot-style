import logging

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from pathlib import Path

from IPython.core.debugger import set_trace

from aiogram.utils.helper import Helper, HelperMode, ListItem

from bot import config, messages, utils
#from config import TOKEN, file_path_to_download
#from messages import MESSAGES
#from utils import Nst, Cycle

from nst import nst_2 as nstk
from run_cyclegan import RunCycle

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG)


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(state = '*', commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(messages.MESSAGES['start'])
    
@dp.message_handler(state = '*', commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(messages.MESSAGES['help'])
    

#NST
#_______________________________

@dp.message_handler(state = '*', commands=['nst'])
async def init_NST(message: types.Message):
    
    state = dp.current_state(user=message.from_user.id)

    await utils.Nst.waiting_for_content_image.set()
    await message.reply(messages.MESSAGES['NST_init'], reply=False)

# Upload photos    
@dp.message_handler(state = utils.Nst.waiting_for_content_image, content_types=['photo'])
async def upload_content_nst_image(message: types.Message):
    
    state = dp.current_state(user=message.from_user.id)

    file_path = config.file_path_to_download
    file_name = 'nst_content_' + str(message.from_user.id) + '.jpg'

    await message.photo[-1].download(file_path + file_name)
    await utils.Nst.waiting_for_style_image.set()
    await message.reply(messages.MESSAGES['NST_first_image'], reply=False)
    
@dp.message_handler(state = utils.Nst.waiting_for_style_image, content_types=['photo'])
async def upload_style_nst_image(message: types.Message):
    
    state = dp.current_state(user=message.from_user.id)

    file_path = config.file_path_to_download
    file_name = 'nst_style_' + str(message.from_user.id) + '.jpg'

    await message.photo[-1].download(file_path + file_name)
    await utils.Nst.waiting_for_result.set()
    await message.reply(messages.MESSAGES['NST_sec_image'], reply=False)
    
    img_proc = nstk.Image_proc(128, "cpu")      # image size
    
    file_path = config.file_path_to_download
    file_name_cont = 'nst_content_' + str(message.from_user.id) + '.jpg'
    file_name_style = 'nst_style_' + str(message.from_user.id) + '.jpg'
    
    cont_img = await img_proc.image_loader(file_path + file_name_cont)
    style_img = await img_proc.image_loader(file_path + file_name_style)
    
    run_nst = nstk.Run_NST(style_img, cont_img, "cpu")
    
    result = await run_nst.run_style_transfer(num_steps=250, style_weight=1000000, content_weight=100)
    file_name_result = 'result_nst_' + str(message.from_user.id) + '.jpg'
    await img_proc.my_imsave(result, filename = file_path + file_name_result)
    
    with open(file_path + file_name_result, 'rb') as photo:
        await message.reply_photo(photo, caption='NST result')
  
# Upload files    
@dp.message_handler(state = utils.Nst.waiting_for_content_image, content_types=['document'])
async def upload_content_nst_file(message: types.Message):
   
    state = dp.current_state(user=message.from_user.id)

    file_path = config.file_path_to_download
    file_name = 'nst_content_' + str(message.from_user.id) + '.jpg'

    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path_server = file.file_path


    await bot.download_file(file_path_server, file_path + file_name) 
    await utils.Nst.waiting_for_style_image.set()
    await message.reply(messages.MESSAGES['NST_first_image'], reply=False) 

@dp.message_handler(state = utils.Nst.waiting_for_style_image, content_types=['document'])
async def upload_style_nst_file(message: types.Message):
    
    state = dp.current_state(user=message.from_user.id)

    file_path = config.file_path_to_download
    file_name = 'nst_style_' + str(message.from_user.id) + '.jpg'

    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path_server = file.file_path


    await bot.download_file(file_path_server, file_path + file_name) 
    await utils.Nst.waiting_for_result.set()
    await message.reply(messages.MESSAGES['NST_sec_image'], reply=False)

    img_proc = nstk.Image_proc(128, "cpu")      # image size
    
    file_path = config.file_path_to_download
    file_name_cont = 'nst_content_' + str(message.from_user.id) + '.jpg'
    file_name_style = 'nst_style_' + str(message.from_user.id) + '.jpg'
    
    cont_img = await img_proc.image_loader(file_path + file_name_cont)
    style_img = await img_proc.image_loader(file_path + file_name_style)
    
    run_nst = nstk.Run_NST(style_img, cont_img, "cpu")
    
    result = await run_nst.run_style_transfer(num_steps=250, style_weight=1000000, content_weight=100)
    file_name_result = 'result_nst_' + str(message.from_user.id) + '.jpg'
    await img_proc.my_imsave(result, filename = file_path + file_name_result)
    
    with open(file_path + file_name_result, 'rb') as photo:
        await message.reply_photo(photo, caption='NST result')

#CycleGan
#_______________________________

@dp.message_handler(state = '*', commands=['cycle'])
async def init_cycle(message: types.Message):
    
    state = dp.current_state(user=message.from_user.id)

    await utils.Cycle.waiting_for_content_image.set()
    await message.reply(messages.MESSAGES['cycle_init'], reply=False)

# Upload photo
@dp.message_handler(state = utils.Cycle.waiting_for_content_image, content_types=['photo'])
async def upload_content_cycle_image(message: types.Message):
    
    state = dp.current_state(user=message.from_user.id)

    file_path = config.file_path_to_download
    folder_name = 'cycle_content_' + str(message.from_user.id)
    file_name = 'cycle_content_' + str(message.from_user.id) + '.jpg'
    output_name = 'cycle_res_' + str(message.from_user.id) + '.jpg'
    
    Path(file_path + folder_name).mkdir(parents=True, exist_ok=True)

    await message.photo[-1].download(file_path + '/' + folder_name + '/' + file_name)
    await utils.Cycle.waiting_for_result.set()
    await message.reply(messages.MESSAGES['cycle_first_image'], reply=False)
    
    curr_gan = RunCycle(file_path + '/' + folder_name, file_path + '/' + folder_name + '/' + output_name, config.checkpoint_dir)
    
    await curr_gan.run_network()
    
    with open(file_path + '/' + folder_name + '/' + output_name, 'rb') as photo:
        await message.reply_photo(photo, caption='CycleGan result')

# Upload file
@dp.message_handler(state = utils.Cycle.waiting_for_content_image, content_types=['document'])
async def upload_content_cycle_file(message: types.Message):
   
    state = dp.current_state(user=message.from_user.id)

    file_path = config.file_path_to_download
    folder_name = 'cycle_content_' + str(message.from_user.id)
    file_name = 'cycle_content_' + str(message.from_user.id) + '.jpg'
    output_name = 'cycle_res_' + str(message.from_user.id) + '.jpg'
    
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path_server = file.file_path

    Path(file_path + folder_name).mkdir(parents=True, exist_ok=True)
    #set_trace()
    
    await bot.download_file(file_path_server, file_path + '/' + folder_name + '/' + file_name) 
    await utils.Nst.waiting_for_style_image.set()
    await message.reply(messages.MESSAGES['cycle_first_image'], reply=False) 

    curr_gan = RunCycle(file_path + '/' + folder_name, file_path + '/' + folder_name + '/' + output_name, config.checkpoint_dir)
    
    await curr_gan.run_network()
    
    with open(file_path + '/' + folder_name + '/' + output_name, 'rb') as photo:
        await message.reply_photo(photo, caption='CycleGan result')

# General handlers
#_______________________________
    
@dp.message_handler(state = '*', commands=['reset'])
async def reset_state(message: types.Message):
    
    state = dp.current_state(user=message.from_user.id)
    
    await state.finish()
    await message.reply(messages.MESSAGES['reset_state'], reply=False)


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)
    
async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    
    
if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
