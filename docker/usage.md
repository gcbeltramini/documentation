
# Definitions

- Docker container: runtime instance of a docker image. It consists of:
    - A Docker image
    - An execution environment
    - A standard set of instructions
- Image: basis of containers. An Image is an ordered collection of root filesystem changes and the corresponding execution parameters for use within a container runtime. An image typically contains a union of layered filesystems stacked on top of each other. An image does not have state and it never changes.
- Dockerfile: text document that contains all the commands a user could call on the command line to assemble an image.

# Repository

- Search the Docker Hub for images:
    ```shell
    $ docker search <name>
    ```
- Pull image from Docker Hub:
    ```shell
    $ docker pull <name>:<tag> # if no tag is given, it assumes `latest`
    $ docker pull ubuntu:16.04
    ```
    (the Ubuntu images and tags are here: https://hub.docker.com/_/ubuntu/)
- Log in to a Docker registry:
    ```shell
    $ docker login -u <docker-registry-username>
    ```
- Push an image or a repository to a registry:
    ```shell
    $ docker push <docker-registry-username>/<image-name>[:tag]
    ```

# Images

- Build an image from a `Dockerfile`:
    ```shell
    $ docker build --tag <image-name> </path/to/context>
    $ docker build --tag <image-name> --file </path/to/Dockerfile> </path/to/context>
    ```
    - Use `.dockerignore` to exclude files and directories from the context
- List images:
    ```shell
    $ docker images
    ```
- Remove images:
    ```shell
    $ docker rmi <image-name>
    ```

# Containers

- Create new container using an image, start it and:
    - run command
    ```shell
    $ docker run <image-name> [<command>]
    $ docker run <image-name> echo "foo"
    ```
    - enter the bash shell (`-i, --interactive` to keep STDIN open even if not attached, and `-t, --tty` to allocate a pseudo-TTY):
    ```shell
    $ docker run -it <image-name> /bin/bash
    ```
    - edit options:
        - Map port `<host-port>` on the host to `<container-port>` on the container, with `-p, --publish`: `-p <host-port>:<container-port>`
        - Bind mount a volume, with `-v, --volume`: `-v <local/path>:<container/destination/path>`
        - Run container in background and print container ID, with `-d, --detach`
        - Overwrite the default `ENTRYPOINT` of the image, with `--entrypoint`: `--entrypoint=/bin/bash`

- Run a command in a running container:
    ```shell
    $ docker exec <container-id> <command>
    $ docker exec -it <container-id> /bin/bash
    ```
- Exit and stop the container, when inside the container:
    ```shell
    # exit
    ```
 - Stop the container:
    ```shell
    $ docker stop <container-id>
    ```
- List all containers (running and stopped):
    ```shell
    $ docker ps -a
    ```
- Start stopped container:
    ```shell
    $ docker start <container-id>
    ```
    (you can't start containers that have exit codes greater than 0)
- Attach local standard input, output, and error streams to a running container:
    ```shell
    $ docker attach <container-id>
    ```
- Remove containers:
    ```shell
    $ docker rm <container-id> [<container-id>...]
    ```
- Copy files/folders between a container and the local filesystem:
    ```shell
    $ docker cp <container-id>:<src/path> <local/destination/path/>
    $ docker cp <local/src/path> <container-id>:<destination/path/>
    ```
- Create a new image from a container's changes:
    ```shell
    $ docker commit -m "What did you do to the image" -a "Author Name" <container-id> <repository>/<new_image_name>
    ```

# Management

- Show docker disk usage (images, containers, local volumes, build cache):
    ```shell
    $ docker system df
    ```
- Remove unused data:
    ```shell
    $ docker system prune
    $ docker system prune --all  # remove also all images without at least one container associated to them
    ```

# Tips and tricks
- Every time you pass a container ID as argument, it can be the shortest number of characters in the beginning of the ID that unambiguously identifies it.
    - Usually the first 3 characters are enough
    - An alternative is to pass the container name

# References
1. https://docs.docker.com/glossary/?term=container
1. https://docs.docker.com/glossary/?term=image
1. https://docs.docker.com/glossary/?term=dockerfile
1. https://docs.docker.com/edge/engine/reference/commandline/docker/
