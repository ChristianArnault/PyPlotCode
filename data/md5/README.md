
# Prérequis

Obligatoire : avoir "sourcer" le fichier `PyPlotCode/bin/env.sh`.

Si on veut utiliser une image docker anaconda 3 :
* se placer dans PyPlotCode
* lancer `anarun 3 bash`
* resourcer `bin/env.sh`
* revenir dans `data/md5`


# Recettes rapides pour utilisateur pressé

Vérifier que les images ne sont pas pathologiques :
```
oval r patho%
oval d patho%
```

Regénérer les signatures de référence pour les images spécifiques :
1. Tourner tous les exercices avec toutes le simages : `oval r ex%`
1. Eventuellement, comparer les résultats avec les références : `oval d ex%`
1. Copier les résultats en tant que nouvelles références : : `oval v ex%`
1. Eventuellement, vérifier que la copie s'est bien faite : `oval d ex%`


# Configuration ovalfile.py

La description des cibles de oval est faite dans le fichier "ovalfile.py". Dans une variante un peu compliquée, parce
qu'au lieu de lister expliciter les cibles, j'utilise du code python pour les générer automatiquement à partir de
ce qui est trouvé dans "data/fits".

Les données préparées par `ovalfile.py`, et qui seront exploitées par `oval.py`, doivent être des tableaux
de la forme :

```python
targets = [

    { "name": "analyze_ex0", "command": "pylint ex0_hello_loops.py" },
    { "name": "analyze_ex1", "command": "pylint ex1_read_image.py" },
    # ...
]

run_filters_out = [

    { "name": "wcs", "re": "^(WARNING:|warning:|Defunct|this form of).*$", "apply": "ex(4|5)%" },
    # ...
]

diff_filters_in = [
    { "name": "pylint", "re": "%rated at%", "apply": "analyze%" },
    # ...
]
```


# Commandes oval

## Différentes commandes oval

* lister toutes les cibles : ```oval l```
* executer toutes les cibles : ```oval r```
* comparer la sortie avec les références : ```oval d```
* écraser les références avec les dernières sorties : ```oval v```
* crypter les références en fichiers md5 : ```oval c```

## Restreindre à un sous-ensemble de cibles

Quelle que soit la commande, on peut restreindre les cibles
en utilisant un motif dont le joker est `%`. Quelques exemples
ci-dessous, avec la commande `oval l`.

* seulement l'exercice 2 : ```oval l ex2%```
* seulement l'image 13 : ```oval l %NPAC13```
* seulement l'exercice2 pour l'image 13 : ```oval l ex2%NPAC13```