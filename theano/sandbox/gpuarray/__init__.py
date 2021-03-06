import logging

import theano
from theano.configparser import config
from theano.compile import optdb

_logger_name = 'theano.sandbox.gpuarray'
_logger = logging.getLogger(_logger_name)
_logger.setLevel(logging.WARNING)

error = _logger.error
info = _logger.info

pygpu_activated = False
try:
    import pygpu
    import pygpu.gpuarray
except ImportError:
    pygpu = None

# This is for documentation not to depend on the availability of pygpu
from type import (GpuArrayType, GpuArrayVariable, GpuArrayConstant,
                  GpuArraySharedVariable, gpuarray_shared_constructor)
import opt


def init_dev(dev):
    global pygpu_activated
    context = pygpu.init(dev)
    pygpu.set_default_context(context)
    pygpu_activated = True

if pygpu:
    try:
        if (config.device.startswith('cuda') or
            config.device.startswith('opencl')):
            init_dev(config.device)
            import theano.compile
            theano.compile.shared_constructor(gpuarray_shared_constructor)
            optdb.add_tags('gpuarray_opt', 'fast_run', 'inplace')
        elif config.gpuarray.init_device != '':
            init_dev(config.gpuarray.init_device)
    except Exception:
        error("Could not initialize pygpu, support disabled", exc_info=True)
else:
    if (config.gpuarray.init_device != '' or
        config.device.startswith('opencl') or
        config.device.startswith('cuda')):
        error("pygpu was configured but could not be imported", exc_info=True)
