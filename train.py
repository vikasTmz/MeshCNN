import time
from options.train_options import TrainOptions
from data import DataLoader
from models import create_model
from util.writer import Writer
from test import run_test

if __name__ == '__main__':
    opt = TrainOptions().parse()
    dataset = DataLoader(opt)
    dataset_size = len(dataset)
    print('#training meshes = %d' % dataset_size)

    model_r = create_model(opt)
    # model_g = create_model(opt)
    # model_b = create_model(opt)
    writer = Writer(opt)
    total_steps = 0

    for epoch in range(opt.epoch_count, opt.niter + opt.niter_decay + 1):
        epoch_start_time = time.time()
        iter_data_time = time.time()
        epoch_iter = 0

        for i, data in enumerate(dataset):
            iter_start_time = time.time()
            if total_steps % opt.print_freq == 0:
                t_data = iter_start_time - iter_data_time
            total_steps += opt.batch_size
            epoch_iter += opt.batch_size

            model_r.set_input(data,0)
            # model_g.set_input(data,1)
            # model_b.set_input(data,2)

            model_r.optimize_parameters()
            # model_g.optimize_parameters()
            # model_b.optimize_parameters()


            if total_steps % opt.print_freq == 0:
                loss = model_r.loss
                t = (time.time() - iter_start_time) / opt.batch_size
                writer.print_current_losses(epoch, epoch_iter, loss, t, t_data)
                writer.plot_loss(loss, epoch, epoch_iter, dataset_size)

            if i % opt.save_latest_freq == 0:
                print('saving the latest model (epoch %d, total_steps %d)' %
                      (epoch, total_steps))
                model_r.save_network('latest')

            iter_data_time = time.time()
        if epoch % opt.save_epoch_freq == 0:
            print('saving the model at the end of epoch %d, iters %d' %
                  (epoch, total_steps))
            model_r.save_network('latest')
            model_r.save_network(epoch)

        print('End of epoch %d / %d \t Time Taken: %d sec' %
              (epoch, opt.niter + opt.niter_decay, time.time() - epoch_start_time))
        model_r.update_learning_rate()
        # model_g.update_learning_rate()
        # model_b.update_learning_rate()
        if opt.verbose_plot:
            writer.plot_model_wts(model, epoch)

        if epoch % opt.run_test_freq == 0:
            acc = run_test(epoch)
            writer.plot_acc(acc, epoch)

    writer.close()
