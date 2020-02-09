# Docopt

## Python

Reference: <https://github.com/docopt/docopt>

1. Setup (assuming you have [Anaconda](https://www.anaconda.com/distribution/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)):

    ```bash
    conda create -yn docopt-env python=3.7 'docopt>=0.6.2,<0.7'
    conda activate docopt-env
    python -m pip install 'schema>=0.7,<1'
    ```

    If you want to have `docopt` permanently installed, install it in the base Python environment.

1. Run: `./my_command.py ...`

1. Clean up:

    ```bash
    conda deactivate
    conda env remove -n docopt-env
    ```
