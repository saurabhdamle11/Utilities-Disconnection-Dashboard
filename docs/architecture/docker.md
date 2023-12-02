# Working with Docker
## This documentation is outdated and needs to be reworked in the future
Open the Web Shell of the 'disconnection_dashboard_ui' instance in JetStream or you can do a ssh by `ssh exouser@149.165.154.35` and enter the password which can be found under Credentails->Passphrase in the JetStream instance or you can save your public key in authorized_keys of the instance.

Then go to the "Utility_Disconnection_Dashboard_App" folder by the command `cd disconnection_dashboard/Utility_Disconnection_Dashboard_App/`

List the currently running Docker containers by the command: `docker container ls`

Note the "CONTAINER ID" of the "dashboard" container. This usually will be on the top of the list. In the below steps, replace <CONTAINER ID> with the Container ID of the dashboard container.
	
Stop the running Docker container by `docker stop <CONTAINER ID>` command. After you execute this command, the application will be down. This commands takes some time to process (usually around 1-2 munites), after this command is sucessfully executed, the CONTAINER ID will be printed on the next line and the command prompt is ready to interact again. 
	
Once the interactive shell is ready, we need to remove the container by the command `docker rm <CONTAINER ID>`. This step will be executed immediately and the container id will be printed on new line.
	
We have stopped the container, now we need to remove the image on which the container was built. In order to remove the image, we need to get the IMAGE ID of the 'dashboard' image by the command `docker images`. Note the IMAGE ID of the 'dashboard' Repository, usually it is on the top. In the below steps, replace <IMAGE ID> with the Image ID of the dashboard image.
	
Now we need to remove the image from Docker, which can be done by the command `docker rmi <IMAGE ID>`. This will print "Untagged: dashboard:latest" on next line denoting the image is deleted successfully and a few lines saying 'Deleted: Sha256: xxxxx'.
	
Now for pulling the code changes from the GitHub Repo, we need to pull the fresh code from the repo. To do that, we need to execute `git pull` command. Once we execute this step, it will prompt for IU GitHub username, enter the username (Be sure you add '@iu.edu' in username) and hit enter. Next it will prompt for password, enter the IU GitHub Password. (Remember the password you type is not displayed in the screen nor does the cursor move, but it is still receiving what ever you are typing) and hit enter.
	
After successful authentication and permissions, the system will pull the changes and merge with the current code in Jetstream. It will show in short the additions and removal of lines of code denoted by a '+' and a '-' sign for modified files.

Now we have fresh code changes in the JetStream instance. We need to rebuild the docker image, and run the container for the application to be up again.

To build the Docker image, execute the command: `docker build -t dashboard .` it creates a docker image with tag dashboard.
	
Now we need to run this image and a container will be created and running by default. We can do this by the command : `docker run -i -p 80:80 -d dashboard` 
