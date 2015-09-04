This document explains how to install and run a Plone instance from a Docker container.

## Contents ##

* A. [About containers and Docker](#A)
* B. [Installing Docker](#B)
  - B.1 [Linux](#B1)
  - B.2 [Windows](#B2)
  - B.3 [Mac OS X](#B3)
* C. [Running Plone from a Docker container](#C)
  - C.1 [Using the `docker-compose` command (Linux and OS X)](#C1)
     - C.1.1 [Linux](#C11)
     - C.1.2 [Mac OS X](C12#)
  - C.2 [Using the `docker` command (Windows)](#C2)

## <a name="A"></a> A. About containers and Docker ##

In short, a _container_ can be seen as an isolated environment within an operating system in which applications and processes can be executed independently of the other processes running on the host machine.  
_Docker_ is a software which automates the deployment of applications inside containers.  
_Docker containers_ can be built and deployed only on a Linux operating system - that is, the prerequisite for building and running Docker containers is to have an underlying Linux environment. This means that Docker cannot be installed directly under non-Linux operating systems (such as Windows); it is necessary to first create a Linux environment and then install Docker.

More information about Docker can be found here: _[What is Docker](https://www.docker.com/whatisdocker "What is Docker")._

## <a name="B"></a> B. Installing Docker ##

In order to build and run a container, you first need to install Docker. The installation steps to be taken depend on the operating system of your computer, as follows:

### <a name="B1"></a> B.1 Linux ###

The way to install Docker varies depending on the Linux distribution on your computer. You can find specific installation instructions for your distribution here: _[Docker Installation](https://docs.docker.com/installation/ "Docker Installation")_.

### <a name="B2"></a> B.2 Windows ###

Because Docker relies on Linux-specific features, you can’t install it and run it natively in Windows. One approach is to install the _Docker Toolbox_ application which sets up a specific Docker environment on your computer. The Toolbox installs a set of tools which allows you to manage and run Docker containers; in addition to the core  Docker software, it installs other software such as _Oracle VirtualBox_ and _Git_.

There are two requirements in order to be able to install the Docker Toolbox:  
- Windows _Version_ - your machine must be running Windows 7 or newer;  
- Windows _Virtualization_ - make sure that your Windows supports Hardware Virtualization Technology and that virtualization is enabled.  
\> for Windows 8/8.1 or newer, choose Start > Task Manager and navigate to the Performance tab. Under CPU, the Virtualization setting should show “Enabled”; If virtualization is not enabled on your system, follow the manufacturer’s instructions for enabling it;  
\> for Windows 7, run the _[Microsoft Hardware-Assisted Virtualization Detection Tool](http://www.microsoft.com/en-us/download/details.aspx?id=592 "Microsoft Hardware-Assisted Virtualization Detection Tool")_ and follow the instructions.

If you already have installed the VirtualBox, there is no need to uninstall it. When prompted by the Docker Toolbox installer, indicate not to reinstall VirtualBox. If you have VirtualBox runnig, shut it down.

Follow these steps to install Docker Toolbox:  
1. Navigate to the _[Docker Toolbox](https://www.docker.com/toolbox "Docker Toolbox")_ page and click the installer link to download it.  
2. Double-click the installer to launch the Docker Toolbox setup wizard. If the Windows security dialog prompts you to allow the program to make changes to your computer, choose Yes.  
3. Follow the steps prompted by the wizard by pressing Next; when prompted with the “Select Components” screen, uncheck “VirtualBox” if you already have it installed on your computer.  
4. Press Install to start the actual installation. If notified by Windows Security that the installer will make changes, make sure you allow the installer to make the necessary changes.  
5. When it completes, the installer reports it was successful. Uncheck “View Shortcuts in File Explorer” and press Finish.

Launch a Docker Toolbox _terminal_ by double-clicking the “Docker Quickstart Terminal” icon on your Desktop. If the system displays a User Account Control prompt to allow VirtualBox to make changes to your computer, choose Yes.  
The terminal does several things to set up Docker Toolbox for you. When it is done, the terminal displays the **`$`** prompt where you can type _bash_ commands; the terminal runs a special bash environment instead of the standard Windows command prompt, since the bash environment is required by Docker.

More information about installing Docker and working with containers can be found here: _[Get Started with Docker for Windows](http://docs.docker.com/windows/started/ "Get Started with Docker for Windows")_.

### <a name="B3"></a> B.3 Mac OS X ###

Because Docker relies on Linux-specific features, you can’t install it and run it natively in OS X. One approach is to install the _Docker Toolbox_ application which sets up a specific Docker environment on your computer. The Toolbox installs a set of tools which allows you to manage and run Docker containers; in addition to the core  Docker software, it installs other software such as _Oracle VirtualBox_ and _Git_.

One requirement in order to be able to install the Docker Toolbox is the OS X _version_. Your machine must be running OS X 10.8 “Mountain Lion” or newer. Choose “About this Mac” from the Apple menu to find out the version of your OS.

If you already have installed the VirtualBox, there is no need to uninstall it. When prompted by the Docker Toolbox installer, you can indicate to upgrade VirtualBox. If you have VirtualBox runnig, shut it down.

Follow these steps to install Docker Toolbox:  
1. Navigate to the _[Docker Toolbox](https://www.docker.com/toolbox "Docker Toolbox")_ page and click the installer link to download it.  
2. Double-click the installer to launch the Docker Toolbox setup wizard.  
3. Follow the steps prompted by the wizard by pressing Continue.  
4. Press Install to start the actual installation. If the system prompts you for your password, provide it and continue with the installation.  
5. When it completes, the installer provides you some shortcuts which you can immediately use to get started with Docker. You can ignore this for now and click Continue to finish the installation.

Launch a Docker Toolbox _terminal_ by clicking the “Docker Quickstart Terminal” icon from the Launchpad. The terminal does several things to set up Docker Toolbox for you. When it is done, the terminal displays the **`$`** prompt where you can type _bash_ commands; the terminal runs a special bash environment instead of the standard Windows command prompt, since the bash environment is required by Docker.

More information about installing Docker and working with containers can be found here: _[Get Started with Docker for Mac OS X](http://docs.docker.com/mac/started/ "Get Started with Docker for Mac OS X")_.

## <a name="C"></a> C. Running Plone from a Docker container ##

There are two ways of building and running a docker container using the terminal:  
- by issuing the `docker` command and manually specifying configuration parameters of the container at the terminal prompt (parameters such as the name of the container, ports to be used for accessing the container etc.);  
- by issuing the `docker-compose` command which automatically reads the configuration parameters of the container from an existing configuration file (e.g.: the “docker-compose.yml” file).

A good practice is to use the `docker-compose` command. Given the fact that, for now, the Docker Toolbox version for Windows does not support this command, the `docker` command can be used instead.

### <a name="C1"></a> C.1 Using the **`docker-compose`** command (Linux and OS X) ###

In order to build and run a Plone container using the docker-compose command, first ensure that you have the “docker-compose.yml” file on your computer - for example in a newly created folder inside your “home” folder.

#### <a name="C11"></a> C.1.1 Linux ####

Using a terminal, navigate to the folder which contains the “docker-compose.yml” configuration file and issue the following command (without the “$”):

**$** `docker-compose up -d`

This will create and run a Docker container with a Plone instance. The “-d” parameter indicates the command to run the container in background - this way you can have the terminal prompt available in order to issue further commands, if needed.

In order to access the Plone instance using the web browser, enter “localhost” or “127.0.0.1” in address bar of the browser. After pressing Enter, the Plone start page should be displayed on your browser. Note that this works as long as the Plone container is running. To stop, start and restart it, you can issue the following commands:

**$** `docker-compose stop`  
**$** `docker-compose start`  
**$** `docker-compose restart`

#### <a name="C12"></a> C.1.2 Mac OS X ####

Using the Docker Toolbox terminal, navigate to the folder which contains the “docker-compose.yml” configuration file and issue the following command (without the “$”):

**$** `docker-compose up -d`

This will create and run a Docker container with a Plone instance. The “-d” parameter indicates the command to run the container in background - this way you can have the terminal prompt available in order to issue further commands, if needed.

In order to access the Plone instance using the web browser, you first need to identify the IP address of the Docker environment on your computer. Issue the following command to accomplish this:

**$** `echo $DOCKER_HOST`

This should display an address which has the following format: “protocol://**ip\_address**:port” (for example “tcp://192.168.99.100:2376”). Open a web browser and enter the IP address (only **ip\_address**) in the address bar of the browser. After pressing Enter, the Plone start page should be displayed on your browser. Note that this works as long as the Plone container is running. To stop, start and restart it, you can issue the following commands:

**$** `docker-compose stop`  
**$** `docker-compose start`  
**$** `docker-compose restart`

### <a name="C2"></a> C.2 Using the **`docker`** command (Windows) ###

Using the Docker Toolbox terminal, issue the following command (without the “$”):

**$** `docker run -d -p 80:80 --name eeacms_plone_container eeacms/plone`

The will create a Docker container named “eeacms\_plone\_container” and starts it in background. You can verify this by issuing the following command, which displays details (such as container ID, name, status etc.) about all running containers:

**$** `docker ps`

Alternatively, you can issue the following command, which displays details about all containers, either running or stopped:

**$** `docker ps -a`

In order to access the Plone instance using the web browser, you first need to identify the IP address of the Docker environment on your computer. Issue the following command to accomplish this:

**$** `echo $DOCKER_HOST`

This should display an address which has the following format: “protocol://**ip\_address**:port” (for example “tcp://192.168.99.100:2376”). Open a web browser and enter the IP address (only **ip\_address**) in the address bar of the browser. After pressing Enter, the Plone start page should be displayed on your browser. Note that this works as long as the Plone container (named “eeacms\_plone\_container”) is in a running state.
To stop, start and restart the “eeacms\_plone\_container” container, you can issue the following commands at the Docker Toolbox terminal:

**$** `docker stop eeacms_plone_container`  
**$** `docker start eeacms_plone_container`  
**$** `docker restart eeacms_plone_container`

