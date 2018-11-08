from pandas import read_csv
from matplotlib import pyplot
import sys
import os

def plot(file_path):
    # load dataset
    df = read_csv(file_path, header=0, index_col=None)

    ## plot data per person
    window = range(0, df.shape[0]) #df.shape[0]

    pyplot.subplot(2,2,1)
    
    g1_x = df.values[window, 0]
    pyplot.plot(window, g1_x, color='red')

    g1_y = df.values[window, 1]
    pyplot.plot(window, g1_y, color='green')

    g1_z = df.values[window, 2]
    pyplot.plot(window, g1_z, color='blue')
    pyplot.title('g1')

    pyplot.subplot(2,2,2)
    
    acc1_x = df.values[window, 3]
    pyplot.plot(window, acc1_x, color='red')

    acc1_y = df.values[window, 4]
    pyplot.plot(window, acc1_y, color='green')

    acc1_z = df.values[window, 5]
    pyplot.plot(window, acc1_z, color='blue')
    pyplot.title('acc1')

    pyplot.subplot(2,2,3)

    g2_x = df.values[window, 6]
    pyplot.plot(window, g2_x, color='red')

    g2_y = df.values[window, 7]
    pyplot.plot(window, g2_y, color='green')

    g2_z = df.values[window, 8]
    pyplot.plot(window, g2_z, color='blue')
    pyplot.title('g2')
    
    pyplot.subplot(2,2,4)
    
    acc2_x = df.values[window, 9]
    pyplot.plot(window, acc2_x, color='red')

    acc2_y = df.values[window, 10]
    pyplot.plot(window, acc2_y, color='green')

    acc2_z = df.values[window, 11]
    pyplot.plot(window, acc2_z, color='blue')
    pyplot.title('acc2')
    
if __name__ == '__main__':    

    if len(sys.argv) != 2:
        print('usage: python3 ' + sys.argv[0] + ' <relative_path_to_csv_dir>') 
        sys.exit()

    #data_dir = os.path.join(os.getcwd(), 'Training', 'RNN', 'raw_data')
    data_dir = sys.argv[1]
    
    filenames = next(os.walk(data_dir))[2] ## get file (not dir) names only

    list_of_moves = {}

    for filename in filenames:

        move = filename.split("_")[0]

        if move not in list_of_moves:
            list_of_moves[move] = list()
            list_of_moves[move].append(filename)
        else:
            list_of_moves[move].append(filename)

    print(list_of_moves)
            
    for move in list_of_moves:
        for person_file in list_of_moves[move]:
            print(person_file)
            fig = pyplot.figure()
            fig.suptitle(person_file)
            file_path =  os.path.join(data_dir, person_file)
            plot(file_path)

        pyplot.show()
