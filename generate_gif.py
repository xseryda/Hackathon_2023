import os

import imageio

images = []

for filename in sorted(os.listdir('pictures')):
    print(filename)
    images.append(imageio.v2.imread(f'pictures/{filename}'))
imageio.mimsave('mowing.gif', images)
