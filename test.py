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
    model_r = create_model(opt)
    model_g = create_model(opt)
    model_b = create_model(opt)
    writer = Writer(opt)

    # colormap
    # colormap = {1:[1,0,0],2:[0,1,0],3:[0,0,1], 0:[0,0,0],4:[0,0,0]}
    # test
    writer.reset_counter()
    for j, data in enumerate(dataset):
        mesh = data['mesh']
        model_r.set_input(data,0)
        model_g.set_input(data,1)
        model_b.set_input(data,2)
        ncorrect, nexamples, out_r, gt_r = model_r.test()
        ncorrect, nexamples, out_g, gt_g = model_g.test()
        ncorrect, nexamples, out_b, gt_b = model_b.test()
        
        # # Save results to obj file with color
        gt_vcolor = np.zeros(mesh[0].vs.shape, dtype=np.float32) * -1
        out_vcolor = np.zeros(mesh[0].vs.shape, dtype=np.float32) * -1

        for i, edges in enumerate(mesh[0].org_edges):
            gt_vcolor[edges[0]] = update_vertex_color(gt_vcolor[edges[0]], [gt_r[i], gt_g[i], gt_b[i]])
            gt_vcolor[edges[1]] = update_vertex_color(gt_vcolor[edges[1]], [gt_r[i], gt_g[i], gt_b[i]])

            out_vcolor[edges[0]] = update_vertex_color(out_vcolor[edges[0]], [out_r[i], out_g[i], out_b[i]])
            out_vcolor[edges[1]] = update_vertex_color(out_vcolor[edges[1]], [out_r[i], out_g[i], out_b[i]])        

        gt_vcolor = np.clip(gt_vcolor, 0, 1)
        out_vcolor = np.clip(out_vcolor, 0, 1)

        mesh[0].export("results/" + str(j) + "_gt.obj", gt_vcolor)
        mesh[0].export("results/" + str(j) + "_out.obj", out_vcolor)

        writer.update_counter(ncorrect, nexamples)
    writer.print_acc(epoch, writer.acc)
    return writer.acc


if __name__ == '__main__':
    run_test()
