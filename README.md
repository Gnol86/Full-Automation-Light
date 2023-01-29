# Full Automation Lights

## Présentation

Vous en avez marre de vous lever à 2h du matin pour éteindre la lumière de votre chambre d'amis qui est encore allumée ? Vous en avez assez de devoir vous rappeler de mettre en marche votre éclairage extérieur lorsque le soleil se couche ? Ne vous inquiétez plus ! Grâce à notre application magique (mais pas trop quand même), vous allez pouvoir automatiser tout cela en un rien de temps !

Notre application est basée sur AppDaemon et fonctionne en conjonction avec Home Assistant. Elle est conçue pour contrôler automatiquement l'éclairage de votre maison en fonction de différents critères tels que l'heure, la luminosité extérieure et l'élévation du soleil. Plus besoin de se prendre la tête avec les commandes, notre application s'occupe de tout ! Et en plus, elle est open-source, vous pourrez donc l'améliorer à votre guise ou l'adapter à vos besoins.

Alors n'hésitez plus et installez notre application pour vivre dans une maison éclairée à la perfection ! Et si jamais vous rencontrez des problèmes, n'hésitez pas à consulter notre documentation, elle est là pour ça !

## Fonctionnalités

- Occupation de la pièce: Le script utilise des capteurs d'occupation pour détecter la présence de personnes dans une pièce et ajuster en conséquence l'éclairage. Il est possible de définir des limites de luminosité et un hystérésis pour chaque pièce. Il y a également une option pour éteindre les lumières automatiquement si la luminosité naturelle dans la pièce est élevée.
- Lumière naturelle: Le script utilise la position du soleil pour ajuster automatiquement la luminosité et la température de couleur des lumières en fonction de l'élévation du soleil. Il est possible de définir différents modes de lumière naturelle pour chaque pièce.
- Scènes: Le script permet de déclencher automatiquement des scènes en fonction de l'état d'un déclencheur spécifique, comme par exemple l'allumage d'un téléviseur. Il est possible de définir différentes scènes pour chaque pièce.
- Configuration pour plusieurs pièces: il est possible de configurer plusieurs pièces avec différentes options pour l'automatisation de la lumière et les scenes. Il y a une configuration pour le salon et une autre pour la cuisine dans l'exemple fourni.
- Configurations avancées: Le script offre une grande flexibilité de configuration pour les utilisateurs expérimentés, permettant de définir des paramètres tels que les limites de luminosité, les modes de lumière naturelle, les scènes et les capteurs d'occupation pour chaque pièce de la maison.

## Prérequis

- Home Assistant : Il est nécessaire d'avoir une installation fonctionnelle de Home Assistant pour utiliser ce script.
- AppDaemon : AppDaemon est un add-on pour Home Assistant qui permet d'exécuter des scripts Python en arrière-plan. Il est nécessaire d'installer et de configurer AppDaemon pour utiliser ce script.

## Installation

Pour installer cette application, vous devez avoir Home Assistant et AppDaemon déjà installés et configurés. Si ce n'est pas le cas, veuillez vous référer aux prérequis pour les instructions d'installation.

Une fois que vous avez Home Assistant et AppDaemon en cours d'exécution, vous pouvez installer cette application en suivant les étapes suivantes:

1. Téléchargez le fichier FullAutomationLights.py et placez-le dans le répertoire "apps" d'AppDaemon.
2. Ajoutez la configuration suivante à votre fichier apps.yaml. Ce fichier se trouve généralement dans le répertoire "apps" d'AppDaemon.

## Configuration

> Exemple de configuration minimal pour allumer et éteindre les lumière du groupe “light.living_room” dans la pièce “living_room” lorsqu’un mouvement est detecté avec le capteur “binary_sensor.living_room_motion” :
> 

```yaml
FullAutomationLights:
  module: FullAutomationLights
  class: FullAutomationLights
  rooms:
    living_room:
      occupancy_entity: binary_sensor.living_room_motion
      lights_entity: light.living_room
```

<aside>
📌 "light.living_room" est allumé avec un simple “light.turn_on” sans parramètre. Il est possible de définir manuellement la luminosité et la température du blanc ou la couleur.
</aside>

