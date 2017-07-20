import matplotlib.pyplot as plt

def generate_triangle(inten_array):
        #take a flat line (array of all zeros) and make a triangle in the middle of it
        for i in range(len(inten_array)):
                if 200 >= i >= 100:
                        inten_array[i] = i-100
                elif 300 >= i > 200:
                        inten_array[i] = 300 - i
        return inten_array






triangle_inten = generate_triangle([0]*400)
print(triangle_inten)

plt.plot(triangle_inten)
plt.show()
