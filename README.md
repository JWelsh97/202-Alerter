# Site-Alerter
Uses the Pushbullet platform to alert you through your selected devices when the selected site goes down.
## Configuration
Rename example.config.yaml to config.yaml. Fill out all of the fields.
## Dependencies
<code>pip install pyyaml</code><br />
<code>pip install enum34</code>
## Usage
<code>python main.py --list</code> to view device id and identities.<br />
<code>python main.py --add \<device_id_here></code> to add the device id to your config<br />
<code>python main.py</code> to run program.

