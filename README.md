[FRANCAIS](README_FR.md)

# Full Automation Lights

## Introduction

Are you tired of getting up from your comfortable bed to check if you turned off the living room light? Are you annoyed by finding the bathroom light on all night? Are you disturbed by bright hallway lights in the middle of the night when you have to use the bathroom? Don't worry! With this magic (but not too much) script, you can automate all of this in no time!

This AppDaemon-based script works with Home Assistant. It's designed to automatically control your home lighting based on different criteria such as brightness and sun elevation. No need to worry about commands, your home will take care of everything! And it's open-source, so you can improve it as you like or adapt it to your needs.

Don't hesitate any longer and install it to live in a perfectly lit home! And if you encounter any problems, don't hesitate to consult our documentation, it's there for that!

## Features

- Room Occupancy: The script uses occupancy sensors to detect the presence of people in a room and adjusts the lighting accordingly. It is possible to set brightness limits and hysteresis for each room. There is also an option to turn off lights automatically if the natural light in the room is high.
- Natural Light: The script uses the position of the sun to automatically adjust the brightness and color temperature of the lights based on the sun's elevation. It is possible to set different natural light modes for each room.
- Scenes: The script allows for automatically triggering scenes based on the state of a specific trigger, such as the turning on of a TV. It is possible to set different scenes for each room.
- Configuration for multiple rooms: it is possible to configure multiple rooms with different options for lighting automation and scenes. There is a configuration for the living room and another for the kitchen in the provided example.
- Advanced Configuration: The script offers great configuration flexibility for experienced users, allowing for setting parameters such as brightness limits, natural light modes, scenes, and occupancy sensors for each room in the house.

## Prerequisites

- Home Assistant: A functional installation of Home Assistant is required to use this script.
- AppDaemon: AppDaemon is an add-on for Home Assistant that allows you to run Python scripts in the background. AppDaemon must be installed and configured to use this script.

## Installation

Once you have Home Assistant and AppDaemon running, you can install this application by following these steps:

1) Download the FullAutomationLights.py file and place it in the "apps" directory of AppDaemon.
2) Add the following configuration to your apps.yaml file. This file is usually located in the "apps" directory of AppDaemon.

## Configuration

Example of minimum configuration to turn on and off the light "light.living_room" in the room "living_room" when a motion is detected with the sensor "binary_sensor.living_room_motion". "light.living_room" is turned on with a simple "turn_on" without any parameters :

```yaml
FullAutomationLights:
  module: FullAutomationLights
  class: FullAutomationLights
  rooms:
    living_room:
      occupancy_entity: binary_sensor.living_room_motion
      lights_entity: light.living_room
```
---

Example of a configuration with the natural light feature. Here, "natural_lighting" is set to turn on the feature. By default, a natural light "mode" named "default" is created. In the "living_room" room, the "light.living_room" is linked to this mode :

```yaml
FullAutomationLights:
  module: FullAutomationLights
  class: FullAutomationLights
  natural_lighting:
  rooms:
    living_room:
      occupancy_entity: binary_sensor.living_room_motion
      lights_entity: light.living_room
      natural_lighting:
        - name: default
          lights_entity: light.living_room
```
---
The following advanced configuration sets the transitions between scenes and natural lighting with a transition time of 5 seconds for scenes and 30 seconds for natural lighting.

Natural lighting is configured with different parameters such as the entity associated with the sun, the limits of the elevation angle for brightness and temperature in Kelvin, as well as the "nl1" and "nl2" modes defined with their own range of brightness and temperature in Kelvin.

Then, the configuration defines the rooms "living_room" and "kitchen". For each room, it defines the entities associated with presence, luminance, luminance limit, and lights. It also defines the natural lighting modes and the scenes associated with these rooms. For example, for "living_room", it defines the scenes associated with ambient lighting for TV and TV on. In both rooms, different light groups are associated with the two natural lighting configurations "nl1" and "nl2".

