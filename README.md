# Full-Automation-Light
## Introduction
Ce script utilise AppDaemon pour automatiser les lumières d'une maison en utilisant les informations de luminosité naturelle et d'occupation des pièces. Il permet de configurer des modes de luminosité et de température de couleur en fonction de la position du soleil, ainsi que des limites de luminosité pour chaque pièce. Il permet également de définir des scènes pour les différentes pièces et de les déclencher en fonction de certains événements. Il est configurable via un fichier yaml pour s'adapter à vos besoins.
## Configuration :
FullAutomationLights : Ce est la section de base de configuration qui contient les paramètres généraux pour l'application.
module: Le nom du module python qui contient le script.
class: Le nom de la classe qui est utilisée pour instancier l'application.
debug: (Optionnel) Active ou désactive les messages de débogage.
natural_lighting : Cette section contient les paramètres liés à la luminosité naturelle.
sun_entity: L'entité de Home Assistant qui représente le soleil (ex: sun.sun).
min_elevation_for_brightness: L'altitude minimale du soleil pour laquelle la luminosité sera ajustée (en degrés).
max_elevation_for_brightness: L'altitude maximale du soleil pour laquelle la luminosité sera ajustée (en degrés).
min_elevation_for_kelvin: L'altitude minimale du soleil pour laquelle la température de couleur sera ajustée (en degrés).
max_elevation_for_kelvin: L'altitude maximale du soleil pour laquelle la température de couleur sera ajustée (en degrés).
modes: Liste des modes de luminosité/température de couleur disponibles. Chaque mode contient :
name: Le nom du mode.
max_brightness: La luminosité maximale pour ce mode (en pourcentage).
min_brightness: La luminosité minimale pour ce mode (en pourcentage).
max_kelvin: La température de couleur maximale pour ce mode (en Kelvin).
min_kelvin: La température de couleur minimale pour ce mode (en Kelvin).
rooms: Cette section contient les paramètres pour chaque pièce de la maison. Chaque pièce est définie par un nom (ex: salon) et contient :
occupancy_entity: L'entité de Home Assistant qui indique si la pièce est occupée ou non (ex: input_boolean.salon_presence).
luminance_entity: L'entité de Home Assistant qui mesure la luminosité de la pièce (ex: sensor.salon_luminosite).
luminance_limit: La limite de luminosité à ne pas dépasser pour cette pièce (en lux).
luminance_hysteresis: La valeur d'hystérésis utilisée pour éviter les fluctuations de la limite de luminosité (en lux).
hight_luminance_off_light : (Optionnel) Si activé, les lumières seront éteintes si la luminosité dépasse la lim
