# New Allsky Repository

This repo contains my supporting code and small changes to teh Team Allsky allsky-camera software.

* I've altered `upload.sh` because i have a target structure into which i want to push the images, keograms, startrails and timelapses.

* I've also added code to upload the timelapse to youtube. This should be added to cron so that it first runs about an hour before dawn. It will monitor the log and once the timelapse has been created, it'll upload it to Youtube and update the cron entry. 

* I also have a script to monitor the allsky process and reboot the pi if it stalls.
