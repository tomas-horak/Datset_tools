
"""
import scipy.io

mat = scipy.io.loadmat('./imagelabels.mat')
labels = mat["labels"][0]

flowers = [
    'pink primrose',
    'hard-leaved pocket orchid',
    'canterbury bells',
    'sweet pea',
    'english marigold',
    'tiger lily',
    'moon orchid',
    'bird of paradise',
    'monkshood',
    'globe thistle',
    'snapdragon',
    "colt's foot",
    'king protea',
    'spear thistle',
    'yellow iris',
    'globe-flower',
    'purple coneflower',
    'peruvian lily',
    'balloon flower',
    'giant white arum lily',
    'fire lily',
    'pincushion flower',
    'fritillary',
    'red ginger',
    'grape hyacinth',
    'corn poppy',
    'prince of wales feathers',
    'stemless gentian',
    'artichoke',
    'sweet william',
    'carnation',
    'garden phlox',
    'love in the mist',
    'mexican aster',
    'alpine sea holly',
    'ruby-lipped cattleya',
    'cape flower',
    'great masterwort',
    'siam tulip',
    'lenten rose',
    'barbeton daisy',
    'daffodil',
    'sword lily',
    'poinsettia',
    'bolero deep blue',
    'wallflower',
    'marigold',
    'buttercup',
    'oxeye daisy',
    'common dandelion',
    'petunia',
    'wild pansy',
    'primula',
    'sunflower',
    'pelargonium',
    'bishop of llandaff',
    'gaura',
    'geranium',
    'orange dahlia',
    'pink-yellow dahlia?',
    'cautleya spicata',
    'japanese anemone',
    'black-eyed susan',
    'silverbush',
    'californian poppy',
    'osteospermum',
    'spring crocus',
    'bearded iris',
    'windflower',
    'tree poppy',
    'gazania',
    'azalea',
    'water lily',
    'rose',
    'thorn apple',
    'morning glory',
    'passion flower',
    'lotus',
    'toad lily',
    'anthurium',
    'frangipani',
    'clematis',
    'hibiscus',
    'columbine',
    'desert-rose',
    'tree mallow',
    'magnolia',
    'cyclamen ',
    'watercress',
    'canna lily',
    'hippeastrum ',
    'bee balm',
    'ball moss',
    'foxglove',
    'bougainvillea',
    'camellia',
    'mallow',
    'mexican petunia',
    'bromelia',
    'blanket flower',
    'trumpet creeper',
    'blackberry lily',
]


os.makedirs(output_folder, exist_ok=True)
for index, label in enumerate(labels):
    class_folder = os.path.join(output_folder, flowers[label - 1])
    os.makedirs(class_folder, exist_ok=True)


# Seřadíme soubory ve složce abecedně
jpg_files = sorted(os.listdir("./jpg"))



for index, label in enumerate(labels):
    img = jpg_files[index]
    source_path = os.path.join("./jpg", img)
    destination_path = os.path.join(output_folder, flowers[label - 1])
    shutil.copy(source_path, destination_path)
    print(index, label, flowers[label - 1])


# Distribuce labelů - počty jednotlivých labelů
label_counts = Counter(labels)

# Vytvoříme DataFrame pro distribuci
class_distribution = {flower: label_counts.get(i + 1, 0) for i, flower in enumerate(flowers)}
df = pd.DataFrame(list(class_distribution.items()), columns=['Class', 'Number of Samples'])

# Zobrazíme DataFrame
print(df)

# Vytvoření bar grafu pro distribuci tříd
plt.figure(figsize=(12, 6))
df.plot(x='Class', y='Number of Samples', kind='bar', legend=False)
plt.title("Class Distribution of Oxford 102 Dataset")
plt.xlabel("Class", fontsize=12)
plt.ylabel("Number of Samples", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=7)
plt.tight_layout()
plt.show()
plants = [
    'Philodendron', 'Devil\'s ivy', 'Bambusoideae', 'Echeveria', 'Dracaena',
    'Fern', 'Jade plant', 'Dumb canes', 'Hoya', 'Alocasia',
    'adenium', 'adiantum', 'aglaonema', 'aloe-vera', 'amaryllis', 'anthurium',
    'araucaria-heterophylla', 'bambusa', 'begonia', 'begonia-rex', 'boston-fern',
    'chlorophytum-comosum', 'crassula-ovata', 'croton', 'curio-rowleyanus', 'dieffenbachia',
    'dracaena-trifasciata', 'epipremnum', 'euphorbiamilii', 'fatsia-japonica', 'ficus-benjamina',
    'ficus-elastica', 'fiddle-leaf', 'haworthiopsis-attenuata', 'hedera-helix', 'hypoestes-phyllostachya',
    'kalanchoe', 'mesembryanthemum-cordifolium', 'monstera-deliciosa', 'opuntia-microdasys', 'pachira',
    'pachypodium-lamerei', 'pedilanthus', 'pelargonium-graveolens', 'pelargonium-hortorum',
    'pelargonium-x-domesticum', 'peperomia-caperata', 'phalaenopsis', 'pilea-peperomioides', 'poinsettia',
    'ponytail-palm', 'schefflera', 'spathiphyllum', 'syngonium', 'thaumatophyllum-bipinnatifidum',
    'tradescantia-fluminensis', 'verbena', 'zamioculcas'
]

os.makedirs(output_folder, exist_ok=True)

for plant in plants:
    class_folder = os.path.join(output_folder, plant.strip())
    os.makedirs(class_folder, exist_ok=True)

"""