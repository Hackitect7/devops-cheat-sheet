# 🐳 Docker Cheat Sheet

> 📘 Docker is a platform for running applications in isolated containers. This cheat sheet contains commands for working with images, containers, networks, volumes, as well as Docker Compose and Swarm.

---

## 📂 Contents

- [🐳 Docker Cheat Sheet](#-docker-cheat-sheet)
  - [📂 Contents](#-contents)
  - [📦 Basic Commands](#-basic-commands)
  - [🔁 Container Management](#-container-management)
  - [🧱 Images and Dockerfile](#-images-and-dockerfile)
  - [🔌 Networks and Volumes](#-networks-and-volumes)
  - [🧩 Docker Plugins](#-docker-plugins)
  - [📋 Docker Compose](#-docker-compose)
  - [📤 Export and Import](#-export-and-import)
  - [🧹 Cleanup and Diagnostics](#-cleanup-and-diagnostics)
  - [🐝 Docker Swarm](#-docker-swarm)
  - [💼 Advanced Docker Usage](#-advanced-docker-usage)
    - [🚀 Professional Docker Commands](#-professional-docker-commands)
    - [🛠 Useful Docker Practices and Automation](#-useful-docker-practices-and-automation)
    - [🐞 Debugging and Profiling Docker Containers](#-debugging-and-profiling-docker-containers)
  - [💼 Advanced Docker Compose Usage](#-advanced-docker-compose-usage)
    - [🚀 Professional Docker Compose Commands](#-professional-docker-compose-commands)
    - [🛠 Useful Practices and Automation with Docker Compose](#-useful-practices-and-automation-with-docker-compose)
    - [🐞 Debugging and Profiling Services in Docker Compose](#-debugging-and-profiling-services-in-docker-compose)
  - [Additional Resources](#additional-resources)
    - [🚫 Ignoring Files with `.dockerignore`](#-ignoring-files-with-dockerignore)
    - [⚡ Simplifying Commands with Aliases](#-simplifying-commands-with-aliases)
    - [🧠 Tip: Docker Usage Advice](#-tip-docker-usage-advice)
    - [🌐 Useful Links](#-useful-links)

---

## 📦 Basic Commands

| Command | Example | Description |
| ------- | ------- | ----------- |
| [**`docker`**](https://docs.docker.com/reference/cli/docker/) | | **The main Docker CLI command used to run subcommands and manage containers, images, networks, and volumes** |
| [**`docker version`**](https://docs.docker.com/reference/cli/docker/version/) | | **Display the installed Docker version (client and server). Useful for installation verification** |
|         | `docker version --format '{{.Client.APIVersion}}'` | Show only the Docker client API version |
|         | `docker version --format '{{.Server.Version}}'` | Show only the Docker server (Engine) version |
|         | `docker version --format '{{json .}}'` | Output full version info in JSON format |
| [**`docker system info`**](https://docs.docker.com/engine/reference/commandline/info/) | | **Display general Docker system information: number of containers, images, resources** |
|         | `docker info` | Show Docker data: versions, networks, number of containers and images |
|         | `docker info --format '{{json .}}'` | Output info in JSON format — useful for automation |
|         | `docker info --format '{{.NCPU}} CPUs, {{.MemTotal}} bytes RAM'` | Display number of CPUs and total memory |
|         | `docker info --format '{{.Driver}}'` | Show the storage driver used by Docker |
| [**`docker image pull`**](https://docs.docker.com/reference/cli/docker/image/pull/) | | **Download an image from Docker Hub or another registry. Containers cannot run without images** |
|         | `docker pull ubuntu` | Download the latest available Ubuntu image |
|         | `docker pull nginx:alpine` | Download the lightweight Nginx image based on Alpine Linux |
|         | `docker pull redis:7` | Download Redis image version 7 |
| [**`docker container run`**](https://docs.docker.com/engine/reference/commandline/run/) | | **Create and run a new container from an image** |
|         | `docker run -it ubuntu bash` | Run Ubuntu with an interactive Bash terminal |
|         | `docker run -d nginx` | Run Nginx in detached (background) mode |
|         | `docker run -p 8080:80 nginx` | Run Nginx and bind container port 80 to host port 8080 |
| [**`docker container ls`**](https://docs.docker.com/reference/cli/docker/container/ls/) | | **List running containers** |
|         | `docker ps` | Show only running containers |
|         | `docker ps -a` | Show all containers, including stopped |
|         | `docker ps --format '{{.Names}}'` | Output only container names |
| [**`docker container start`**](https://docs.docker.com/reference/cli/docker/container/start/) | | **Start one or more stopped containers** |
|         | `docker start container_name` | Start a container by name |
|         | `docker start $(docker ps -aq)` | Start all containers |
|         | `docker start -ai container_name` | Start a container and attach interactive terminal |
| [**`docker container stop`**](https://docs.docker.com/engine/reference/commandline/stop/) | | **Stop a running container** |
|         | `docker stop container_name` | Stop a container by name |
|         | `docker stop $(docker ps -q)` | Stop all running containers |
|         | `docker stop -t 5 container_name` | Stop a container giving it 5 seconds to finish processes |
| [**`docker container restart`**](https://docs.docker.com/reference/commandline/restart/) | | **Restart a container** |
|         | `docker restart container_name` | Restart a specific container |
|         | `docker restart $(docker ps -q)` | Restart all running containers |
|         | `docker restart -t 10 container_name` | Restart a container with a 10 second delay |
| [**`docker container rm`**](https://docs.docker.com/engine/reference/commandline/rm/) | | **Remove a container** |
|         | `docker rm container_name` | Remove a specific stopped container |
|         | `docker rm $(docker ps -aq)` | Remove all stopped containers |
|         | `docker rm -f container_name` | Force remove a running container |
| [**`docker image ls`**](https://docs.docker.com/engine/reference/commandline/images/) | | **List downloaded images** |
|         | `docker images` | Show all images on the host |
|         | `docker images -a` | Show all images, including intermediate layers |
|         | `docker images --format '{{.Repository}}:{{.Tag}}'` | Output only image names and tags |
| [**`docker image rm`**](https://docs.docker.com/reference/cli/docker/image/rm/) | | **Remove one or more images from local storage** |
|         | `docker rmi test1:latest` | Remove image with tag `latest` from repository `test1` |
|         | `docker rmi 1a2b3c4d5e6f` | Remove image by its ID |
|         | `docker rmi $(docker images -q)` | Remove all images (use with caution!) |

---

## 🔁 Container Management

| Command | Example | Description |
| ------- | ------- | ----------- |
| [**`docker container exec`**](https://docs.docker.com/engine/reference/commandline/exec/) | | **Run a command inside a running container** |
|         | `docker exec -it container bash` | Launch an interactive bash shell inside the container named `container` |
|         | `docker exec container ls /app` | Execute `ls` command in the `/app` directory inside the container |
|         | `docker exec -d container touch /tmp/testfile` | Run a command in the container in detached mode (no waiting) |
| [**`docker container logs`**](https://docs.docker.com/engine/reference/commandline/logs/) | | **View container logs** |
|         | `docker logs container` | Show all logs from the container `container` |
|         | `docker logs -f container` | Follow container logs in real time |
|         | `docker logs --tail 50 container` | Show last 50 lines of logs |
| [**`docker inspect`**](https://docs.docker.com/engine/reference/commandline/inspect/) | | **Retrieve detailed JSON information about a container or image** |
|         | `docker inspect container` | Display details of the container `container` |
|         | `docker inspect --format '{{.NetworkSettings.IPAddress}}' container` | Show the container’s IP address |
| [**`docker container stats`**](https://docs.docker.com/reference/cli/docker/container/stats/) | | **Show real-time resource usage statistics of containers** |
|         | `docker stats` | Display CPU, memory, network, and disk usage for all containers |
|         | `docker stats container_name` | Show stats for a specific container only |
|         | `docker stats --no-stream` | Show a one-time snapshot of stats and exit |
| [**`docker container rename`**](https://docs.docker.com/engine/reference/commandline/rename/) | | **Rename a container** |
|         | `docker rename old_name new_name` | Rename container from `old_name` to `new_name` |
| [**`docker container cp`**](https://docs.docker.com/engine/reference/commandline/cp/) | | **Copy files between a container and the host** |
|         | `docker cp container:/src/file.txt ./file.txt` | Copy a file from container to current host directory |
|         | `docker cp ./config.yaml container:/app/config.yaml` | Copy a file from host to container |
|         | `docker cp CONTAINER:/var/logs/app.log - \| tar x -O \| grep "ERROR"` | Stream a log file from container and filter "ERROR" lines without saving to disk |
| [**`docker container top`**](https://docs.docker.com/engine/reference/commandline/top/) | | **Display running processes inside a container** |
|         | `docker top container` | Show processes of the container named `container` |
| [**`docker container pause`**](https://docs.docker.com/engine/reference/commandline/pause/) | | **Pause all processes in a container** |
|         | `docker pause container` | Pause the container `container` |
| [**`docker container unpause`**](https://docs.docker.com/engine/reference/commandline/unpause/) | | **Resume a paused container** |
|         | `docker unpause container` | Resume the container `container` |
| [**`docker container update`**](https://docs.docker.com/engine/reference/commandline/update/) | | **Update container settings without restarting** |
|         | `docker update --memory 500m container` | Limit container memory usage to 500 MB |

---

## 🧱 Images and Dockerfile

| Command | Example | Description |
| ------- | ------- | ----------- |
| [**`docker buildx build`**](https://docs.docker.com/engine/reference/commandline/build/) | | **Build a Docker image from a Dockerfile** |
|         | `docker build -t my_image .` | Build an image tagged `my_image` from the current directory |
|         | `docker build -t my_image:1.0 .` | Build an image tagged with version `1.0` |
|         | `docker build --no-cache -t my_image .` | Build an image without using cache for a clean build |
| [**`docker container commit`**](https://docs.docker.com/engine/reference/commandline/commit/) | | **Create an image from the current state of a container** |
|         | `docker commit container my_img:v1` | Create image `my_img` tagged `v1` from container `container` |
|         | `docker commit -m "Added config" container my_img:v2` | Create an image with a commit message |
|         | `docker commit -a "John Doe" container my_img:latest` | Create an image specifying the author |
| [**`docker image tag`**](https://docs.docker.com/engine/reference/commandline/tag/) | | **Add or change an image tag** |
|         | `docker tag my_image myrepo/my_image:latest` | Add a tag for pushing to registry `myrepo` |
|         | `docker tag my_image:1.0 my_image:stable` | Create tag `stable` for image tagged `1.0` |
|         | `docker tag my_image my_image:backup` | Add a `backup` tag to a local image |
| [**`docker image push`**](https://docs.docker.com/engine/reference/commandline/push/) | | **Push an image to Docker Hub or another registry** |
|         | `docker push myrepo/my_image:latest` | Push image tagged `latest` to repository `myrepo` |
|         | `docker push myrepo/my_image:1.0` | Push image tagged `1.0` |
|         | `docker push myrepo/my_image` | Push image with default tag `latest` |
| [**`docker login`**](https://docs.docker.com/engine/reference/commandline/login/) | | **Authenticate to Docker Hub or another registry** |
|         | `docker login` | Enter username and password interactively for Docker Hub |
|         | `docker login myregistry.local:5000` | Login to a private registry |
|         | `docker login -u username -p password` | Login with username and password (not recommended) |
| [**`docker logout`**](https://docs.docker.com/engine/reference/commandline/logout/) | | **Logout from Docker Hub or another registry** |
|         | `docker logout` | Logout from Docker Hub |
|         | `docker logout myregistry.local:5000` | Logout from private registry |
| [**`HEALTHCHECK`**](https://docs.docker.com/reference/dockerfile/#healthcheck) | | **Dockerfile instruction to automatically check container health status** |
|         | `HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost/ \|\| exit 1` | Add health check to verify service availability every 30 seconds |
|         | `docker inspect --format='{{json .State.Health}}' container_name` | Check the healthcheck status of a running container |

---

## 🔌 Networks and Volumes

| Command | Example | Description |
| ------- | ------- | ----------- |
| [**`docker network ls`**](https://docs.docker.com/reference/cli/docker/network/ls/) | | **List all Docker networks** |
|         | `docker network ls` | Show all created Docker networks |
|         | `docker network ls --filter driver=bridge` | Show only networks with the `bridge` driver |
|         | `docker network ls --format '{{.Name}}'` | Show only network names |
| [**`docker network create`**](https://docs.docker.com/reference/cli/docker/network/create/) | | **Create a new Docker network** |
|         | `docker network create my_net` | Create a network named `my_net` with default settings |
|         | `docker network create --driver bridge my_bridge_net` | Create a network with the `bridge` driver |
|         | `docker network create --subnet=192.168.10.0/24 my_custom_net` | Create a network with a specified subnet |
| [**`docker network connect`**](https://docs.docker.com/reference/cli/docker/network/connect/) | | **Connect a container to a network** |
|         | `docker network connect my_net container` | Connect container named `container` to network `my_net` |
|         | `docker network connect --alias db_net my_net container` | Connect with alias `db_net` |
| [**`docker network disconnect`**](https://docs.docker.com/reference/cli/docker/network/disconnect/) | | **Disconnect a container from a network** |
|         | `docker network disconnect my_net container` | Disconnect container `container` from network `my_net` |
| [**`docker volume ls`**](https://docs.docker.com/reference/cli/docker/volume/ls/) | | **List all Docker volumes** |
|         | `docker volume ls` | Show all Docker volumes |
|         | `docker volume ls --filter dangling=true` | Show unused volumes |
| [**`docker volume create`**](https://docs.docker.com/reference/cli/docker/volume/create/) | | **Create a new Docker volume** |
|         | `docker volume create my_vol` | Create a volume named `my_vol` |
|         | `docker volume create --driver local --opt type=tmpfs my_tmp_vol` | Create a temporary volume using tmpfs |
| [**`docker volume inspect`**](https://docs.docker.com/reference/cli/docker/volume/inspect/) | | **Show detailed information about a volume** |
|         | `docker volume inspect my_vol` | Display details of volume `my_vol` in JSON format |
| [**`docker volume rm`**](https://docs.docker.com/reference/cli/docker/volume/rm/) | | **Remove one or more volumes** |
|         | `docker volume rm my_vol` | Remove volume named `my_vol` |
|         | `docker volume rm $(docker volume ls -qf dangling=true)` | Remove all unused volumes |

---

## 🧩 Docker Plugins

| Command | Example | Description |
| ------- | ------- | ----------- |
| [**`docker plugin ls`**](https://docs.docker.com/reference/cli/docker/plugin/ls/) | | **List installed Docker plugins** |
|         | `docker plugin ls` | Display all plugins and their status |
| [**`docker plugin install`**](https://docs.docker.com/reference/cli/docker/plugin/install/) | | **Install a Docker plugin from a registry** |
|         | `docker plugin install vieux/sshfs` | Install the SSHFS volume plugin |
|         | `docker plugin install store/weaveworks/net-plugin:latest_release` | Install the Weave network plugin |
| [**`docker plugin disable`**](https://docs.docker.com/reference/cli/docker/plugin/disable/) | | **Disable an installed plugin** |
|         | `docker plugin disable vieux/sshfs` | Disable the SSHFS plugin |
| [**`docker plugin enable`**](https://docs.docker.com/reference/cli/docker/plugin/enable/) | | **Enable a previously disabled plugin** |
|         | `docker plugin enable vieux/sshfs` | Enable the SSHFS plugin |
| [**`docker plugin rm`**](https://docs.docker.com/reference/cli/docker/plugin/rm/) | | **Remove a Docker plugin** |
|         | `docker plugin rm vieux/sshfs` | Remove the SSHFS plugin |

---

## 📋 Docker Compose

| Command | Example | Description |
| ------- | ------- | ----------- |
| [**`docker compose up`**](https://docs.docker.com/compose/reference/up/) | | **Start containers defined in `docker-compose.yml`** |
|         | `docker compose up` | Start all services in the current directory in interactive mode |
|         | `docker compose up -d` | Start services in detached mode (background) |
|         | `docker compose up --build` | Build images before starting services |
| [**`docker compose down`**](https://docs.docker.com/compose/reference/down/) | | **Stop and remove containers, networks, and volumes created by `up`** |
|         | `docker compose down` | Stop all running services and remove associated resources |
|         | `docker compose down --volumes` | Also remove volumes created by Compose |
|         | `docker compose down --rmi all` | Also remove images created by Compose |
| [**`docker compose logs`**](https://docs.docker.com/compose/reference/logs/) | | **View logs of all or specific services** |
|         | `docker compose logs` | Show logs of all services |
|         | `docker compose logs -f` | Follow logs in real time |
|         | `docker compose logs web` | Show logs for the `web` service only |
| [**`docker compose exec`**](https://docs.docker.com/compose/reference/exec/) | | **Run a command inside a running service container** |
|         | `docker compose exec web bash` | Enter an interactive bash shell inside the `web` service container |
|         | `docker compose exec db ls /var/lib/postgresql` | Run `ls` command inside the database container |
|         | `docker compose exec -d worker touch /tmp/done` | Run a command inside the `worker` container in detached mode |
| [**`docker compose build`**](https://docs.docker.com/compose/reference/build/) | | **Build or rebuild service images** |
|         | `docker compose build` | Build all images defined in `docker-compose.yml` |
|         | `docker compose build web` | Build only the `web` service image |
|         | `docker compose build --no-cache` | Build images without using cache |
| [**`docker compose ps`**](https://docs.docker.com/compose/reference/ps/) | | Show the status of all services and containers |
|         | `docker compose ps -a` | Show all containers, including stopped ones |
|         | `docker compose ps --services` | Show only the service names |
| [**`docker compose pull`**](https://docs.docker.com/compose/reference/pull/) | | Download/update service images from registry |
|         | `docker compose pull web` | Pull image only for the `web` service |
|         | `docker compose pull --ignore-pull-failures` | Continue pulling even if some images fail |
| [**`docker compose restart`**](https://docs.docker.com/compose/reference/restart/) | | Restart all or specified services |
|         | `docker compose restart db` | Restart only the `db` service |
|         | `docker compose restart -t 10` | Restart services with a 10-second timeout |
| [**`docker compose config`**](https://docs.docker.com/compose/reference/config/) | | Display the final Compose configuration in YAML format |
|         | `docker compose config --services` | List all services in the configuration |
|         | `docker compose config --volumes` | List all volumes defined in the configuration |
| [**`docker compose start`**](https://docs.docker.com/compose/reference/start/) | | Start stopped services without recreating containers |
|         | `docker compose start web` | Start the `web` service |
|         | `docker compose start db api` | Start multiple services at once |
| [**`docker compose stop`**](https://docs.docker.com/compose/reference/stop/) | | Stop services without removing containers |
|         | `docker compose stop web` | Stop the `web` service |
|         | `docker compose stop -t 5` | Stop services with a 5-second timeout |

---

## 📤 Export and Import

| Command | Example | Description |
| ------- | ------- | ----------- |
| [**`docker image save`**](https://docs.docker.com/reference/cli/docker/image/save/) | | **Save one or more Docker images to a tar archive for later import or transfer** |
|         | `docker save -o image.tar my_img:tag` | Save a Docker image to a tar archive file |
|         | `docker save my_image > my_image.tar` | Alternative way to save an image to a file |
|         | `docker save -o redis_latest.tar redis:latest` | Save a specific Redis image to a file |
| [**`docker image load`**](https://docs.docker.com/reference/cli/docker/image/load/) | | **Load Docker images from a previously saved tar archive** |
|         | `docker load < image.tar` | Load a Docker image from a tar archive file |
|         | `docker load --input redis_latest.tar` | Load an image specifying the file via parameter |
|         | `docker load --quiet < my_image.tar` | Load an image without progress output |
| [**`docker container export`**](https://docs.docker.com/reference/cli/docker/container/export/) | | **Export a container’s filesystem as a tar archive without image history or metadata** |
|         | `docker export container > file.tar` | Export container filesystem to an archive |
|         | `docker export my_container > my_container_fs.tar` | Export container by name |
|         | `docker export -o container_fs.tar container_id` | Export by container ID using the `-o` flag |
| [**`docker image import`**](https://docs.docker.com/reference/cli/docker/image/import/) | | **Create a new image from a tar archive of a filesystem** |
|         | `docker import file.tar new_img` | Import archive file as a new Docker image |
|         | `docker import https://example.com/image.tar my_new_image` | Import image directly from a URL |
|         | `docker import - my_image < file.tar` | Import from standard input |

---

## 🧹 Cleanup and Diagnostics

| Command | Example | Description |
| ------- | ------- | ----------- |
| [**`docker system df`**](https://docs.docker.com/reference/cli/docker/system/df/) | | **Show Docker disk usage: volumes, images, containers, and build cache** |
|         | `docker system df -v` | Detailed output with info on each image, container, and volume |
|         | `docker system df --format '{{json .}}'` | Output information in JSON format |
| [**`docker system prune`**](https://docs.docker.com/reference/cli/docker/system/prune/) | | **Remove all unused Docker data: stopped containers, unused networks, dangling images, and build cache** |
|         | `docker system prune -a` | Remove unused images including intermediate ones |
|         | `docker system prune --volumes` | Remove unused volumes along with other resources |
| [**`docker image prune`**](https://docs.docker.com/reference/cli/docker/image/prune/) | | **Remove unused Docker images including dangling layers** |
|         | `docker image prune -a` | Remove all unused images including dangling ones |
|         | `docker image prune --filter "until=24h"` | Remove images older than 24 hours |
| [**`docker container prune`**](https://docs.docker.com/reference/cli/docker/container/prune/) | | **Remove stopped containers matching filters or all if none specified** |
|         | `docker container prune --filter "until=24h"` | Remove stopped containers older than 24 hours |
|         | `docker container prune --force` | Remove without confirmation prompt |

---

## 🐝 Docker Swarm

| Command | Example | Description |
| ------- | ------- | ----------- |
| [**`docker swarm init`**](https://docs.docker.com/reference/cli/docker/swarm/init/) | | **Initialize a new Docker Swarm cluster on the current node** |
|         | `docker swarm init --advertise-addr 192.168.1.100` | Initialize the cluster specifying the IP address |
|         | `docker swarm init --listen-addr 0.0.0.0:2377` | Initialize with a specified listen port |
| [**`docker service create`**](https://docs.docker.com/reference/cli/docker/service/create/) | | **Create a new service in the Swarm cluster** |
|         | `docker service create --name nginx nginx` | Create an Nginx service in Swarm |
|         | `docker service create --replicas 3 --name web webserver` | Create a service with 3 replicas |
|         | `docker service create --name redis --publish 6379:6379 redis` | Create a service with port mapping |
| [**`docker stack deploy`**](https://docs.docker.com/reference/cli/docker/stack/deploy/) | | **Deploy a stack of services to the Swarm cluster based on a Compose file** |
|         | `docker stack deploy -c docker-compose.yml mystack` | Deploy stack from compose file |
|         | `docker stack deploy --with-registry-auth -c compose.yml mystack` | Deploy with registry authentication forwarding |
|         | `docker stack deploy -c swarm-compose.yml mystack` | Use an alternative compose file for the stack |
| [**`docker stack rm`**](https://docs.docker.com/reference/cli/docker/stack/rm/) | | **Remove one or more stacks from the Swarm cluster** |
|         | `docker stack rm mystack` | Remove the `mystack` stack |
|         | `docker stack rm` | Remove all stacks (not recommended) |
|         | `docker stack rm mystack && docker swarm leave --force` | Remove stack and leave Swarm |

---

## 💼 Advanced Docker Usage

### 🚀 Professional Docker Commands

| Command | Example | Description |
| ------- | ------- | ----------- |
| [**`docker buildx`**](https://docs.docker.com/reference/cli/docker/buildx/) | | **Advanced image build tool replacing `docker build`. Supports multi-platform, caching, parallel builds, and exporting to various formats. Useful for CI/CD and cross-platform development** |
|         | `docker buildx build --platform linux/arm64,linux/amd64 -t myimg:multi .` | Build a multi-platform image (ARM and x86 simultaneously) |
|         | `docker buildx build --load -t localimg .` | Build an image and load it into the local Docker Engine cache |
|         | `docker buildx build --push --platform linux/amd64,linux/arm64 -t repo/app:latest .` | Build and push a multi-platform image to a registry |
| [**`docker context`**](https://docs.docker.com/reference/cli/docker/context/) | | **Manage Docker contexts for working with remote or multiple environments. Enables quick switching between local and remote Docker Engines** |
|         | `docker context create myremote --docker "host=ssh://user@host"` | Create a context for connecting to a remote Docker host |
|         | `docker context use myremote` | Switch to the remote context |
|         | `docker context ls` | List available contexts and the active one |
| [**`docker system events`**](https://docs.docker.com/reference/cli/docker/system/events/) | | **Listen to Docker events in real time, with filtering by event type (e.g., container start). Useful for monitoring and automation** |
|         | `docker events --filter 'event=start'` | Show only container start events |
|         | `docker events --since 1h --until 10m` | Show events from the last hour until 10 minutes ago |
|         | `docker events --filter 'type=network'` | Show only network-related events |
|         | `docker events --filter 'image=nginx'` | Show events related to the `nginx` image |
| [**`docker container update`**](https://docs.docker.com/reference/cli/docker/container/update/) | | **Change resource limits and settings of a running container without restarting it** |
|         | `docker update --cpus 2 --memory 1g my_container` | Set limit to 2 CPUs and 1 GB RAM |
|         | `docker update --restart unless-stopped my_container` | Set auto-restart policy to `unless-stopped` |
|         | `docker update --pids-limit 200 my_container` | Limit the number of processes to 200 |
| [**`docker container diff`**](https://docs.docker.com/reference/cli/docker/container/diff/) | | **Show filesystem changes in a container compared to its original image. Useful for debugging and auditing** |
|         | `docker diff my_container` | Show all filesystem changes in the container |
|         | `docker diff my_container \| grep '^A'` | Show only added files (`A` — Added) |
| [**`docker image history`**](https://docs.docker.com/reference/cli/docker/image/history/) | | **Display the history of image layers: build commands, size of each layer, and creation time. Useful for optimization and auditing** |
|         | `docker history my_image` | Show layer history of an image |
|         | `docker history --no-trunc my_image` | Show full build commands without truncation |
|         | `docker history --format "{{.CreatedBy}}: {{.Size}}" my_image` | Output only build commands and layer sizes |

### 🛠 Useful Docker Practices and Automation

- **Minimize image size**  
  Use base images like `alpine` or `scratch` for minimal size.
  To squash layers, you can use `--squash` during build (requires experimental features enabled).  
  Also, remove temporary files and caches in a single layer:

  ```dockerfile
  RUN apk add --no-cache curl && rm -rf /var/cache/apk/*
  ```

- **Minimize number of layers**
  Combine commands in one `RUN` to reduce the number of layers and final image size:

  ```dockerfile
  RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
  ```

- **Optimize Dockerfile build**  
  Use multi-stage builds so only necessary files remain in the final image.
Copy and install dependencies first, then copy code — this improves layer caching and speeds up rebuilds.
- **Separate secrets and configs**  
  Never store `.env` files, API keys, or private certificates inside the image.
  Use for configuration:
  - `docker secret` (in Swarm)
  - environment variables (`-e VAR=value` or `.env`)
  - external volumes for configs
- **Build-time secrets (BuildKit)**
  For secure secret passing during build, use the `--secret` flag:

  ```bash
  docker buildx build --secret id=mysecret,src=./secret.txt .
  ```

  In Dockerfile, secret is available at `/run/secrets/mysecret`:

  ```dockerfile
  RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
  ```

  🛡 This prevents secrets from being stored in image layers.
- **Rootless Docker**
  Running Docker without root rights improves security and reduces host compromise risk.
  To enable:

  ```bash
  dockerd-rootless-setuptool.sh install
  export PATH=/usr/bin:$PATH
  ```

  Check:

  ```bash
  docker info | grep Rootless
  ```

  ⚠ Some features (e.g., port forwarding <1024) will be unavailable.
- **Scan images for vulnerabilities**
  Use built-in tools:

  ```bash
  docker scan my_image
  ```

  Or the new CLI:

  ```bash
  docker scout cves my_image
  ```

  This helps detect vulnerabilities in base images and dependencies.
- **Monitor resource usage**  
  Limit containers by memory, CPU, and process count:

  ```bash
  docker run --memory=512m --cpus="1.5" --pids-limit=200 myimage
  ```

  This prevents resource overconsumption.
  You can also limit I/O:

  ```bash
  docker run --device-read-bps /dev/sda:1mb --device-write-bps /dev/sda:1mb myimage
  ```

  Useful for containers that shouldn’t overload disk subsystem.
- **Automatic cleanup**
  Regularly remove unused images, containers, volumes, and networks:

  ```bash
  docker system prune -af --volumes
  ```

  > ⚠ Be careful: this command deletes all unused resources.
  
  For selective cleanup use:

  ```bash
  docker image prune --filter "until=24h"
  ```

- **CI/CD integration**
  Embed build, test, and deploy into GitHub Actions, GitLab CI, Jenkins pipelines.
  Example GitHub Actions step:

  ```yaml
  - run: docker build -t myapp:${GITHUB_SHA} .
  - run: docker push myapp:${GITHUB_SHA}
  ```

- **Logging and monitoring**
  Attach logging drivers (`--log-driver`) to centralized systems: ELK, Loki, Splunk.
Use Prometheus + cAdvisor for container metrics.
- **Production deployment**
  Separate configs for development and production using `docker-compose.override.yml`.
For high availability and scaling use:
  - Docker Swarm
  - Kubernetes

### 🐞 Debugging and Profiling Docker Containers

| Command | Example | Description |
| ------- | ------ | ----------- |
| [**`docker container exec`**](https://docs.docker.com/reference/cli/docker/container/exec/) | | **Runs a command inside a running container, providing interactive access or the ability to run processes in the container's isolated environment** |
|         | `docker exec -it my_container bash` | Start an interactive terminal (bash) inside a running container |
|         | `docker exec -it my_container sh` | Start a minimal shell inside the container (if bash is unavailable) |
|         | `docker exec my_container ls /app` | Run a command inside the container without interactive mode |
| [**`docker container logs`**](https://docs.docker.com/reference/cli/docker/container/logs/) | | **Displays logs of the specified container, allowing to view output and events related to its operation for diagnostics and monitoring** |
|         | `docker logs -f --tail 100 my_container` | View the last 100 lines of logs with real-time streaming |
|         | `docker logs my_container` | Show all available logs of the container |
|         | `docker logs --since 1h my_container` | Show logs from the last hour |
| [**`docker inspect`**](https://docs.docker.com/reference/cli/docker/inspect/) | | **Outputs detailed information about a Docker object (container, image, network, etc.) in JSON format, including configuration and state** |
|         | `docker inspect my_container` | Get full JSON info about the container |
|         | `docker inspect --format '{{.State.Pid}}' my_container` | Get the PID of the container’s main process on the host |
|         | `docker inspect --format '{{.NetworkSettings.IPAddress}}' my_container` | Show the container's IP address |
| [**`nsenter`**](https://man7.org/linux/man-pages/man1/nsenter.1.html) (with `strace`) | | **Linux utility to enter the namespaces of another process (here, the container). Used with `strace` to trace system calls inside the container for debugging** |
|         | `nsenter --target $(docker inspect --format '{{.State.Pid}}' my_container) --mount --uts --ipc --net --pid strace -p 1` | Enter container namespaces and trace system calls of process 1 |
|         | `nsenter --target $(docker inspect --format '{{.State.Pid}}' my_container) --mount --uts --ipc --net --pid bash` | Open bash shell inside container namespaces |
|         | `nsenter --target $(docker inspect --format '{{.State.Pid}}' my_container) --net netstat -tulnp` | View open ports inside the container |
| [**`tcpdump`**](https://www.tcpdump.org/manpages/tcpdump.1.html) (inside container) | `docker exec -it my_container tcpdump -i any` | **Console tool for capturing and analyzing network traffic. Used in container to diagnose network issues, analyze packets, and monitor connections** |
|         | `docker exec -it my_container tcpdump -i any` | Capture and analyze network traffic inside container |
|         | `docker exec -it my_container tcpdump -nn port 80` | Capture traffic only on port 80 |
|         | `docker exec -it my_container tcpdump -w /tmp/dump.pcap` | Save traffic to file for later analysis |
| [**`docker container stats`**](https://docs.docker.com/reference/cli/docker/container/stats/) | | **Shows current resource usage metrics (CPU, memory, network, disk) for one or multiple containers in real time** |
|         | `docker stats my_container` | Display real-time CPU, memory, network, and disk usage by the container |
|         | `docker stats` | Show stats for all containers |
|         | `docker stats --no-stream` | Output stats once and exit |
| [**`docker container top`**](https://docs.docker.com/reference/cli/docker/container/top/) | | **Displays the list of processes running inside the container, similar to `ps` in Linux, to analyze container activity** |
|         | `docker top my_container` | Show processes running inside the container |
|         | `docker top my_container aux` | Use alternate output format like `ps aux` |
|         | `docker top my_container -eo pid,cmd` | Show only PID and command of processes |
| [**`docker diff`**](https://docs.docker.com/reference/cli/docker/container/diff/) | | **Shows changes in the container’s filesystem compared to its base image, indicating added, changed, or deleted files** |
|         | `docker diff my_container` | Show filesystem changes in the container compared to the base image |
|         | `docker diff my_container \| grep '^A'` | Show only added files (`A` — Added) |
|         | `docker diff my_container \| grep '^C'` | Show only changed files (`C` — Changed) |
| [**`docker cp`**](https://docs.docker.com/reference/cli/docker/container/cp/) | | **Copies files and directories between a container and the host machine, enabling data exchange and backup** |
|         | `docker cp my_container:/path/to/file ./file` | Copy file from container to host |
|         | `docker cp ./config.yaml my_container:/app/config.yaml` | Copy file from host into container |
|         | `docker cp my_container:/var/log/app.log - \| tar x -O \| grep "ERROR"` | Copy log file and filter error lines without saving to disk |

> 💡 For advanced debugging you can use `nsenter`, `strace`, `tcpdump`, `gdb`, and other low-level tools.

---

## 💼 Advanced Docker Compose Usage

### 🚀 Professional Docker Compose Commands

| Command | Example | Description |
| ------- | ------ | ----------- |
| [**`docker compose up`**](https://docs.docker.com/reference/cli/docker/compose/up/) | | **Start and manage the lifecycle of specified services from the docker-compose.yml file with the ability to run in the background** |
|         | `docker compose up -d web db` | Run only the `web` and `db` services in detached mode |
|         | `docker compose up --build` | Rebuild images before starting services |
|         | `docker compose up --remove-orphans` | Remove containers not defined in the current compose file |
| [**`docker compose build`**](https://docs.docker.com/reference/cli/docker/compose/build/) | | **Build images for services as described in the compose file with cache control and parallelism** |
|         | `docker compose build --no-cache` | Fully rebuild images without using cache |
|         | `docker compose build --parallel` | Build all services concurrently to speed up the process |
|         | `docker compose build web` | Build image only for the `web` service |
| [**`docker compose pull`**](https://docs.docker.com/reference/cli/docker/compose/pull/) | | **Download the latest versions of images from the registry for all or specified services** |
|         | `docker compose pull` | Pull images for all services |
|         | `docker compose pull db` | Pull image only for the `db` service |
|         | `docker compose pull --ignore-pull-failures` | Continue execution ignoring errors during image pull |
| [**`docker compose restart`**](https://docs.docker.com/reference/cli/docker/compose/restart/) | | **Restart all or specified services without recreating containers** |
|         | `docker compose restart` | Restart all services in the current project |
|         | `docker compose restart worker` | Restart only the `worker` service |
|         | `docker compose restart web db` | Restart multiple services at once |
| [**`docker compose exec`**](https://docs.docker.com/reference/cli/docker/compose/exec/) | | **Execute a command inside a running service container with optional interactive mode** |
|         | `docker compose exec db psql -U user -d database` | Run psql inside the `db` service container |
|         | `docker compose exec web sh` | Open a shell inside the `web` container |
|         | `docker compose exec api curl http://localhost:8080` | Execute curl request from the `api` service container |
| [**`docker compose config`**](https://docs.docker.com/reference/cli/docker/compose/config/) | | **Output the final Compose configuration considering all files and environment variables** |
|         | `docker compose config` | Show merged configuration in YAML format |
|         | `docker compose config --services` | List all services |
|         | `docker compose config --environment` | Show all environment variables used by services |
| [**`docker compose watch`**](https://docs.docker.com/reference/cli/docker/compose/watch/) | | **Automatically restart services on source file changes, useful for development** |
|         | `docker compose watch` | Start watching files and restart services on changes |
| [**`docker compose events`**](https://docs.docker.com/reference/cli/docker/compose/events/) | | **Stream Compose events: service start, stop, update** |
|         | `docker compose events --json` | Receive events in JSON format |
| [**`docker compose rm`**](https://docs.docker.com/reference/cli/docker/compose/rm/) | | **Remove stopped service containers** |
|         | `docker compose rm web db` | Remove containers of `web` and `db` services |
| [**`docker compose pause`**](https://docs.docker.com/reference/cli/docker/compose/pause/) | | **Pause service operation** |
|         | `docker compose pause api` | Pause the `api` service |
| [**`docker compose unpause`**](https://docs.docker.com/reference/cli/docker/compose/unpause/) | | **Resume paused services** |
|         | `docker compose unpause api` | Resume the `api` service |
| [**`docker compose create`**](https://docs.docker.com/reference/cli/docker/compose/create/) | | **Create containers without starting them** |
|         | `docker compose create web db` | Create containers for `web` and `db` but do not start them |
| [**`docker compose images`**](https://docs.docker.com/reference/cli/docker/compose/images/) | | **Show list of images used by services** |
|         | `docker compose images` | Display images of all services |
| [**`docker compose top`**](https://docs.docker.com/reference/cli/docker/compose/top/) | | **Show processes running inside service containers** |
|         | `docker compose top web` | Show processes inside containers of the `web` service |

### 🛠 Useful Practices and Automation with Docker Compose

- **Environment Separation**  
  Use separate `docker-compose.override.yml` files for different environments — `development`, `staging`, `production`. This helps isolate configurations and avoid conflicts between settings.  
  You can also combine multiple config files using the `-f` flag:

  ```bash
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
  ```

  Use different `.env` files (`.env.dev`, `.env.prod`, etc.) to manage environment variables.
- **Secure Secrets Storage**  
  Do not include sensitive data (passwords, tokens) directly in Compose files. Instead, use:
  - `.env` files for environment variables (note that `.env` files are not encrypted and should not be committed to public repos)
  - `docker secret` and `docker config` for secure secrets and configuration management in Docker Swarm
  - external volumes for configuration files containing secrets
  - external secret management systems (e.g., HashiCorp Vault, AWS Secrets Manager)
- **Startup Order with `depends_on` and `healthcheck`**
  To make services wait for dependencies to be ready:

  ```yaml
  services:
    db:
      image: postgres
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U postgres"]
        interval: 10s
        retries: 5
    api:
      image: my_api
      depends_on:
        db:
          condition: service_healthy
  ```

- **Minimize Downtime During Updates**  
  Before updating services, run:
  
  ```bash
  docker compose pull && docker compose up -d --remove-orphans
  ```

  The `-d` option runs containers in the background, and `--remove-orphans` removes containers not defined in current configs.
To fully stop and remove old containers if needed:

  ```bash
  docker compose down --remove-orphans
  ```

  This ensures fresh images are loaded and unused containers are removed without downtime.
- **Hot Code Reloading for Development**
  Use `volumes` to mount local directories into containers. This allows instant application of code changes without rebuilding images.
  Be mindful of file permission issues and filesystem caching peculiarities, especially on Windows and macOS, to avoid performance problems.
- **Hot Code Reloading Without Volume (Compose 2.22+)**

  ```yaml
  develop:
    watch:
      - path: ./src
        action: sync
        target: /app
  ```

- **Centralized Logging of Services**
  Redirect container logs to monitoring and log aggregation systems like ELK Stack, Loki, Prometheus, and Fluentd for easy analysis and alerting.
  Use Docker logging drivers (`--log-driver`) to enable centralized log collection and processing.
  Configure logging drivers for containers in Compose:

  ```yaml
  services:
    api:
      image: my_api
      logging:
        driver: "json-file"
        options:
          max-size: "10m"
          max-file: "3"
  ```

- **Automatic Service Restart**
  Configure restart policy in `docker-compose.yml`:

  ```yaml
  restart: unless-stopped
  ```

  Other restart policies include:
  - `no` — no automatic restart (default)
  - `always` — always restart container
  - `on-failure` — restart only on failures (optionally with retry count)
  
  In production, `unless-stopped` is the optimal choice to ensure service resilience.
  This enables automatic recovery of services after failures or host reboots.
- **Service Profiles**  
  Allow running only specific groups of services:

  ```yaml
  services:
    db:
      image: postgres
      profiles: ["backend"]
    web:
      image: nginx
      profiles: ["frontend"]
  ```

  To run only the frontend profile:

  ```bash
  docker compose --profile frontend up
  ```

### 🐞 Debugging and Profiling Services in Docker Compose

| Command | Example | Description |
| ------- | ------ | ----------- |
| [**`docker compose exec`**](https://docs.docker.com/reference/cli/docker/compose/exec/) | | **Execute a command inside a running service, providing access to the container or running individual processes** |
|         | `docker compose exec web sh` | Open a shell inside the `web` service container |
|         | `docker compose exec db psql -U user -d database` | Run the psql command inside the `db` service container |
| [**`docker compose logs`**](https://docs.docker.com/reference/cli/docker/compose/logs/) | | **View service logs for diagnostics and monitoring** |
|         | `docker compose logs -f db` | View `db` service logs in real-time |
|         | `docker compose logs --tail=50 api` | Show the last 50 lines of logs from the `api` service |
|         | `docker compose logs --since=1h web` | Show logs from the last hour for the `web` service |
| [**`docker inspect`**](https://docs.docker.com/reference/cli/docker/inspect/) | | **View detailed information about the container running a service** |
|         | `docker inspect $(docker compose ps -q web)` | Get JSON with detailed info about the `web` service container |
| [**`docker container stats`**](https://docs.docker.com/reference/cli/docker/container/stats/) | | **Monitor resource usage of containers running services** |
|         | `docker stats $(docker compose ps -q worker)` | Track CPU, memory, and other resource usage for the `worker` service container |
| [**`docker compose run --rm`**](https://docs.docker.com/reference/cli/docker/compose/run/) | | **Run a temporary container with service settings, useful for debugging** |
|         | `docker compose run --rm web sh` | Start a one-off container for the `web` service with an interactive shell |
| [**`docker container cp`**](https://docs.docker.com/reference/cli/docker/container/cp/) | | **Copy files between host and container** |
|         | `docker cp $(docker compose ps -q db):/dump.sql ./dump.sql` | Copy a file from the `db` service container to the host |

> 💡 For convenient debugging of complex multi-service setups, use `docker compose run --rm` to launch individual containers with necessary networks and volumes without affecting main services.

---

## Additional Resources

### 🚫 Ignoring Files with `.dockerignore`

Add files and folders to the `.dockerignore` file that should not be included in the image to reduce size and speed up the build:

```text
node_modules/
*.log
.env
```

### ⚡ Simplifying Commands with Aliases

You can create aliases for frequently used commands to run them faster:

```bash
alias dcu="docker compose up -d"
alias dcd="docker compose down"
alias dcb="docker compose build"
```

### 🧠 Tip: Docker Usage Advice

- Don’t try to memorize everything — use `docker --help` or `docker <command> --help` to explore commands.
- Practice regularly and experiment with simple projects.
- Keep an eye on image sizes and remove unnecessary files via `.dockerignore`.

### 🌐 Useful Links

📘 **Official Docker Documentation** — comprehensive guides and references on all Docker topics:
[https://docs.docker.com/](https://docs.docker.com/)

📙 **Docker Cheat Sheet** — complete official Docker cheat sheet:
[https://dockerlabs.collabnix.com/docker/cheatsheet/](https://dockerlabs.collabnix.com/docker/cheatsheet/)

📗 **Docker Hub** — images and registries:
[https://hub.docker.com/](https://hub.docker.com/)
