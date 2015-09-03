This document explains how to install and run a Plone instance from a Docker container.

## Introduction ##

  In short, a *container* can be seen as an isolated environment within an operating system in which applications and processes can be executed independently of the other processes running on the host machine.
*Docker containers* can be built and deployed only on a Linux operating system - that is, the prerequisite for building and running Docker containers is to have an underlying Linux environment. This means that *Docker* cannot be installed directly under non-Linux operating systems (such as Windows); it is necessary to first create a Linux environment and then install Docker. Given this fact, the document explains how to install Docker and run containers under Linux, as well as Windows.

## A. Install and run Docker containers under Windows ##

Because Docker relies on Linux-specific features, you can’t install it and run it natively in Windows. One approach is to install the *Docker Toolbox* application which sets up a specific Docker environment on your computer. The Toolbox installs the following set of tools which allows you to manage and run Docker containers under Windows:

- Oracle VirtualBox
- Git
- Docker Client
- Docker Machine
- Docker Kitematic

### A.1 Prerequisites ###

- Windows *Version* - your machine must be running Windows 7 or newer to run Docker Toolbox
- Windows *Virtualization* - make sure that your Windows supports Hardware Virtualization Technology and that virtualization is enabled.  
\> for Windows 8/8.1 or newer, choose Start > Task Manager and navigate to the Performance tab. Under CPU, the Virtualization setting should show “Enabled”; If virtualization is not enabled on your system, follow the manufacturer’s instructions for enabling it;  
\> for Windows 7, run the [Microsoft Hardware-Assisted Virtualization Detection Tool](http://www.microsoft.com/en-us/download/details.aspx?id=592 "Microsoft Hardware-Assisted Virtualization Detection Tool") and follow the instructions.

### A.2 Installation ###

If you already have installed the VirtualBox, there is no need to uninstall it. When prompted by the Docker Toolbox installer, indicate not to reinstall VirtualBox. If you have VirtualBox runnig, shut it down.
  
Follow these steps to install Docker Toolbox:

1. Navigate to the [Docker Toolbox](https://www.docker.com/toolbox "Docker Toolbox") page.
2. Click the installer link to download it.
3. Double-click the installer to launch the Docker Toolbox setup wizard. If the Windows security dialog prompts you to allow the program to make changes to your computer, choose Yes.
4. Follow the steps prompted by the wizard by pressing Next; when prompted with the “Select Components” screen, uncheck “VirtualBox” if you already have it installed on your computer.
5. Press Install to start the actual installation. If notified by Windows Security that the installer will make changes, make sure you allow the installer to make the necessary changes.
6. When it completes, the installer reports it was successful. Uncheck “View Shortcuts in File Explorer” and press Finish.

Launch a Docker Toolbox *terminal* by double-clicking the “Docker Quickstart Terminal” icon on your Desktop. If the system displays a User Account Control prompt to allow VirtualBox to make changes to your computer, choose Yes.
The terminal does several things to set up Docker Toolbox for you. When it is done, the terminal displays the **$** prompt where you can type *bash* commands; the terminal runs a special bash environment instead of the standard Windows command prompt, since the bash environment is required by Docker.

### A.3 Running Plone from a Docker container ###

Using the Docker Toolbox terminal, issue the following command (without the “$”):

**$** `docker run -d -p 80:80 --name eeacms_plone_container eeacms/plone`

The command creates a Docker container named “eeacms_plone_container” and starts it in background. You can verify this by issuing the following command, which displays details (such as container ID, name, status etc.) about all running containers:

**$** `docker ps`

Alternatively, you can issue the following command, which displays details about all containers, either running or stopped:

**$** `docker ps -a`

In order to access the Plone instance using the web browser, you first need to identify the IP address of the Docker environment on your computer. Issue the following command to accomplish this:

**$** `echo $DOCKER_HOST`

This should display an address which has the following format: “protocol://*IP_ADDRESS*:port” (for example “tcp://192.168.99.100:2376”). Open a web browser and enter the IP address (only *IP_ADDRESS*) in the address bar of the browser. After pressing Enter, the Plone start page should be displayed on your browser. Note that this works as long as the plone container (named “eeacms_plone_container”) is in a running state.
To stop, start and restart the “eeacms_plone_container” container, you can issue the following commands at the Docker Toolbox terminal:

- **$** `docker stop eeacms_plone_container`
- **$** `docker start eeacms_plone_container`
- **$** `docker restart eeacms_plone_container`

