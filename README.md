# Site-Alerter #
Uses the Pushbullet platform to alert you through your selected devices when the selected site goes down. Used with a Task Scheduler like cron.
## Configuration ##
Rename example.config.yaml to config.yaml. Fill out all of the fields.
## Dependencies  ##
`pip install pyyaml`  
`pip install enum34`

## Usage ##
`python main.py args`  
`python main.py` will run the program.

## Arguments ##
**-l**  
**--list-devices**  
Prints the list of devices on your Pushbullet account  
[device_id] device_name: device_identity  

**-a**  
**--add-device** *device_id*  
Adds the selected device_id (found using -l/--list-devices argument) to your configuration.  

**-r**  
**--remove-device** *device_id*  
Removes the selected device_id (found using -l/--list-devices argument) from your configuration.  

**-t**
**--test**
Sends a test push to each device in the configuration.  
