import matplotlib.pyplot as plt
import tensorflow as tf
import time
import numpy as np

from IPython import display as ipythondisplay
from string import Formatter

# This should be made conditional for Intel Dev Cloud, already defined in Google Colab
# Also... does not work.  Add to kernel?
from IPython.core.magic import (register_line_magic)

@register_line_magic
def tensorflow_version(line):
    "tensorflow_version"
    return line

# In an interactive session, we need to delete it after registration to avoid
# name conflicts for automagic to work on line magics.
del tensorflow_version

def display_model(model):
  tf.keras.utils.plot_model(model,
             to_file='tmp.png',
             show_shapes=True)
  return ipythondisplay.Image('tmp.png')


def plot_sample(x,y,vae):
    plt.figure(figsize=(2,1))
    plt.subplot(1, 2, 1)

    idx = np.where(y==1)[0][0]
    plt.imshow(x[idx])
    plt.grid(False)

    plt.subplot(1, 2, 2)
    _, _, _, recon = vae(x)
    recon = np.clip(recon, 0, 1)
    plt.imshow(recon[idx])
    plt.grid(False)

    plt.show()



class LossHistory:
  def __init__(self, smoothing_factor=0.0):
    self.alpha = smoothing_factor
    self.loss = []
  def append(self, value):
    self.loss.append( self.alpha*self.loss[-1] + (1-self.alpha)*value if len(self.loss)>0 else value )
  def get(self):
    return self.loss

class PeriodicPlotter:
  def __init__(self, sec, xlabel='', ylabel='', scale=None):

    self.xlabel = xlabel
    self.ylabel = ylabel
    self.sec = sec
    self.scale = scale

    self.tic = time.time()

  def plot(self, data):
    if time.time() - self.tic > self.sec:
      plt.cla()

      if self.scale is None:
        plt.plot(data)
      elif self.scale == 'semilogx':
        plt.semilogx(data)
      elif self.scale == 'semilogy':
        plt.semilogy(data)
      elif self.scale == 'loglog':
        plt.loglog(data)
      else:
        raise ValueError("unrecognized parameter scale {}".format(self.scale))

      plt.xlabel(self.xlabel); plt.ylabel(self.ylabel)
      ipythondisplay.clear_output(wait=True)
      ipythondisplay.display(plt.gcf())

      self.tic = time.time()


def create_grid_of_images(xs, size=(5,5)):
    """ Combine a list of images into a single image grid by stacking them into an array of shape `size` """

    grid = []
    counter = 0
    for i in range(size[0]):
        row = []
        for j in range(size[1]):
          row.append(xs[counter])
          counter += 1
        row = np.hstack(row)
        grid.append(row)
    grid = np.vstack(grid)
    return grid
