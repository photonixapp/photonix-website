# Building Tensorflow

Tensorflow is the Machine Learning library we use for our more complex image analysis features. It allows us to create algorithms to do things like detecting and recognising objects in a photo or identifying a style.

- Python integration
- Pre-built packages
- Device compatibility
- Build tools - Bazel, Docker
- Raspberry Pi
- Common problems
  - Pip package versions
  - OOM
    - Progress shown (e.g. [15,686 / 23,361]) - if you run again and it fails at a different stage then it's probably OOM
Execution platform: @local_execution_config_platform//:platform
In file included from /usr/include/python2.7/Python.h:8:0,
                 from ./tensorflow/python/lib/core/numpy.h:35,
                 from tensorflow/python/lib/core/numpy.cc:20:
/usr/include/python2.7/pyconfig.h:24:54: fatal error: arm-linux-gnueabihf/python2.7/pyconfig.h: No such file or directory
 #  include <arm-linux-gnueabihf/python2.7/pyconfig.h>
