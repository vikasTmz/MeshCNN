from options.test_options import TestOptions
from data import DataLoader
from models import create_model
from util.writer import Writer
import numpy as np

def run_test(epoch=-1):
    def update_vertex_color(current_color, new_color):
        if current_color[0] < 0:
            return new_color
        else:
            return (current_color + new_color) / 2

    print('Running Test')
    opt = TestOptions().parse()
    opt.serial_batches = True  # no shuffle
    dataset = DataLoader(opt)
    model = create_model(opt)
    writer = Writer(opt)
    # test
    writer.reset_counter()
    for i, data in enumerate(dataset):
        mesh = data['mesh']
        model.set_input(data)
        ncorrect, nexamples, out, gt = model.test()
        
        # Save results to obj file with color
        gt_vcolor = np.zeros(mesh[0].vs.shape, dtype=np.float32) * -1
        out_vcolor = np.zeros(mesh[0].vs.shape, dtype=np.float32) * -1
        for i, edges in enumerate(mesh[0].edges):
            gt_vcolor[edges[0]] = update_vertex_color(gt_vcolor[edges[0]], gt[i])
            gt_vcolor[edges[1]] = update_vertex_color(gt_vcolor[edges[1]], gt[i])

            out_vcolor[edges[0]] = update_vertex_color(out_vcolor[edges[0]], out[i])
            out_vcolor[edges[1]] = update_vertex_color(out_vcolor[edges[1]], out[i])        

        gt_vcolor = np.clip(gt_vcolor, 0, 1)
        out_vcolor = np.clip(out_vcolor, 0, 1)
        # f_gt = open("results/" + str(i) + "_gt.obj", "w")
        # f_out = open("results/" + str(i) + "_out.obj", "w")

        mesh.export("results/" + str(i) + "_gt.obj", gt_vcolor)
        mesh.export("results/" + str(i) + "_out.obj", out_vcolor)
        # f_gt.close()
        # f_out.close()
        # np.savetxt('results/'+str(i)+'.txt', out, delimiter=' ')
        writer.update_counter(ncorrect, nexamples)
    writer.print_acc(epoch, writer.acc)
    return writer.acc


if __name__ == '__main__':
    run_test()
