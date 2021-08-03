## Setup local environment

Create a .env file from .env-sample

Create a app/logging.cfg file from app/logging.cfg.stdout

## Running with Docker

### Build Docker Image

When you start using docker, you need to download the sourcecode and do this in the root folder. If the code has changed, just run it again and it will update the image.

    docker build -t ccm/backend  .

### Create Container

If you want to see the backend logs:

    docker run -p 5000:5000 --name ccm-backend ccm/backend

Run it in the background:

    docker run -p 5000:5000 -d --name ccm-backend ccm/backend

### Stop

    docker stop ccm-backend

### Start

If you stopped the container and don't want to rebuild it, don't use Build and Create, only Start and Stop. 

    docker start ccm-backend

### Checking the running containers

    docker ps

### Delete Contaier

If something wrong with the Container and you want to have a clean state

    docker kill ccm-backend
    
### Delete Image

You can only do this if the container is not running. Same as delete Container.

    docker rmi ccm/backend
