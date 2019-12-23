# Get Docker CE for Ubuntu

For more information and alternative installation (download the DEB package and install it manually,
or use testing environment), consult the reference.

1. Uninstall old versions

    ```shell
    sudo apt-get remove docker docker-engine docker.io
    ```

1. Update the `apt` package index:

    ```shell
    sudo apt-get update
    ```

1. Install packages to allow `apt` to use a repository over HTTPS:

    ```shell
    sudo apt-get install \
      apt-transport-https \
      ca-certificates \
      curl \
      software-properties-common
    ```

1. Add Docker’s official GPG key:

    ```shell
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```

    Verify that you now have the key with the fingerprint
    `9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88`:

    ```shell
    sudo apt-key fingerprint 0EBFCD88
    ```

1. Set up the stable repository:

    ```shell
    sudo add-apt-repository \
      "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) \
      stable"
    ```

1. Update the `apt` package index:

    ```shell
    sudo apt-get update
    ```

1. Install the latest version of Docker CE:

    ```shell
    sudo apt-get install docker-ce
    ```

    For a specific version (recommended for production systems):

    - List the available versions

        ```shell
        apt-cache madison docker-ce
        ```

    - Choose a version and install it:

        ```shell
        sudo apt-get install docker-ce=<VERSION>
        ```

1. Verify that Docker CE is installed correctly by running the hello-world image.

    ```shell
    sudo docker run hello-world
    ```

    Docker CE is installed and running.

1. You need to use `sudo` to run Docker commands. Allow non-privileged users to run Docker commands:
    1. Create the `docker` group:

        ```shell
        sudo groupadd docker
        ```

    1. Add your user to the `docker` group:

        ```shell
        sudo usermod -aG docker $USER
        ```

    1. Log out and log back in so that your group membership is re-evaluated.
    1. Verify that you can run docker commands without `sudo`.

        ```shell
        docker run hello-world
        ```

1. Consult <https://docs.docker.com/install/linux/linux-postinstall/> for other optional
configuration steps, such as:

- Configure Docker to start on boot
- Use a different storage engine
- Configure where the Docker daemon listens for connections
- Enable IPv6 on the Docker daemon
- Troubleshooting

## Files and directories used by Docker

- `/var/lib/docker/`: images, containers, volumes, or customized configuration files on your host
- `~/.docker/`: custom settings
- `/etc/docker/daemon.json`: `hosts` array

## Reference

1. <https://docs.docker.com/install/linux/docker-ce/ubuntu/>
