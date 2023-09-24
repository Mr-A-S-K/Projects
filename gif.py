import imageio as io
Photos = ['ex1.jpg', 'ex2.jpg', 'ex3.jpg']
save = []
for photo in Photos:
    save.append(io.imread(photo))
io.mimsave('im.gif', save, duration=2000)