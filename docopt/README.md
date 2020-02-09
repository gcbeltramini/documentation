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

1. Clean up (if installed temporarily):

    ```bash
    conda deactivate
    conda env remove -n docopt-env
    ```

## Shell

Reference: <https://github.com/docopt/docopts>

1. Setup:
    1. Download the pre-built Go binaries from the [releases page](https://github.com/docopt/docopts/releases).
    In the assets list, choose the file for your operating system. Suggested version: `v0.6.3-rc1`.
    1. Choose an installation folder:
      * If it's temporary: `INSTALLATION_FOLDER="$(pwd)" && export PATH="${INSTALLATION_FOLDER}:${PATH}"`
      * If it's permanent: `INSTALLATION_FOLDER="/usr/local/bin"`
    1. In macOS Catalina:

      ```bash
      mv "${HOME}/Downloads/docopts_darwin_amd64" "${INSTALLATION_FOLDER}/docopts"
      chmod +x "${INSTALLATION_FOLDER}/docopts"
      xattr -d com.apple.quarantine "${INSTALLATION_FOLDER}/docopts"
      ```

    1. Optionally, download the `docopts.sh` lib helper:

      ```bash
      URL="https://raw.githubusercontent.com/docopt/docopts/master/docopts.sh"
      (cd "${INSTALLATION_FOLDER}" && curl -O "${URL}")
      ```

    If you `source docopts.sh`, these functions are enabled:
        - `docopt_auto_parse`
        - `docopt_get_help_string`
        - `docopt_get_version_string`
        - `docopt_get_values`
        - `docopt_get_eval_array`
        - `docopt_get_raw_value`
        - `docopt_print_ARGS`

1. Run: `./my_command.sh ...`

1. Clean up (if installed temporarily):

    ```bash
    rm "${INSTALLATION_FOLDER}/docopts"
    "${INSTALLATION_FOLDER}/docopts.sh"
    ```
