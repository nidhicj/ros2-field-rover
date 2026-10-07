
import os
import yaml

CONFIG_PATH = os.environ.get(
    'CRAWLER_SW_PROFILE',
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'sw_profile.yml'),
)

class LoadConfig():
    def __init__(self):
        pass
    def load_config(self,mode):
        with open(CONFIG_PATH, 'r') as file:
            self.config = yaml.safe_load(file)
            offset_fl = self.config[mode]['fl_sw']['servo']
            offset_fr = self.config[mode]['fr_sw']['servo']
            offset_bl = self.config[mode]['bl_sw']['servo']
            offset_br = self.config[mode]['br_sw']['servo']


            print(f'self.crawler_mode : {offset_fl}')
            print(f'self.crawler_mode : {offset_fr}')
            print(f'self.crawler_mode : {offset_bl}')
            print(f'self.crawler_mode : {offset_br}')
            
            return offset_fl,offset_fr,offset_bl,offset_br