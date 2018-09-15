import vk_friends_loader as vk_loader
import vk_freinds_json_parser as vk_parser

universities = ['narfu','tsu','mgu']

for university in universities:
    vk_loader.get_freinds(university)
    print('friends loaded')
    vk_parser.parse_json_files(university)
    print('friends parsed')