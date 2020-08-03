from options.test_options import TestOptions
from data import DataLoader
from models import create_model
from util.writer import Writer
import numpy as np

def run_test(epoch=-1):
    print('Running Test')
    opt = TestOptions().parse()
    opt.serial_batches = True  # no shuffle
    dataset = DataLoader(opt)
    model = create_model(opt)
    writer = Writer(opt)
    # test
    writer.reset_counter()
    for i, data in enumerate(dataset):
        model.set_input(data)
        ncorrect, nexamples, out, gt = model.test()
        # Save results to obj file with color
        mesh = data['mesh']
        print(mesh[0].edges)

        f_gt = open("results/" + str(i) + "_gt.obj", "w")
        f_out = open("results/" + str(i) + "_out.obj", "w")
        # f.write("Woops! I have deleted the content!")
        f_gt.close()
        f_out.close()
        # np.savetxt('results/'+str(i)+'.txt', out, delimiter=' ')
        writer.update_counter(ncorrect, nexamples)
    writer.print_acc(epoch, writer.acc)
    return writer.acc


if __name__ == '__main__':
    run_test()
