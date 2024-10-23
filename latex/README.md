# LaTeX

Aquí se encuentran los documentos que crean la documentación a entregar.

## Instalación de lo necesario para compilar el documento en una distro Debian

Tested en: Linux Mint 21.3 x86_64.

```console
$ sudo apt install texlive-latex-base

$ sudo apt install dvipng
$ sudo apt install texlive-latex-extra
$ sudo apt install texlive-fonts-recommended
$ sudo apt install texlive-pictures
$ sudo apt install texlive-extra-utils
$ sudo apt install magick
$ sudo apt install texlive-font-utils
$ sudo apt install latexmk
$ sudo apt install texlive-lang-greek
$ sudo apt install texlive-lang-spanish
$ sudo apt install cm-super
```

Seguramente haya más maneras.

Fuente: [Using LaTeX in Sublime Text](https://rowannicholls.github.io/sublime_text/latex.html).

También debería funcionar [Overleaf](https://www.overleaf.com/). Altamente recomendado para principiantes en LaTeX.

## Crear el documento:

Dentro de este directorio:

```console
$ ./build.sh
```

A veces el índice no se actualiza bien la primera vez. Razón desconocida.

## TODO

- Cuando se haga una parte que se explique? Idk
