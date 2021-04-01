Mon projet serais d'écrire un code simple pour générer une image, (ou une vidéo, car le code est appelé à chaque frame),<br>
mais qui utiliserais automatiquement la carte graphique grace a OpenGL, et qui serais donc très rapide.<br>
<br>
Exemple : le compilateur se nourit du fichier source.monlangage et produit le dossier bin en sortie.<br>
<br>
Ce dossier de sortie contient l'executable produit par le compilateur : OpenGL.exe,<br>
ainsi que les shaders eux aussi produits par le compilateur, qui sont nécessaires au bon fonctionnement de l'exécutable.<br>
<br>
Vous constatez qu'avec un code rudimentaire, on peut obtenir un programme qui genere l'ensemble de mandelbrot<br>
avec une rapidité stupéfiante car ça se passe sur la carte graphique.<br>
Bon ok ça lag un peu, mais si vous remplacer les double par des floats, et les dvec4 / dvec2 par des vec4 / vec2,<br>
ou que vous réduisez le nombre d'itérations par pixel, qui actuellement est 1000, ça tournera en 60 fps.<br>
Et ceci, quel que soit la taille de l'écran ! Du moment que vous avez moins de pixels sur votre écran, que vous n'avez<br> d'unité dans votre carte graphique, le programme tournera à la même vitesse.
<br>
<br>
La syntaxe serais la même que celle des shaders d'OpenGL, qui est assez rudimentaire,<br>
donc je n'aurais pas besoin de lire des lexemes à ce niveau là, puisque c'est OpenGL qui va se charger<br>
de compiler le plus gros du programme.<br>
<br>
En revanche, les shaders ne fonctionnent pas tous seuls, il faut un code (C++ par exemple) qui les lis et les envoie,<br>
à OpenGL pour qu'il les compile, puis à la carte graphique.<br>
<br>
Le fichier C++ en question est : fichier_cpp_utilise_par_le_compilateur.cpp<br>
<br>
Si j'ai été clair jusqu'ici, vous avez du comprendre que mon compilateur ne fait rien du tout:<br>
Il prend le fichier fichier_cpp_utilise_par_le_compilateur.cpp et le fichier source.monlangage, et les envoies<br>
a gcc.<br>
(C'est ensuite, lors de l'éxécution du programme, que OpenGL compile les shaders, donc le fichier source.monlangage)<br>
<br>
Effectivement j'aurais pu m'arrêter là, j'aurais atteint mon but qui est de simplifier la confection d'un code qui<br>
s'éxécute sur la carte graphique.<br>
En revance je n'aurais pas atteint mon but qui est de faire un compilateur dans le cadre de ce cours.<br>
<br>
J'aurais pu changer la syntaxe des shaders d'OpenGL pour faire mon propre langage mais je ne l'ai pas fait<br>
car je souhaite garder un maximum de fonctionnalitées fournies par OpenGL, et la syntaxe est vraiment simple.<br>
Mais un simple shader ne permet pas de specifier certains parametres, par exemple la taille de la fenêtre.<br>
C'est là que j'ajoute ma touche personnelle.<br>
Si je ne modifie pas la syntaxe du langage des shaders d'OpenGL, je peut en revanche y ajouter des fonctionnalités.<br>
<br>
Par exemple, la ligne suivante au début du fichier permet de définir la taille de l'écran.<br>
```c++
size(1600, 900);
```
<br>
Pour faire ça, je vais avoir besoin que mon compilateur remplace cette ligne par:<br>

```c++
#version 460 core

layout(location = 0) out vec4 color;

uniform unsigned int frame;
uniform vec4 screenRect;
```
<br>
Je vais aussi avoir besoin que cette ligne modifie WIDTH et HEIGHT dans le fichier<br>
fichier_cpp_utilise_par_le_compilateur.cpp<br>
<br>
Je n'ai pas encore pensé à toutes les fonctionnalités que je pourrais ajouter.<br>