<div align="right"><a href="https://www.buymeacoffee.com/gnol86" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a></div>

# Full Automation Lights

## Présentation

Vous en avez marre de vous lever après vous être confortablement installer dans votre lit car vous vous demandez si vous avez bien éteint la lumière du salon ? Vous en avez assez de remarquer le matin que la lumière de la salle de bain est restée allumée toute la nuit ? Cela vous aggace être ébloui par une lumière trop forte dans le couloir en pleine nuit lorsque vous allez faire vos besoins naturels. Ne vous inquiétez plus ! Grace à ce script magique (mais pas trop quand même), vous allez pouvoir automatiser tout cela en un rien de temps !

Ce script basé sur AppDaemon fonctionne avec Home Assistant. Il est conçu pour contrôler automatiquement l'éclairage de votre maison en fonction de différents critères tels la luminosité et l'élévation du soleil. Plus besoin de se prendre la tête avec des commandes, votre maison s'occupe de tout ! Et en plus, c'est open-source, vous pourrez donc l'améliorer à votre guise ou l'adapter à vos besoins.

N'hésitez plus et installez-le pour vivre dans une maison éclairée à la perfection ! Et si jamais vous rencontrez des problèmes, n'hésitez pas à consulter notre documentation, elle est faite pour ça !

## Fonctionnalités

- Occupation de la pièce: Le script utilise des capteurs d'occupation pour détecter la présence de personnes dans une pièce et ajuste en conséquence l'éclairage. Il est possible de définir des limites de luminosité et un hystérésis pour chaque pièce. Il y a également une option pour éteindre les lumières automatiquement si la luminosité naturelle dans la pièce est élevée.
- Lumière naturelle: Le script utilise la position du soleil pour ajuster automatiquement la luminosité et la température de couleur des lumières en fonction de l'élévation du soleil. Il est possible de définir différents modes de lumière naturelle pour chaque pièce.
- Scènes: Le script permet de déclencher automatiquement des scènes en fonction de l'état d'un déclencheur spécifique, comme par exemple l'allumage d'un téléviseur. Il est possible de définir différentes scènes pour chaque pièce.
- Configuration pour plusieurs pièces: il est possible de configurer plusieurs pièces avec différentes options pour l'automatisation de la lumière et les scènes. Il y a une configuration pour le salon et une autre pour la cuisine dans l'exemple fourni.
- Configurations avancées: Le script offre une grande flexibilité de configuration pour les utilisateurs expérimentés, permettant de définir des paramètres tels que les limites de luminosité, les modes de lumière naturelle, les scènes et les capteurs d'occupation pour chaque pièce de la maison.

## Prérequis

- Home Assistant : Il est nécessaire d'avoir une installation fonctionnelle de Home Assistant pour utiliser ce script.
- AppDaemon : AppDaemon est un add-on pour Home Assistant qui permet d'exécuter des scripts Python en arrière-plan. Il est nécessaire d'installer et de configurer AppDaemon pour utiliser ce script.

## Installation

Une fois que vous avez Home Assistant et AppDaemon en cours d'exécution, vous pouvez installer cette application en suivant les étapes suivantes:

1. Téléchargez le fichier FullAutomationLights.py et placez-le dans le répertoire "apps" d'AppDaemon.
2. Ajoutez la configuration suivante à votre fichier apps.yaml. Ce fichier se trouve généralement dans le répertoire "apps" d'AppDaemon.

## Configuration

Exemple de configuration minimale pour allumer et éteindre la lumière “light.living_room” dans la pièce “living_room” lorsqu’un mouvement est détecté avec le capteur “binary_sensor.living_room_motion”. "light.living_room" est allumé avec un simple “turn_on” sans paramètre. :

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

Le même exemple de configuration avec la fonction lumière naturelle. Ici ‘natural_lighting’ est défini pour activer la fonctionnalité. Par défaut, un “mode” de lumière naturelle nommé “default” est créé. Dans pièce “living_room”, la lumière “light.living_room” est lié à ce mode :

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
La configuration avancée suivante définit les transitions entre les scènes et l'éclairage naturel avec un temps de transition de 5 secondes pour les scènes et 30 secondes pour l'éclairage naturel.

L'éclairage naturel est configuré avec différents paramètres tels que l'entité associée au soleil, les limites de l'angle d'élévation pour la luminosité et la température en Kelvin, ainsi que les modes "nl1" et "nl2" définis avec leur propre plage de luminosité et de température en Kelvin.