---

> Le même exemple de configuration avec la fonction lumière naturel. Ici ‘natural_lighting’ est défini pour activer la fonctionnalitée. Par défaut, un “mode” de lumière naturelle nommé “default” est créé. La la pièce “living_room”, le groupe de lumières “light.living_room” est lié à ce mode :
> 

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

La configuration de FullAutomationLights comprend les paramètres suivants :

- **`module`** et **`class`** Ces paramètres indiquent à AppDaemon où trouver le fichier FullAutomationLights.py et quelle classe utiliser pour démarrer l'application.
- **`debug`** : (Optionel) [boolean] Cette option permet d'activer ou de désactiver les messages de débogage de l'application. Il est conseillé de la mettre à "true" lors de la première installation pour vérifier que tout fonctionne correctement. La fonction débug est bavarde et ralenti le script. Pour la mise en production, il est préférable de la désactiver. Défaut : false
- **`transitions`** : (Optionel) Cette section permet de définir des transitions personalisées.
- **`natural_lighting`** : (Optionel) Cette section permet de configurer la gestion de la lumière naturelle. Elle comprend plusieurs sous-paramètres.
- **`rooms`** : Cette section permet de spécifier les paramètres de chaque pièce de la maison. Pour chaque pièce.

### `**transitions**`

- **`init`** : (Optionel) [integer] durée de la transition en secondes lors de l’initialisation du script. Défaut : 0
- **`occupancy`** : (Optionel) [integer] durée de la transition en secondes lors changement d’état du au capteur “occupancy_entity”. Défaut : 1
- **`low_light`** : (Optionel) [integer] durée de la transition en secondes lors changement d’état du au capteur “luminance_entity”. Défaut : 15
- **`scenes`** : (Optionel) [integer] {5} durée de la transition en secondes lors changement de scène.
- **`natural_lighting`** : (Optionel) [integer] {10} durée de la transition en secondes lors changement de la numière naturel.
- **`off`** : (Optionel) [integer] {3} durée de la transition en secondes lors de l’extinction des lampes.

> Exemple avec les valeurs par défaut.
> 

```yaml
transitions:
  init: 0
  occupancy: 1
  low_light: 15
  scenes: 5
  natural_lighting: 10
  off: 3
```

### **`natural_lighting`**

- **`sun_entity` :** (Optionel) [string] {sun.sun} L'entité de soleil de Home Assistant qui est utilisée pour déterminer l'élévation du soleil.
- **`min_elevation_for_brightness`** et **`max_elevation_for_brightness`** : (Optionel) [int] {-20 et 20} Ces paramètres déterminent la plage d'élévation du soleil en degré pendant laquelle la luminosité des lumières est ajustée en fonction de celle-ci.
- **`min_elevation_for_kelvin`** et **`max_elevation_for_kelvin`** : (Optionel) [int] {0 et 20} Ces paramètres déterminent la plage d'élévation du soleil en degré pendant laquelle la température de couleur des lumières est ajustée en fonction de celle-ci.
- **`modes`** : (Optionel) Cette section permet de définir des modes de lumière pour les différentes plages d'élévation du soleil. Chaque mode peut avoir les paramètres suivants :
    - **`name`** : Le nom du mode. Ce nom est utilisé pour lier les lumières à un mode dans la configuration des pièces.
    - **`max_brightness`** et **`min_brightness`** : Les limites de luminosité pour ce mode.
    - **`max_kelvin`** et **`min_kelvin`** : Les limites de température de couleur pour ce mode.

### Pièces

La section "rooms" de la configuration permet de spécifier les paramètres de chaque pièce de la maison. Pour chaque pièce, vous devez spécifier les entités Home Assistant suivantes:

