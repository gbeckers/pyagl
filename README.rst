pyagl
=====

A python library for statistical and artificial grammar learning (AGL)
analyses.

This software is used for our own research, but is freely available to
others for use or contributions.

We are at an incipient stage where just one model for word segmentation
(PARSER) is implemented, as well as more general string analysis functions.

Pyagl has its roots in, and will supersede, two related earlier projects:
`aglcheck <https://github.com/gjlbeckers-uu/aglcheck>`__ by Gabriël Beckers.
The PARSER module was initiated by Bror-E, in `PARSER-for-Python
<https://github.com/Bror-E/PARSER-for-Python>`__, but has since then evolved
to a large extent.

Pyagl is currently pre-1.0, still undergoing significant development. It is
open source and freely available under the
`New BSD License <https://opensource.org/licenses/BSD-3-Clause>`__ terms.


Installation
------------

As long as there is no official release I recommend working in Anaconda.

Create an environment::

    $ conda create -n agltest pip python=3.6 jupyterlab git pyaml pandas

Switch to this new environment:

Linux and MacOS::

    $ source activate agltest

Windows::

    $ conda activate agltest

Install the pyagl master repo::

    $ pip install git+https://git.science.uu.nl/G.J.L.Beckers//pyagl@master


If you want to remove the conda environment later::

    $ conda env remove -n agltest


Documentation
-------------

Not there yet.


pyagl is BSD licensed (BSD 3-Clause License). (c) 2019-2020, Gabriël Beckers.
