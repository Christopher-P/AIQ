# Docker
Docker allows for easy to install and greater flexability across systems.

To begin, make changes in the full_test.py.
More files can be added by modifying the last line of the Dockerfile.

Change sample.yml to credentials.yml and fill out with your AIQ website login.

To create the Docker image, simply run the following command.

```bash
docker build -t [name] .
```

this will proceed to download the required applications and python packages.

Once this is completed, run the following code to execute:

```bash
docker run [name]
```

Ignore these errors, they are a result of ViZDoom being run in a docker:
```bash
Cannot connect to server socket err = No such file or directory
Cannot connect to server request channel
jack server is not running or cannot be started
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for 4294967295, skipping unlock
JackShmReadWritePtr::~JackShmReadWritePtr - Init not done for 4294967295, skipping unlock
```
