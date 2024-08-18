import matplotlib.pyplot as plt


def read_colors_from_file(filename):
    colors = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('Hex:'):
                hex_color = line.split(',')[0].split(': ')[1].strip()
                colors.append(hex_color)
    return colors


def plot_color_distribution(colors):
    color_counts = {color: colors.count(color) for color in colors}
    labels = color_counts.keys()
    sizes = color_counts.values()

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=labels)
    ax.axis('equal')

    plt.title('Color Distribution')
    plt.show()


def visualize():
    colors = read_colors_from_file('C:/Users/HarshitaaMS/Downloads/automation-project1/automation-project/scraped/www.flipkart.com/colour_codes.txt')
    plot_color_distribution(colors)