Ensuite, la configuration définit les pièces "living_room" et "kitchen". Pour chaque pièce, il définit les entités associées à la présence, à la luminance, à la limite de luminance et aux lumières. Il définit également les modes d'éclairage naturel et les scènes associées à ces pièces. Par exemple, pour "living_room", il définit les scènes associées à un éclairage ambiant pour la TV et la TV en marche. Dans les deux pièces, des groupes de lumières differentes sont assossiées aux deux configuration de lumières naturelles "nl1" et "nl2".

"boost_brightness_pct" est utilisé dans les paramètres de "natural_lighting" de "living_room". Il représente le pourcentage de boost de luminosité pour une lumière spécifique. Le mode "nl1" a un boost de luminosité de -30%. Cela signifie que la luminosité sera réduite de 30% pour les lumières spécifiées dans l'entité "lights_entity" (light.living_room_group_1).

"hight_luminance_off_light" est également défini à "true" dans "living_room". Cela signifie que, contrairement à "kitchen", si la luminosité captée par "sensor.living_room_luminance" est supérieur à 50 + 5, la lumière s'éteindra. Vu que cette fonctionnalité n'est pas utilisée dans "kitchen", "luminance_hysteresis" n'est pas défini et est donc égal à sa valeur par défaut, à savoir 0.

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
          scene_trigger_entity: switch.android_tv_ambilight_hue
          scene_trigger_value: "on"
        - scene_entity: scene.living_room_tv
          scene_trigger_entity: media_player.android_tv
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

### La configuration de FullAutomationLights comprend les paramètres suivants :

- `module:` et `class:` Ces paramètres indiquent à AppDaemon où trouver le fichier FullAutomationLights.py et quelle classe utiliser pour démarrer l'application.
- `debug:` (Optionel) [boolean] Cette option permet d'activer ou de désactiver les messages de débogage de l'application. Il est conseillé de la mettre à "true" lors de la première installation pour vérifier que tout fonctionne correctement. La fonction débug est bavarde et ralenti le script. Pour la mise en production, il est préférable de la désactiver. Défaut : false
- `transitions:` (Optionel) Cette section permet de définir des transitions personalisées.
	- `init:` (Optionel) [integer] durée de la transition en secondes lors de l’initialisation du script. Défaut : None
	- `occupancy:` (Optionel) [integer] durée de la transition en secondes lors du changement d’état dû au capteur “occupancy_entity”. Défaut : None
	- `low_light:` (Optionel) [integer] durée de la transition en secondes lors du changement d’état dû au capteur “luminance_entity”. Défaut : 15
	- `scenes:` (Optionel) [integer] durée de la transition en secondes lors du changement de scène. Défaut : 5
	- `natural_lighting:` (Optionel) [integer] durée de la transition en secondes lors du changement de la lumière naturelle. Défaut : 10
	- `off:` (Optionel) [integer] durée de la transition en secondes lors de l’extinction des lampes. Défaut : 3
- `natural_lighting:` (Optionel) Cette section permet de configurer la gestion de la lumière naturelle. Elle comprend plusieurs sous-paramètres.
	- `sun_entity:` (Optionel) [string] Entité soleil de Home Assistant qui est utilisée pour déterminer l'élévation du soleil. Défaut : sun.sun
	- `min_elevation_for_brightness:` et `max_elevation_for_brightness:` : (Optionel) [integer] Ces paramètres déterminent la plage d'élévation du soleil en degré pendant laquelle la luminosité des lumières est ajustée. Défaut : -20 et 20
	- `min_elevation_for_kelvin:` et `max_elevation_for_kelvin:` : (Optionel) [integer] Ces paramètres déterminent la plage d'élévation du soleil en degré pendant laquelle la température de couleur des lumières est ajustée. Défaut : 0 et 20
	- `modes:` (Optionel) Cette section permet de définir des modes de lumière naturelle pour les différentes plages d'élévation du soleil. Chaque mode peut avoir les paramètres suivants :
    	- `name:` Le nom du mode. Ce nom est utilisé pour lier les lumières à un mode dans la configuration des pièces.
    	- `max_brightness:` et `min_brightness:` (Optionel) [integer] Les limites de luminosité pour ce mode. Défaut : 255 et 100
    	- `max_kelvin:` et `min_kelvin:` (Optionel) [integer] Les limites de température de couleur pour ce mode. Défaut : 5500 et 2000