"boost_brightness_pct" is used in the "natural_lighting" settings of "living_room". It represents the boost percentage of brightness for a specific light. The "nl1" mode has a brightness boost of -30%. This means that the brightness will be reduced by 30% for the lights specified in the "lights_entity" (light.living_room_group_1).

"high_luminance_off_light" is also set to "true" in "living_room". This means that, unlike in "kitchen", if the luminance captured by "sensor.living_room_luminance" is above 50 + 5, the light will turn off. Since this feature is not used in "kitchen", "luminance_hysteresis" is not defined and is therefore equal to its default value, which is 0.

```yaml
FullAutomationLights:
  module: FullAutomationLights
  class: FullAutomationLights
  debug: true
  transitions:
    scenes: 5
    natural_lighting: 30
  natural_lighting:
    sun_entity: sun.sun
    min_elevation_for_brightness: -20
    max_elevation_for_brightness: 20
    min_elevation_for_kelvin: 0
    max_elevation_for_kelvin: 20
    modes:
      - name: nl1
        max_brightness: 255
        min_brightness: 100
        max_kelvin: 5500
        min_kelvin: 2000
      - name: nl2
        max_brightness: 255
        min_brightness: 100
        max_kelvin: 5500
        min_kelvin: 2700
  rooms:
    living_room:
      occupancy_entity: binary_sensor.living_room_motion
      luminance_entity: sensor.living_room_luminance
      luminance_limit: 50
      luminance_hysteresis: 5
      hight_luminance_off_light: true
      lights_entity: light.living_room
      natural_lighting:
        - name: nl1
          lights_entity: light.living_room_group_1
          boost_brightness_pct: -30
        - name: nl2
          lights_entity: light.living_room_group_2
      scenes:
        - scene_entity: scene.living_room_ambilight
          scene_trigger: switch.android_tv_ambilight_hue
          scene_trigger_value: "on"
        - scene_entity: scene.living_room_tv
          scene_trigger: media_player.android_tv
          scene_trigger_value: "on"
    kitchen:
      occupancy_entity: binary_sensor.kitchen_motion
      luminance_entity: sensor.kitchen_illuminance
      luminance_limit: 35
      lights_entity: light.kitchen
      natural_lighting:
        - name: nl1
          lights_entity: light.kitchen_spots
        - name: nl2
          lights_entity: light.table
```

### The FullAutomationLights configuration includes the following settings :

- `module:` et `class:` These parameters tell AppDaemon where to find the FullAutomationLights.py file and which class to use to start the application.
- `debug:` (Optional) [boolean] This option enables or disables the debugging messages from the application. It is recommended to set it to "true" during the first installation to check that everything is working correctly. The debug function is chatty and slows down the script. For production, it is best to deactivate it. Default: false
- `transitions:` (Optional) This section allows for defining custom transitions.
	- `init:` (Optional) [integer] duration of the transition in seconds when the script is initialized. Default: 0
	- `occupancy:` (Optional) [integer] duration of the transition in seconds when changing state due to the "occupancy_entity" sensor. Default: 1
	- `low_light:` (Optional) [integer] Duration of the transition in seconds when changing state due to the "luminance_entity" sensor. Default: 15
	- `scenes:` (Optional) [integer] duration of the transition in seconds when changing the scene. Default: 5
	- `natural_lighting:` (Optionel) [integer] duration of the transition in seconds when changing the natural lighting. Default: 10
	- `off:` (Optional) [integer] duration of the transition in seconds when turning off the lights. Default: 3
- `natural_lighting:` (Optionel) This section allows configuring natural light management. It includes several sub-parameters.
	- `sun_entity:` (Optional) [string] Sun entity from Home Assistant is used to determine the sun elevation. Default: sun.sun
	- `min_elevation_for_brightness:` et `max_elevation_for_brightness:` : (Optional) [integer] These parameters determine the range of sun elevation in degrees during which the brightness of the lights is adjusted. Default: -20 and 20
	- `min_elevation_for_kelvin:` et `max_elevation_for_kelvin:` : (Optional) [integer] These parameters determine the range of sun elevation in degrees during which the color temperature of the lights is adjusted. Default: 0 and 20
	- `modes:` (Optional) This section allows for defining natural light modes for different ranges of sun elevation. Each mode can have the following parameters:
    	- `name:` The name of the mode. This name is used to link lights to a mode in the room configuration.
    	- `max_brightness:` et `min_brightness:` (Optional) [integer] The brightness limits for this mode. Default: 255 and 100
    	- `max_kelvin:` et `min_kelvin:` (Optional) [integer] The color temperature limits for this mode. Default: 5500 and 2000
