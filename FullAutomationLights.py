import appdaemon.plugins.hass.hassapi as hass

#
# Light
# @gnol86
# https://github.com/Gnol86/FullAutomationLights
#

class FullAutomationLights(hass.Hass):

    def initialize(self):
        self.debug = self.args['debug'] if 'debug' in self.args else False
        self.error = ""
        self.log("#--------------------------#")
        self.log("|  Full Automation Lights  |")
        self.log("#--------------------------#")
        self.log("")

        self.natural_lighting = self.init_natural_lighting()
        self.transitions = self.init_transitions()
        self.rooms = self.init_rooms()
        
        if self.error == "":
            for room_name in self.rooms:
                self.set_light(room_name, "init")
            self.log("Initialized")
        self.stop()

    def set_light(self, room_name, trigger):
        transition = self.transitions[trigger] if trigger in self.transitions else 1
        self.debug_log(f"{room_name} : {trigger}")
        if self.rooms[room_name]['is_light_on']:
            mode = ""
            if len(self.rooms[room_name]['scenes']) > 0:
                for scene in self.rooms[room_name]['scenes']:
                    if self.get_state(scene['scene_trigger']) == scene['scene_trigger_value']:
                        mode = "scene"
                        entity = self.get_entity(scene['scene_entity'])
                        domaine = scene['scene_entity'].split('.')[0]
                        match domaine:
                            case "script":
                                entity.call_service("turn_on")
                            case _:
                                entity.call_service("turn_on", transition = transition)
                        self.debug_log(f"ON - Scene : {scene['scene_entity']}")
                        break
            if mode == "" and self.natural_lighting and len(self.rooms[room_name]['natural_lighting']) > 0:
                for natural_lighting in self.rooms[room_name]['natural_lighting']:
                    mode = 'natural_lighting'
                    brightness = self.natural_lighting['modes'][natural_lighting['name']]['brightness']
                    kelvin = self.natural_lighting['modes'][natural_lighting['name']]['kelvin']
                    entity = self.get_entity(natural_lighting['lights_entity'])
                    if natural_lighting['boost_brightness_pct'] != 0:
                        brightness=int(brightness+(brightness/100*natural_lighting['boost_brightness_pct']))
                        if brightness > 255: brightness=255
                        elif brightness < 1: brightness=1
                    entity.call_service("turn_on", brightness = brightness, kelvin = kelvin, transition = transition)
                self.debug_log("ON - Natural lighting")
            if mode == "":
                entity = self.get_entity(self.rooms[room_name]['lights_entity'])
                entity.call_service("turn_on", transition = transition)
                self.debug_log("ON")
        else:
            self.debug_log("OFF")
            entity = self.get_entity(self.rooms[room_name]['lights_entity'])
            entity.call_service("turn_off", transition = self.transitions['off'])
        self.debug_log("")

    def init_rooms(self):
        self.debug_log("Init Rooms...")
        if 'rooms' in self.args:
            rooms = {}
            for name in self.args['rooms']:
                self.debug_log(name)
                rooms[name] = {}
                rooms[name]['occupancy_entity'] = self.args['rooms'][name]['occupancy_entity'] if 'occupancy_entity' in self.args['rooms'][name] else False
                rooms[name]['lights_entity'] = self.args['rooms'][name]['lights_entity'] if 'lights_entity' in self.args['rooms'][name] else False
                if not rooms[name]['occupancy_entity'] or not rooms[name]['lights_entity']:
                    self.error = f"!!! 'occupancy_entity' and 'lights_entity' are required in the '{name}' configuration in 'rooms' in 'apps.yaml' !!!"
                    break
                else:
                    self.debug_log(f"occupancy_entity : {rooms[name]['occupancy_entity']}")
                    self.debug_log(f"lights_entity : {rooms[name]['lights_entity']}")
                    rooms[name]['occupancy_off_delay'] = self.args['rooms'][name]['occupancy_off_delay'] if 'occupancy_off_delay' in self.args['rooms'][name] else 0
                    self.debug_log(f"occupancy_off_delay : {rooms[name]['occupancy_off_delay']}")
                    rooms[name]['luminance_entity'] = self.args['rooms'][name]['luminance_entity'] if 'luminance_entity' in self.args['rooms'][name] else False
                    if rooms[name]['luminance_entity']:
                        self.debug_log(f"luminance_entity : {rooms[name]['luminance_entity']}")
                        rooms[name]['luminance_limit'] = self.args['rooms'][name]['luminance_limit'] if 'luminance_limit' in self.args['rooms'][name] else 10
                        self.debug_log(f"luminance_limit : {rooms[name]['luminance_limit']}")
                        rooms[name]['luminance_hysteresis'] = self.args['rooms'][name]['luminance_hysteresis'] if 'luminance_hysteresis' in self.args['rooms'][name] else 0
                        self.debug_log(f"luminance_hysteresis : {rooms[name]['luminance_hysteresis']}")
                        rooms[name]['hight_luminance_off_light'] = self.args['rooms'][name]['hight_luminance_off_light'] if 'hight_luminance_off_light' in self.args['rooms'][name] else False
                        self.debug_log(f"hight_luminance_off_light : {rooms[name]['hight_luminance_off_light']}")
                    rooms[name]['natural_lighting'] = self.args['rooms'][name]['natural_lighting'] if 'natural_lighting' in self.args['rooms'][name] else {}
                    if type(rooms[name]['natural_lighting']) == list:
                        if len(rooms[name]['natural_lighting']) > 0:
                            self.debug_log("Natural lighting :")
                            for natural_lighting in rooms[name]['natural_lighting']:
                                if not 'boost_brightness_pct' in natural_lighting: natural_lighting['boost_brightness_pct'] = 0
                                if not natural_lighting['name'] in self.natural_lighting['modes']:
                                    self.debug_log(f"  ! '{natural_lighting['name']}' does not exist in the 'natural_lighting' configuration")
                                    self.debug_log("  ! It is replaced by 'default'")
                                    natural_lighting['name'] = 'default'
                                self.debug_log(f"  {natural_lighting['name']} : {natural_lighting['lights_entity']} ({natural_lighting['boost_brightness_pct']})")
                    
                    rooms[name]['scenes'] = self.args['rooms'][name]['scenes'] if 'scenes' in self.args['rooms'][name] else {}
                    if type(rooms[name]['scenes']) == list:
                        if len(rooms[name]['scenes']) > 0:
                            self.debug_log("Scenes :")
                            for scene in rooms[name]['scenes']:
                                self.debug_log(f"  {scene['scene_entity']}")
                                self.debug_log(f"  if {scene['scene_trigger']} = {scene['scene_trigger_value']}")
                    self.debug_log("")
                    rooms[name]['occupancy'] = True if self.get_state(rooms[name]['occupancy_entity']) in ["on","home",True,"true","True"] else False
                    self.debug_log(f"Occupancy : {rooms[name]['occupancy']}")
                    if rooms[name]['luminance_entity']:
                        rooms[name]['low_light'] = True if self.int(self.get_state(rooms[name]['luminance_entity'])) <= rooms[name]['luminance_limit'] else False
                        self.debug_log(f"Low light : {rooms[name]['low_light']}")
                    else: rooms[name]['low_light'] = True
                    rooms[name]['is_light_on'] = rooms[name]['occupancy'] and rooms[name]['low_light']
                    self.debug_log(f"Light is ON : {rooms[name]['is_light_on']}")
                    
                    if rooms[name]['occupancy_off_delay'] > 0:
                        self.listen_state(self.set_is_light_on, rooms[name]['occupancy_entity'], new="on", room_name=name, trigger="occupancy")
                        self.listen_state(self.set_is_light_on, rooms[name]['occupancy_entity'], new="off", duration = rooms[name]['occupancy_off_delay'], room_name=name, trigger="occupancy")
                    else:
                        self.listen_state(self.set_is_light_on, rooms[name]['occupancy_entity'], room_name=name, trigger="occupancy")
                    if rooms[name]['luminance_entity']:
                        self.listen_state(self.set_is_light_on, rooms[name]['luminance_entity'], room_name=name, trigger="low_light")
                    for scene in rooms[name]['scenes']:
                        self.listen_state(self.set_is_light_on, scene['scene_trigger'], new=scene['scene_trigger_value'], room_name=name, trigger="scene")
                        self.listen_state(self.set_is_light_on, scene['scene_trigger'], old=scene['scene_trigger_value'], room_name=name, trigger="scene")
                self.debug_log("---")
            self.debug_log("Rooms Initialized")
            self.debug_log("")
            return rooms
        else:
            self.error = "!!! No configured room, check the 'apps.yaml' file !!!"
            return False

    def set_is_light_on(self, entity, attribute, old, new, kwargs):
        if kwargs['trigger'] == 'occupancy':
            self.rooms[kwargs['room_name']]['occupancy'] = True if new in ["on","home",True,"true","True"] else False
        if kwargs['trigger'] == 'low_light':
            luminance_limit = self.int(self.rooms[kwargs['room_name']]['luminance_limit'])
            if self.rooms[kwargs['room_name']]['low_light']:
                luminance_limit += self.int(self.rooms[kwargs['room_name']]['luminance_hysteresis'])
            else:
                luminance_limit -= self.int(self.rooms[kwargs['room_name']]['luminance_hysteresis'])
            self.rooms[kwargs['room_name']]['low_light'] = True if self.int(new) <= luminance_limit else False
        old_is_light_on = self.rooms[kwargs['room_name']]['is_light_on']
        if not (self.rooms[kwargs['room_name']]['is_light_on'] and not self.rooms[kwargs['room_name']]['low_light']) or self.rooms[kwargs['room_name']]['hight_luminance_off_light'] or kwargs['trigger'] == 'occupancy':
            self.rooms[kwargs['room_name']]['is_light_on'] = self.rooms[kwargs['room_name']]['occupancy'] and self.rooms[kwargs['room_name']]['low_light']
        
        if kwargs['trigger'] in ["init", "scene", "natural_lighting"] or old_is_light_on != self.rooms[kwargs['room_name']]['is_light_on']:
            self.set_light(kwargs['room_name'], kwargs['trigger'])

    def init_transitions(self):
        self.debug_log("Init Transitions...")
        transitions = self.args['transitions'] if 'transitions' in self.args else {}
        if not 'init' in transitions: transitions['init'] = 0
        if not 'occupancy' in transitions: transitions['occupancy'] = 1
        if not 'low_light' in transitions: transitions['low_light'] = 15
        if not 'scenes' in transitions: transitions['scenes'] = 5
        if not 'natural_lighting' in transitions: transitions['natural_lighting'] = 10
        if not 'off' in transitions: transitions['off'] = 3
        self.debug_log("Transitions Initialized")
        self.debug_log("")
        return transitions

    def init_natural_lighting(self):
        if 'natural_lighting' in self.args:
            self.debug_log("Init Natural Lighting...")
            natural_lighting = {
                'modes': {
                    'default': {
                        'max_brightness' : 255,
                        'min_brightness' : 100,
                        'max_kelvin' : 5500,
                        'min_kelvin' : 2000,
                        'brightness' : 0,
                        'kelvin' : 0,
                    }
                },
                'sun_entity' : 'sun.sun',
                'min_elevation_for_brightness' : -20,
                'max_elevation_for_brightness' : 20,
                'min_elevation_for_kelvin' : 0,
                'max_elevation_for_kelvin' : 20
                }
            if type(self.args['natural_lighting']) == dict:
                if 'modes' in self.args['natural_lighting']:
                    if type(self.args['natural_lighting']['modes']) == list:
                        for mode in self.args['natural_lighting']['modes']:
                            natural_lighting['modes'][mode['name']] = natural_lighting['modes']['default'].copy()
                            if 'max_brightness' in mode: natural_lighting['modes'][mode['name']]['max_brightness'] = mode['max_brightness']
                            if 'min_brightness' in mode: natural_lighting['modes'][mode['name']]['min_brightness'] = mode['min_brightness']
                            if 'max_kelvin' in mode: natural_lighting['modes'][mode['name']]['max_kelvin'] = mode['max_kelvin']
                            if 'min_kelvin' in mode: natural_lighting['modes'][mode['name']]['min_kelvin'] = mode['min_kelvin']

                if 'sun_entity' in self.args['natural_lighting']: natural_lighting['sun_entity'] = self.args['natural_lighting']['sun_entity']
                if 'min_elevation_for_brightness' in self.args['natural_lighting']: natural_lighting['min_elevation_for_brightness'] = self.args['natural_lighting']['min_elevation_for_brightness']
                if 'max_elevation_for_brightness' in self.args['natural_lighting']: natural_lighting['max_elevation_for_brightness'] = self.args['natural_lighting']['max_elevation_for_brightness']
                if 'min_elevation_for_kelvin' in self.args['natural_lighting']: natural_lighting['min_elevation_for_kelvin'] = self.args['natural_lighting']['min_elevation_for_kelvin']
                if 'max_elevation_for_kelvin' in self.args['natural_lighting']: natural_lighting['max_elevation_for_kelvin'] = self.args['natural_lighting']['max_elevation_for_kelvin']
            
            natural_lighting['sun_elevation'] = self.int(self.get_state(natural_lighting['sun_entity'], attribute='elevation'))
            self.listen_state(self.callback_sun_elevation, natural_lighting['sun_entity'], attribute='elevation')
            self.debug_log(f"Listen state of {natural_lighting['sun_entity']}")
            natural_lighting = self.set_natural_lighting(natural_lighting)
            self.debug_log("Natural Lighting Initialized")
            self.debug_log("")
            return natural_lighting
        else:
            self.debug_log("Natural Lighting Inactive")
            self.debug_log("")
            return False

    def callback_sun_elevation(self, entity, attribute, old, new, kwargs):
        self.natural_lighting['sun_elevation'] = self.int(new)
        self.natural_lighting = self.set_natural_lighting(self.natural_lighting)
        for room_name in self.rooms:
            if self.rooms[room_name]['natural_lighting'] and self.rooms[room_name]['is_light_on']:
                self.set_light(room_name, "natural_lighting")
        
    def set_natural_lighting(self, natural_lighting):
        self.debug_log("---")
        self.debug_log(f"Sun elevation : {natural_lighting['sun_elevation']}")
        for name in natural_lighting['modes']:
            natural_lighting['modes'][name]['brightness'] = self.scale(
                natural_lighting['sun_elevation'],
                (natural_lighting['min_elevation_for_brightness'], natural_lighting['max_elevation_for_brightness']),
                (natural_lighting['modes'][name]['min_brightness'], natural_lighting['modes'][name]['max_brightness'])
                )
            natural_lighting['modes'][name]['kelvin'] = self.scale(
                natural_lighting['sun_elevation'],
                (natural_lighting['min_elevation_for_kelvin'], natural_lighting['max_elevation_for_kelvin']),
                (natural_lighting['modes'][name]['min_kelvin'], natural_lighting['modes'][name]['max_kelvin'])
                )
            self.debug_log(f"{name} - brightness : {natural_lighting['modes'][name]['brightness']} - kelvin : {natural_lighting['modes'][name]['kelvin']}")
        self.debug_log("---")
        return natural_lighting

    def scale(self, val, src, dst):
        if val < src[0]: val = src[0]
        if val > src[1]: val = src[1]
        return self.int(((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0])

    def int(self, val):
        if type(val) == str or type(val) == float:
            return int(float(val))
        return val

    def debug_log(self, message):
        if self.debug: self.log(message)
    
    def stop(self):
        if self.error != "":
            self.log(self.error)
            self.stop_app(self.name)
