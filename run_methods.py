import vk_friends_loader as vk_loader
import vk_freinds_json_parser as vk_parser
import migrations
import coords as pos
import unique_cities as cities

universities = {
    'narfu':'Архангельск','mgu':'Москва','tsu':'Томск',
    'hse':'Москва','svfu':'Якутия','urfu':'Екатеринбург'
}

for university, city in universities.items():
    print('current university',university)
    #vk_loader.get_freinds(university)
    print('friends loaded')
    #vk_parser.parse_json_files(university)
    print('friends parsed')
    #migrations.get_migrations(university, city, 0)
    print('positions loaded')
    #pos.get_coords(university)

#cities.get_cities([*universities])