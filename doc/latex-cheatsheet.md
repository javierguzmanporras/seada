# Latex cheat sheet

###### bash commands
$ make
$ aspell --encoding=ISO-8859-1 --lang=es_ES -c memoria.tex

###### Compiladores

* tex: compile .tex files to dvi.
* latex: complite .latex to dvi
* pdftex/pdflatex: compile to pdf.
* xetex/xelatex: compile to pdf with unicode management using systemsfonts.
* luatex/lualatex: compile to pdf write in Lua.


###### Documents
Commands start with backslash "\\".
Comments starts with percentage "%".

environment
* \begin, \end

preamble
* Start in \documentclass command.
* Load \userpackage packages.
* Define commands
* Set options


###### Symbols and special characters
single quotes `texto' -> 'texto'
double quotes ``texto' -> "texto"

% -> Comments
\# -> input arguments
& -> tab separator 
$ -> maths in line ($a$, $ a + b = c$)

\$ -> $


###### Commands
(preámbulo)
\title
\author
\date

\maketitle after \begin{document} contenido del encabezado
\abstract -> define un resumen

\section
\subsection
\subsubsection
\paragraph

\twocolumns
\onecolumn


\ldots -> 3 puntos suspensivos

\begin{itemize}
    \item
    \item
\end{itemize}

\begin{enumerate}
    \item
    \item
\end{enumerate}

\begin{equation} ... \end{equation}
\begin{document} ... \end{document}
    

###### packages
\documentclass{article}
\usepackage[utf8]{inputenc} %Paquete de codificación para carácteres en español
\usepackage[spanish]{babel} %Paquete para reconocimiento de idioma
\usepackage{ammath} %Paquete de la Sociedad Americana de Matemáticas