- `rooms:` This section allows specifying the parameters for each room in the house.
	- `name of the room:`
		- `occupancy_entity:` [string] The entity used to detect occupancy in the room. This can be a motion sensor, switch, etc.
		- `luminance_entity:` (Optional) [string] Entity used to measure the room's luminosity.
		- `luminance_limit:` (Optional) [integer] The brightness threshold below which the room lights will automatically turn on. Default: 10
		- `luminance_hysteresis:` (Optional) [integer] Value used to define a range of luminance around `luminance_limit`, within which the lights in the room will be automatically turned on or off. Default: 0
		- `hight_luminance_off_light:` (Optional) [boolean] Value is used to define if the room lights should be automatically turned off in case of high luminosity (greater than `luminance_limit` + `luminance_hysteresis`). Default: false
		- `lights_entity:` [string] Light entity used to control the lights in the room. It can be a group of lights or an individual light.
		- `natural_lighting:` (Optional) This section allows you to specify the natural lighting parameters for each room. You can specify different lighting modes `name:` with different brightness and color temperature parameters. You can also specify individual light entities for each lighting mode.
    		- `name:` (Optional) [string] Name of the natural lighting that is desired to be used. It is possible to define several different names based on the user's needs, for example "primary" and "secondary".
    		- `lights_entity:` (Optionel) [string] Entities that will be controlled based on the sun elevation.
    		- `boost_brightness_pct:` (Optionel) [integer] This setting allows you to increase or decrease the brightness of the lighting by percentage.
		- `scenes:` (Optional) Scenes are triggered when an event is triggered. For example, specific lighting when the TV is turned on.
    		- `scene_entity:` [string] Scene that we want to activate. This entity can be a scene or a script.
    		- `scene_trigger:` [string] The entity that triggers the activation of the scene defined in `scene_entity`. This entity can be a switch, sensor, TV or any other item that can send a specific value.
    		- `scene_trigger_value:` [] The value that `scene_trigger` must take for the scene defined in `scene_entity` to be activated. For example, if `scene_trigger_value` is set to "on", the scene will only be activated when `scene_trigger` switches to the "on" state.
        
It is possible to define multiple scenes for each room by adding multiple "scenes" blocks in the configuration.
Example:
        
```yaml
scenes:
 - scene_entity: scene.ambilight
   scene_trigger: switch.android_tv_ambilight_hue
   scene_trigger_value: "on"
 - scene_entity: scene.tv
   scene_trigger: media_player.android_tv
   scene_trigger_value: "on"
```
        
It means:
If the switch "android_tv_ambilight_hue" is turned on, the scene "salon_ambilight" is triggered.
If the media player "android_tv" is turned on, the scene "salon_tv" is triggered.

Note that the scenes are in a priority order. If both "triggers" are active, "scene.salon_ambilight" will be triggered.

## Order of operations

- Presence in the room?
- Yes
	- Low luminance?
	- Yes
		- Scene configured and active?
		- Yes
			- Launch the active scene
		- No
			- Natural lighting configured?
			- Yes
				- Turn on light based on natural light and adjust while it is on
			- No
				- Simply turn on the light
	- No
		- Turn off if high_luminance_off_light = true
- No
	- Turn off

## Future improvement possibilities

- Clean up of the code and improvement of performance

## Remerciements

- Thank you to @github/jlpouffier for introducing me to Appdaemon through his YouTube channel (https://www.youtube.com/@HorizonDomotique).
- Thank you to ChatGPT for their valuable assistance in writing the documentation and translating it into English.
- Thank you to my partner for proofreading this documentation.
