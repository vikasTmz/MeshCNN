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

    # colormap
    colormap = {1:[1,0,0],2:[0,1,0],3:[0,0,1], 0:[0,0,0],4:[0,0,0]}
    # test
    writer.reset_counter()
    for j, data in enumerate(dataset):
        mesh = data['mesh']
        model.set_input(data)
        ncorrect, nexamples, out, gt = model.test()
        
        # # Save results to obj file with color
        gt_vcolor = np.zeros(mesh[0].vs.shape, dtype=np.float32) * -1
        out_vcolor = np.zeros(mesh[0].vs.shape, dtype=np.float32) * -1
        print(len(mesh[0].edges), mesh[0].faces.shape)

        for i, edges in enumerate(mesh[0].edges):
            gt_vcolor[edges[0]] = update_vertex_color(gt_vcolor[edges[0]], colormap[int(gt[i])])
            gt_vcolor[edges[1]] = update_vertex_color(gt_vcolor[edges[1]], colormap[int(gt[i])])

            out_vcolor[edges[0]] = update_vertex_color(out_vcolor[edges[0]], colormap[int(out[i])])
            out_vcolor[edges[1]] = update_vertex_color(out_vcolor[edges[1]], colormap[int(out[i])])        

        # gt_vcolor = np.clip(gt_vcolor, 0, 1)
        # out_vcolor = np.clip(out_vcolor, 0, 1)

        mesh[0].export("results/" + str(j) + "_gt.obj", gt_vcolor)
        mesh[0].export("results/" + str(j) + "_out.obj", out_vcolor)

        writer.update_counter(ncorrect, nexamples)
    writer.print_acc(epoch, writer.acc)
    return writer.acc


if __name__ == '__main__':
    run_test()
