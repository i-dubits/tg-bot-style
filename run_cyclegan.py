


#import sys

#sys.path.insert(1, 'd/My Documents/Обучение после аспирантуры/ML/Курс Stepik Deep learning/Проект/Bot_ver_3/bot')



#from config import check_p_dir, data_root_cycle_gan
from bot import config as cg


import os
from options.test_options import TestOptions
from data import create_dataset
from models import create_model
from util.visualizer import save_images
from util import html

from IPython.core.debugger import set_trace


from util import util

import copy

import asyncio

#check_p_dir = cg.checkpoint_dir

#data_root_cycle_gan = cg.data_root_cycle_gan
#data_root_cycle_gan = 'd:/temp/CycleGan/summer2winter_yosemite_2'

#file_path_to_download = cg.file_path_to_download


class RunCycle:
    
    def __init__(self, image_folder_path, output_path_file_name, check_p_dir):
       
        self.image_folder_path = image_folder_path
        self.output_path_file_name = output_path_file_name
        self.check_p_dir = check_p_dir
        
        self.opt = TestOptions()
        # hard-code some parameters for test
        self.opt.num_threads = 0   # test code only supports num_threads = 0
        self.opt.batch_size = 1    # test code only supports batch_size = 1
        self.opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
        self.opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
        self.opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
        
        # my hard-coded parameters
        self.opt.aspect_ratio = 1.0
        self.opt.checkpoints_dir = self.check_p_dir
        self.opt.crop_size = 256
        self.opt.dataroot = self.image_folder_path
        self.opt.dataset_mode = 'single'
        self.opt.direction = 'AtoB'
        self.opt.epoch = 'latest'
        self.opt.eval = True        
        self.opt.gpu_ids = []
        self.opt.init_gain = 0.02
        self.opt.init_type = 'normal'
        self.opt.input_nc = 3 
        self.opt.isTrain = False
        self.opt.load_iter = 0
        self.opt.load_size = 256
        self.opt.max_dataset_size = 100.     # ? Class<float> default = inf
        self.opt.model = 'test'
        self.opt.model_suffix = ''
        self.opt.n_layers_D = 3
        self.opt.name = 'summer2winter_yosemite.pth'
        self.opt.ndf4 = 64
        self.opt.netD = 'basic'
        self.opt.netG = 'resnet_9blocks'
        self.opt.ngf = 64                            
        self.opt.no_dropout = True                      
        self.opt.norm = 'instance'                      
        self.opt.num_test = 1                            
        self.opt.output_nc = 3                             
        self.opt.phase = 'test'                          
        self.opt.preprocess = 'none'  # default 'resize_and_crop' !!! 'none' works fine but longer for large images               
        self.opt.results_dir ='./results/'                          
        self.opt.suffix = ''                               
        self.opt.verbose = False 
        
        self.opt.display_winsize = 256
        
    async def run_network(self):
        
        await asyncio.sleep(0.1)
        dataset = create_dataset(self.opt)  # create a dataset given opt.dataset_mode and other options
        await asyncio.sleep(0.1)
        model = create_model(self.opt)      # create a model given opt.model and other options
        await asyncio.sleep(0.1)
        model.setup(self.opt) 
       
        if self.opt.eval:
            model.eval()
            
        for i, data in enumerate(dataset):
            if i >= self.opt.num_test:  # only apply our model to opt.num_test images.
                break
            model.set_input(data)  # unpack data from data loader
            model.test()           # run inference
            await asyncio.sleep(0.1)
            visuals = model.get_current_visuals()  # get image results
            #set_trace()
            #img_path = model.get_image_paths()     # get image paths
            #if i % 5 == 0:  # save images to an HTML file
            #    print('processing (%04d)-th image... %s' % (i, img_path))
            #save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize)
        #webpage.save()  # save the HTML
        
        im = util.tensor2im(visuals['fake'])
        await asyncio.sleep(0.1)
        util.save_image(im, self.output_path_file_name, aspect_ratio=self.opt.aspect_ratio)        
        await asyncio.sleep(0.1)

'''
opt = TestOptions()  # CREATE test options object

#set_trace()

# hard-code some parameters for test
opt.num_threads = 0   # test code only supports num_threads = 0
opt.batch_size = 1    # test code only supports batch_size = 1
opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.

# my hard-coded parameters
opt.aspect_ratio = 1.0
opt.checkpoints_dir = check_p_dir
opt.crop_size = 256
opt.dataroot = data_root_cycle_gan
opt.dataset_mode = 'single'
opt.direction = 'AtoB'
opt.epoch = 'latest'
opt.eval = True        
opt.gpu_ids = []
opt.init_gain = 0.02
opt.init_type = 'normal'
opt.input_nc = 3 
opt.isTrain = False
opt.load_iter = 0
opt.load_size = 256
opt.max_dataset_size = 100.     # ? Class<float> default = inf
opt.model = 'test'
opt.model_suffix = ''
opt.n_layers_D = 3
opt.name = 'summer2winter_yosemite.pth'
opt.ndf4 = 64
opt.netD = 'basic'
opt.netG = 'resnet_9blocks'
opt.ngf = 64                            
opt.no_dropout = True                      
opt.norm = 'instance'                      
opt.num_test = 1                            
opt.output_nc = 3                             
opt.phase = 'test'                          
opt.preprocess = 'resize_and_crop'               
opt.results_dir ='./results/'                          
opt.suffix = ''                               
opt.verbose = False 

opt.display_winsize = 256


dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
model = create_model(opt)      # create a model given opt.model and other options
model.setup(opt) 
              # regular setup: load and print networks; create schedulers
# create a website

#web_dir = os.path.join(opt.results_dir, opt.name, '{}_{}'.format(opt.phase, opt.epoch))  # define the website directory
#if opt.load_iter > 0:  # load_iter is 0 by default
#    web_dir = '{:s}_iter{:d}'.format(web_dir, opt.load_iter)
#print('creating web directory', web_dir)
#webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.epoch))

# test with eval mode. This only affects layers like batchnorm and dropout.
# For [pix2pix]: we use batchnorm and dropout in the original pix2pix. You can experiment it with and without eval() mode.
# For [CycleGAN]: It should not affect CycleGAN as CycleGAN uses instancenorm without dropout.


if opt.eval:
    model.eval()
    
for i, data in enumerate(dataset):
    if i >= opt.num_test:  # only apply our model to opt.num_test images.
        break
    model.set_input(data)  # unpack data from data loader
    model.test()           # run inference
    visuals = model.get_current_visuals()  # get image results
    #set_trace()
    #img_path = model.get_image_paths()     # get image paths
    #if i % 5 == 0:  # save images to an HTML file
    #    print('processing (%04d)-th image... %s' % (i, img_path))
    #save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize)
#webpage.save()  # save the HTML

im = util.tensor2im(visuals['fake'])
util.save_image(im, 'd:/My Documents/Обучение после аспирантуры/ML/Курс Stepik Deep learning/Проект/Bot_ver_3/images/cycle_output.jpg', aspect_ratio=opt.aspect_ratio)

#my_img_proc = Image_proc_sync(opt.display_winsize, 'cpu')
#my_img_proc.my_imsave(visuals['fake'][0,:,:,:], filename='d:/My Documents/Обучение после аспирантуры/ML/Курс Stepik Deep learning/Проект/Bot_ver_2/images/cycle_output.png')

'''
