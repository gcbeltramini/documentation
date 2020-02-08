# Docopt

## Python

Reference: <https://github.com/docopt/docopt>

1. Setup (assuming you have [Anaconda](https://www.anaconda.com/distribution/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)):

    ```bash
    conda create -yn docopt python=3.7 'docopt>=0.6.2,<0.7'
    conda activate docopt
    python -m pip install 'schema>=0.7,<1'
    ```

1. Run: `./my_command.py ...`

1. Finish: `conda deactivate`
