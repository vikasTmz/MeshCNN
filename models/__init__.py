def create_model(opt):
	if opt.dataset_mode == 'segmentation' or opt.dataset_mode == 'classification':
	    from .mesh_classifier import ClassifierModel # todo - get rid of this ?
	    model = ClassifierModel(opt)
	elif opt.dataset_mode == 'texturize':
		from .mesh_texturize import TexturizeModel
		model = TexturizeModel(opt)
    return model
