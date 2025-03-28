from DatasetUtilities.AIScraper.OpenAI import get_plant_info

x = ["Aloe vera", "Ficus lyrata"]

def search_plants(plants_list, output_file = "plant_care_info.txt"):
    write_opening_json(output_file)
    for plant in plants_list:
        info = get_plant_info(plant)
        flower_info = str(info)
        save_to_file(flower_info, output_file)
    write_closing_json(output_file)


def save_to_file(data, filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write(data)
        file.write(",\n")

def write_opening_json(filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write('{\n   "plants":[\n')

def write_closing_json(filename):
    with open(filename, "a", encoding='utf-8') as file:
        file.write('\n   ]\n}')

search_plants(x)

