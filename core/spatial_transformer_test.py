import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from rare.core import spatial_transformer


class SpatialTransformerTest(tf.test.TestCase):
  
  def test_transform(self):
    transformer = spatial_transformer.SpatialTransformer(
      output_size=(32, 100),
      num_control_points=6,
      margin=0.05
    )
    test_input_ctrl_pts = np.array([
      [0.1, 0.4], [0.5, 0.1], [0.9, 0.4],
      [0.1, 0.9], [0.5, 0.6], [0.9, 0.9]
    ], dtype=np.float32)
    test_im = Image.open('rare/data/test_image.jpg').resize((100, 32))
    test_image_array = np.array(test_im)
    test_image = tf.constant(test_image_array)

    sampling_grid = transformer._generate_grid(test_input_ctrl_pts)
    rectified_image = transformer._sample(test_image, sampling_grid)

    with self.test_session() as sess:
      outputs = sess.run({
        'sampling_grid': sampling_grid,
        'rectified_image': rectified_image
      })

    output_grid = transformer._output_grid.reshape([-1, 2])
    output_ctrl_pts = transformer._output_ctrl_pts

    # visualize

    plt.figure()
    plt.subplot(1,2,1)
    plt.scatter(test_input_ctrl_pts[:,0], test_input_ctrl_pts[:,1])
    plt.subplot(1,2,2)
    plt.scatter(output_ctrl_pts[:,0], output_ctrl_pts[:,1])

    plt.figure()
    plt.subplot(1,2,1)
    plt.scatter(outputs['sampling_grid'][:,0], outputs['sampling_grid'][:,1])
    plt.subplot(1,2,2)
    plt.scatter(output_grid[:,0], output_grid[:,1])

    plt.figure()
    plt.subplot(2,1,1)
    plt.imshow(test_image_array)
    plt.subplot(2,1,2)
    plt.imshow(outputs['rectified_image'])
    plt.show()


if __name__ == '__main__':
  tf.test.main()