- occupancy_entity: cette entité est utilisée pour détecter la présence dans la pièce. Il peut s'agir d'un capteur de mouvement, d'un bouton-poussoir, etc.
- luminance_entity: cette entité est utilisée pour mesurer la luminosité de la pièce. Il peut s'agir d'un capteur de luminosité, d'un capteur de lumière, etc.
- luminance_limit: cette valeur est utilisée pour définir un seuil de luminosité en dessous duquel les lumières de la pièce seront automatiquement allumées.
- luminance_hysteresis: cette valeur est utilisée pour définir un intervalle de luminosité autour de luminance_limit, dans lequel les lumières de la pièce seront automatiquement allumées ou éteintes.
- hight_luminance_off_light: cette valeur est utilisée pour définir si les lumières de la pièce doivent être éteintes automatiquement en cas de luminosité élevée (supérieure à luminance_limit + luminance_hysteresis).
- lights_entity: cette entité est utilisée pour contrôler les lumières de la pièce. Il peut s'agir d'un groupe de lumières, d'une lumière individuelle, etc.
- natural_lighting: cette section permet de spécifier les paramètres de l'éclairage naturel pour chaque pièce. Il est possible de spécifier différents modes d'éclairage (name) avec différents paramètres de luminosité et de température de couleur. Il est également possible de spécifier des entités de lumière individuelles pour chaque mode d'éclairage.
    - La sous-section "name" permet de spécifier le nom de l'éclairage naturel que l'on souhaite utiliser. Il est possible de définir plusieurs noms différents en fonction des besoins de l'utilisateur, par exemple "primaire" et "secondaire".
    - La sous-section "lights_entity" permet de définir l'entité de l'éclairage qui sera contrôlée en fonction de l'élévation du soleil. Il est possible de définir plusieurs entités différentes en fonction des besoins de l'utilisateur, par exemple "light.salon_primaire" et "light.salon_secondaire".
    - Il existe également une option "boost_brightness_pct" qui permet d'augmenter ou de diminuer la luminosité de l'éclairage en pourcentage.
- "scenes" dans "rooms" permet de définir des scénarios spécifiques pour chaque pièce. Chacun des scénarios est défini par une "scene_entity", une "scene_trigger" et une "scene_trigger_value".
    - "scene_entity" est l'entité Home Assistant qui représente la scène que l'on souhaite activer. Cette entité peut être une scène prédéfinie dans Home Assistant ou une scène personnalisée créée par l'utilisateur.
    - "scene_trigger" est l'entité Home Assistant qui déclenche l'activation de la scène définie dans "scene_entity". Cette entité peut être un interrupteur, un capteur ou tout autre élément pouvant envoyer une commande à Home Assistant.
    - "scene_trigger_value" est la valeur que doit prendre "scene_trigger" pour que la scène définie dans "scene_entity" soit activée. Par exemple, si "scene_trigger_value" est défini comme "on", la scène ne sera activée que lorsque "scene_trigger" passe à l'état "on".
        
        > Il est possible de définir plusieurs scénarios pour chaque pièce en ajoutant plusieurs blocs "scenes" dans la configuration.
        Exemple :
        > 
        
        ```yaml
        scenes:
        	- scene_entity: scene.salon_ambilight
        		scene_trigger: switch.android_tv_ambilight_hue
        		scene_trigger_value: "on"
        	- scene_entity: scene.salon_tv
        		scene_trigger: media_player.android_tv
        		scene_trigger_value: "on"
        ```
        
        > Ce qui signifie :
        Si le switch "android_tv_ambilight_hue" est allumé, la scène "salon_ambilight" est activée.
        Si le media player "android_tv" est allumé, la scène "salon_tv" est activée.
        > 
        
        > Notez que les scènes sont dans un ordre prioritaire. Si les deux "trigger" sont actifs, c’est "scene.salon_ambilight" qui sera activée.
        > 

Exemple de configuration minimal :

```yaml
rooms:
	salon:
	  occupancy_entity: input_boolean.salon_presence
	  lights_entity: light.salon
```

## Pistes d'amélioration future

- Néttoyage du code et amélioration des performances

## Remerciements

- Merci à @jlpouffier pour m’avoir fait découvrir appdaemon via sa chaine Youtube ([https://www.youtube.com/@HorizonDomotique](https://www.youtube.com/@HorizonDomotique)).
- Merci à ChatGPT pour son aide précieuse dans la rédaction de la documentation ainsi que sa traduction en anglais.
