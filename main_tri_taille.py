#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
import sys
from tycat import read_instance
from math import sqrt


def quad_is_included(quad1, quad2):
    return (quad1.min_coordinates[0] >= quad2.min_coordinates[0] and quad1.min_coordinates[1] >= quad2.min_coordinates[1]) \
        and (quad1.max_coordinates[0] <= quad2.max_coordinates[0] and quad1.max_coordinates[1] <= quad2.max_coordinates[1])


def diago(quad):
    total = 0
    for c_1, c_2 in zip(quad.min_coordinates, quad.max_coordinates):
        diff = c_1 - c_2
        total += diff * diff
    return sqrt(total)


def is_left(P0, P1, P2):
    return (P1.coordinates[0] - P0.coordinates[0]) * (P2.coordinates[1] - P0.coordinates[1]) \
        - (P2.coordinates[0] - P0.coordinates[0]) * (P1.coordinates[1] - P0.coordinates[1])

def wn_PnPoly(poly, V):

    P = poly.points[0]

    wn = 0

    V = tuple(V.points[:]) + (V.points[0],)

    for i in range(len(V)-1):
        if V[i].coordinates[1] <= P.coordinates[1]:
            if V[i+1].coordinates[1] > P.coordinates[1]:
                if is_left(V[i], V[i+1], P) > 0:
                    wn += 1
        else:
            if V[i+1].coordinates[1] <= P.coordinates[1]:
                if is_left(V[i], V[i+1], P) < 0:
                    wn -= 1
    return wn


def is_included(poly, poly2):
    
    if not quad_is_included(poly[2], poly2[2]):
        return False

    return wn_PnPoly(poly[1], poly2[1])


def trouve_inclusions(liste_poly):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """

    vecteur_reponse = [-1] * len(liste_poly)

    liste_num_poly_quad = []

    for i, p in enumerate(liste_poly):
        liste_num_poly_quad.append([i, p, p.bounding_quadrant()])
  
    liste_num_poly_quad.sort(key=lambda x: diago(x[2]))

    for i, poly in enumerate(liste_num_poly_quad):
        for j in range(i + 1, len(liste_num_poly_quad)):
            if is_included(poly, liste_num_poly_quad[j]):
                vecteur_reponse[poly[0]] = liste_num_poly_quad[j][0]
                break

    return vecteur_reponse


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions = trouve_inclusions(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