- `rooms:` Cette section permet de spécifier les paramètres de chaque pièce de la maison.
	- `nom de la pièce:`
		- `occupancy_entity:` [string] Entité utilisée pour détecter la présence dans la pièce. Il peut s'agir d'un capteur de mouvement, d'un interrupteur, etc.
		- `luminance_entity:` (Optionel) [string] Entité est utilisée pour mesurer la luminosité de la pièce.
		- `luminance_limit:` (Optionel) [integer] Seuil de luminosité en-dessous duquel les lumières de la pièce seront automatiquement allumées. Défaut : 10
		- `luminance_hysteresis:` (Optionel) [integer] Valeur est utilisée pour définir un intervalle de luminosité autour de `luminance_limit`, dans lequel les lumières de la pièce seront automatiquement allumées ou éteintes. Défaut : 0
		- `hight_luminance_off_light:` (Optionel) [boolean] Valeur est utilisée pour définir si les lumières de la pièce doivent être éteintes automatiquement en cas de luminosité élevée (supérieure à `luminance_limit` + `luminance_hysteresis`). Défaut : false
		- `lights_entity:` [string] Entité utilisée pour contrôler les lumières de la pièce. Il peut s'agir d'un groupe de lumières ou d'une lumière individuelle.
		- `natural_lighting:` (Optionel) Section qui permet de spécifier les paramètres de l'éclairage naturel pour chaque pièce. Il est possible de spécifier différents modes d'éclairage `name:` avec différents paramètres de luminosité et de température de couleur. Il est également possible de spécifier des entités de lumière individuelles pour chaque mode d'éclairage. Si rien n'est spécifié dans cette section, la lumière naturelle 'default' sera utilisée pour la lumière spécifiée dans `lights_entity:`.
    		- `name:` (Optionel) [string] Nom de l'éclairage naturel que l'on souhaite utiliser. Il est possible de définir plusieurs noms différents en fonction des besoins de l'utilisateur, par exemple "primaire" et "secondaire".
    		- `lights_entity:` (Optionel) [string] Eclairage qui sera contrôlée en fonction de l'élévation du soleil.
    		- `boost_brightness_pct:` (Optionel) [integer] Permet d'augmenter ou de diminuer la luminosité de l'éclairage en pourcentage.
		- `scenes:` (Optionel) Les scènes sont activées lorsqu'un événement est declanché. Par exemple, un éclairage spécifique lorsque la télévision est allumée.
    		- `scene_entity:` [string] Scène que l'on souhaite activer. Cette entité peut être une scène ou un script.
    		- `scene_trigger_entity:` [string] Entité qui declenche l'activation de la scène définie dans `scene_entity`. Cette entité peut être un interrupteur, un capteur, une télévision ou tout autre élément pouvant envoyer une valeur spécifique.
    		- `scene_trigger_value:` [] Valeur que doit prendre `scene_trigger_entity` pour que la scène définie dans `scene_entity` soit activée. Par exemple, si "scene_trigger_value" est défini comme "on", la scène ne sera activée que lorsque "scene_trigger_entity" passe à l'état "on".
        
        > Il est possible de définir plusieurs scènes pour chaque pièce en ajoutant plusieurs blocs "scenes" dans la configuration.
        Exemple :
        > 
        
```yaml
scenes:
 - scene_entity: scene.salon_ambilight
   scene_trigger_entity: switch.android_tv_ambilight_hue
   scene_trigger_value: "on"
 - scene_entity: scene.salon_tv
   scene_trigger_entity: media_player.android_tv
   scene_trigger_value: "on"
```
        
Ce qui signifie :
Si le switch "android_tv_ambilight_hue" est allumé, la scène "salon_ambilight" est activée.
Si le media player "android_tv" est allumé, la scène "salon_tv" est activée.

Notez que les scènes sont dans un ordre prioritaire. Si les deux "trigger" sont actifs, c’est "scene.salon_ambilight" qui sera activée.

## Ordre des opérations

- Présence dans la pièce ?
	- Oui
		- Luminosité faible ?
		- Oui
			- Scène configurée et active ?
			- Oui
				- Lancement de la scène active
			- Non
				- Lumière naturelle configurée ?
				- Oui
					- Allume la lumière en fonction de la lumière naturelle et l'adapte le temps qu'elle est allumée
				- Non
					- Allume simplement la lumière
		- Non
			- Eteindre si `hight_luminance_off_light` = `true`
	- Non
		- Eteindre

## Pistes d'amélioration future

- Nettoyage du code et amélioration des performances

## Remerciements

- Merci à [@jlpouffier](https://github.com/jlpouffier) pour m’avoir fait découvrir appdaemon via sa chaine Youtube ([https://www.youtube.com/@HorizonDomotique](https://www.youtube.com/@HorizonDomotique)).
- Merci à ChatGPT pour son aide précieuse dans la rédaction de la documentation ainsi que sa traduction en anglais.
- Merci à ma compagne pour la relecture de cette documentation.
