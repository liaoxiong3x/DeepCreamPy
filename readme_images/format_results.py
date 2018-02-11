from PIL import Image
import matplotlib.pyplot as plt

def format_results(images, dst):
    fig = plt.figure()
    for i, image in enumerate(images):
        text, img = image
        fig.add_subplot(1, 3, i + 1)
        plt.imshow(img)
        plt.tick_params(labelbottom='off')
        plt.tick_params(labelleft='off')
        plt.gca().get_xaxis().set_ticks_position('none')
        plt.gca().get_yaxis().set_ticks_position('none')
        plt.xlabel(text)
    plt.savefig(dst)
    plt.close()

if __name__ == "__main__":
    masked = Image.open("censored.png")
    img = Image.open("decensored.png")
    raw = Image.open("original.png")
    format_results([['Input', masked], ['Output', img], ['Ground Truth', raw]], "result.png")