#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
import sys
from tycat import read_instance
from bisect import insort_right
 

def quad_is_included(quad1, quad2):
    return (quad1.min_coordinates[0] >= quad2.min_coordinates[0] and quad1.min_coordinates[1] >= quad2.min_coordinates[1]) \
        and (quad1.max_coordinates[0] <= quad2.max_coordinates[0] and quad1.max_coordinates[1] <= quad2.max_coordinates[1])


def is_left(P0, P1, P2):
    return (P1.coordinates[0] - P0.coordinates[0]) * (P2.coordinates[1] - P0.coordinates[1]) \
        - (P2.coordinates[0] - P0.coordinates[0]) * (P1.coordinates[1] - P0.coordinates[1])

def wn_PnPoly(poly, V):

    P = poly[0].points[0]

    wn = 0

    V = tuple(V[0].points[:]) + (V[0].points[0],)

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




def trouve_inclusions(liste_poly):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """

    for i, p in enumerate(liste_poly):
        liste_poly[i] = (p, p.bounding_quadrant())


    vecteur_reponse = [-1] * len(liste_poly)

    liste_y = []


    for i, poly in enumerate(liste_poly):
        max_y = -float('Inf')
        for point in poly[0].points:
            if point.coordinates[1] > max_y:
                max_y = point.coordinates[1]
        insort_right(liste_y, (max_y, i))
        
            
    for i, triplet in enumerate(liste_y):
        for j in range(i+1, len(liste_y)):
            if not quad_is_included(liste_poly[triplet[1]][1], liste_poly[liste_y[j][1]][1]):
                continue
            if wn_PnPoly(liste_poly[triplet[1]], liste_poly[liste_y[j][1]]) != 0:
                vecteur_reponse[triplet[1]] = liste_y[j][1]
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
