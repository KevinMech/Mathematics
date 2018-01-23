#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Représentation graphique des tables de multiplication.
Pour lancer ce programme, exécuter :
    multiplication.py
"""

import sys
import math
import random
import decimal
import time
import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
LIMEGREEN = (50, 205, 50)

screen_width = 1800
screen_height = 1000

centre_cercle_x = 900
centre_cercle_y = 500

cercle_rayon = 400
point_rayon = 3


def add_point(gSurface, gFont, points, val, base_angle, afficher=False):
    p_angle = (math.pi / 2) - float(val) * base_angle
    p_x = centre_cercle_x + int(math.ceil(cercle_rayon * math.cos(p_angle)))
    p_y = centre_cercle_y - int(math.ceil(cercle_rayon * math.sin(p_angle)))
    points[val] = [p_x, p_y]

    if afficher:
        label = gFont.render('%s' % val, True, BLACK, WHITE)
        labelRect = label.get_rect()

        label_x = centre_cercle_x + int(math.ceil((cercle_rayon + 15) * math.cos(p_angle)))
        label_y = centre_cercle_y - int(math.ceil((cercle_rayon + 15) * math.sin(p_angle)))

        labelRect.centerx = label_x
        labelRect.centery = label_y

        gSurface.blit(label, labelRect)
        pygame.draw.circle(gSurface, RED, (p_x, p_y), point_rayon, 0)
    return [p_x, p_y]


def dessine_table(gSurface, gFont, table, base, precision=0, afficher=False):
    points = {}
    table_mul = {}
    usage_points = {}

    base_angle = (math.pi * 2) / base

    for d in range(base):
        table_mul[d] = d * table

        if precision > 0:
            src = decimal.Decimal(d)
            dest = decimal.Decimal(str(round(table_mul[d], precision) % base))
        else:
            src = d
            dest = table_mul[d] % base

        if points.get(src) is None:
            p_src = add_point(gSurface, gFont, points, src, base_angle, afficher)
            usage_points[src] = 1
        else:
            p_src = points[src]
            usage_points[src] += 1

        """
        print "d: {0} table_mul[{0}]: {1} arrondi(table_mul[{0}]) % {2}: {3}".format(d,
                                                                              float(table_mul[d]),
                                                                              base,
                                                                              dest)
        """

        try:
            if points.get(dest) is None:
                p_dest = add_point(gSurface, gFont, points, dest, base_angle, afficher)
                usage_points[dest] = 1
            else:
                p_dest = points[dest]
                usage_points[dest] += 1

            r_alea = int(math.ceil(random.random() * 255))
            g_alea = int(math.ceil(random.random() * 255))
            b_alea = int(math.ceil(random.random() * 255))
            couleur = BLUE
            # couleur = [r_alea, g_alea, b_alea]

            pygame.draw.line(gSurface, couleur, p_src, p_dest, 1)
            pygame.display.update()
        except:
            print ("%s x %s = %s modulo %s = %s n'est pas dans points") % (d, 
                                                                         table, 
                                                                         table_mul[d], 
                                                                         base, 
                                                                         dest)


if __name__ == '__main__':
    precision = 0
    pygame.init()

    table = None
    while table is None:
        table_input = raw_input("Entrez la table de multiplication souhaitée: ")
        if table_input.isdigit():
            table = int(table_input)
        else:
            print('Veuillez entrer un numéro et réessayer\n')

    base = None
    while base is None:
        base_input = raw_input("Entrez la base souhaitée: ")
        if base_input.isdigit() and int(base_input) > 0:
            base = int(base_input)
        else:
            print("entrez un nombre supérieur à 0 et réessayez\n")

    afficher = raw_input("Afficher les points (o / n) : ")

    if afficher == "o":
        afficher_points = True
    else:
        afficher_points = False

    start_time = time.time()

    if precision > 0:
        increment = decimal.Decimal("{0}".format(1.0 / pow(10, precision), precision))
    else:
        increment = 1

    windowSurface = pygame.display.set_mode([screen_width, screen_height], 0, 32)

    # Titre de la fenêtre
    pygame.display.set_caption("Table de %s dans la base %s, precision %s, increment %s" % (table, 
                                                                                            base,
                                                                                            precision,
                                                                                            increment))
    basicFont = pygame.font.SysFont(None, 18)
    windowSurface.fill(WHITE)
    pygame.display.update()
    pygame.draw.circle(windowSurface, BLACK, (centre_cercle_x, centre_cercle_y), cercle_rayon, 1)
    pygame.display.update()
    dessine_table(windowSurface, basicFont, table, base, precision, afficher_points)
    end_time = time.time()
    print("Temps d'exécution {0}").format(end_time - start_time)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    pygame.quit()
