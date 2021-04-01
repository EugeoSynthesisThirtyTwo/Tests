Mon projet serais d'écrire un code simple pour générer une image, (ou une vidéo, car le code est appelé à chaque frame),<br>
mais qui utiliserais automatiquement la carte graphique grace a OpenGL.<br>
<br>
Exemple : le compilateur se nourit du fichier source.monlangage et produit le dossier bin en sortie.<br>
<br>
Ce dossier de sortie contient l'executable produit par le compilateur : OpenGL.exe,<br>
ainsi que les shaders eux aussi produits par le compilateur, qui sont nécessaires au bon fonctionnement de l'exécutable.<br>
<br>
Vous constatez qu'avec un code rudimentaire, on peut obtenir un programme qui genere l'ensemble de mandelbrot<br>
avec une rapidité stupéfiante car ça se passe sur la carte graphique.<br>
<br>

La syntaxe serais la même que celle des shaders d'OpenGL, qui est assez rudimentaire, donc je n'aurais pas besoin de lire<br>
des lexemes à ce niveau là, puisque c'est OpenGL qui va se charger de compiler le plus gros du programme.<br>
<br>
En revanche, les shaders ne fonctionnent pas tous seuls, il faut un code (C++ par exemple) qui les lis et les envoie,<br>
à OpenGL pour qu'il les compile, puis à la carte graphique.<br>
<br>
Le fichier C++ en question est : fichier_cpp_utilise_par_le_compilateur.cpp<br>
<br>
Si j'ai été clair jusqu'ici, vous avez du comprendre que mon compilateur ne fait rien du tout:<br>
