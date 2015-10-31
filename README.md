# Site-Alerter #
Uses the Pushbullet platform to alert you through your selected devices when the selected site goes down.
## Configuration ##
Rename example.config.yaml to config.yaml. Fill out all of the fields.
## Dependencies  ##
```pip install pyyaml```  
```pip install enum34```
## Usage ##
```python main.py --list``` to view device id and identities.  
```python main.py --add <device_id_here>``` to add the the selected device_id to your config.  
```python main.py``` to run program.
