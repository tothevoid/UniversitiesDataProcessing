import vk_friends_loader as vk_loader
import vk_freinds_json_parser as vk_parser
import transorm_to_datasets as data_transoformer

university = 'narfu'

vk_loader.get_freinds(university)
vk_parser.parse_json_files(university)
data_transoformer.transform(university, True)