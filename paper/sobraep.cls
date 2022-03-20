%%*******************************************************************
%%  SOBRAEP LateX Class
%%
%%  Version 1.0 BETA
%%
%%  Last Modification - 23/07/2015
%%
%%  Copyright 2015 
%%
%%  This work may be distributed and/or modified under the
%%  conditions of the LaTeX Project Public License, either version 1.3
%%  of this license of (at your option) any later version.
%%  The latest version of this license is in
%%    http://www.latex-project.org/lppl.txt
%%  and version 1.3 or later is part of all distributions of LaTeX
%%  version 2005/12/01 or later.
%%
%%  The Current Maintainer of this work is Cássio Luciano Baratieri.
%%*******************************************************************

%%*******************************************************************
%%  DESCRIPTION
%%
%%  Class Options
%%
%%
%%  Document Options
%%
%%*******************************************************************


\ProvidesClass{sobraep}[2015/05/12 V1.0]
%\typeout{-- See the "IEEEtran_HOWTO" manual for usage information.}
%\typeout{-- http://www.michaelshell.org/tex/ieeetran/}
\NeedsTeXFormat{LaTeX2e}

\LoadClass[10pt,twocolumn]{article}



\RequirePackage{ifthen}
\RequirePackage{setspace}
\RequirePackage{fancyhdr}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{graphicx}
\RequirePackage{float}
\RequirePackage{subfigure}
\RequirePackage{geometry}
\RequirePackage{indentfirst}
\RequirePackage{caption}
\RequirePackage{fancybox}
\RequirePackage{lastpage}
\RequirePackage{color}
\RequirePackage{amssymb}
\RequirePackage{amsfonts}
\RequirePackage{amsthm}
\RequirePackage{amsmath}
\RequirePackage{multicol}
\RequirePackage{mathptmx}
\RequirePackage{cite}
\RequirePackage{epstopdf}

\RequirePackage{multirow}
\RequirePackage{booktabs}
\RequirePackage{balance}


%*******************************************************************
\RequirePackage{datetime}

\RequirePackage{siunitx} % A comprehensive (SI) units package

\sisetup{
	round-mode = places,
	round-precision = 2
}

\DeclareSIUnit \voltampere {VA} %apparent power 
\DeclareSIUnit \var {var} %volt-ampere reactive - idle power 


%*******************************************************************
%*******************************************************************
% Options

%Padrão
\def\configlanguage{2}

\DeclareOption{english}
  {
    \def\configlanguage{1}
  }

\DeclareOption{portugues}
  {
    \def\configlanguage{2}
  }

\ProcessOptions

\ifnum \configlanguage = 1
\RequirePackage[english]{babel}
\else
\RequirePackage[brazil]{babel}
\fi

\geometry{tmargin=25mm,
	            lmargin=18mm,
	            rmargin=12mm,
	            bmargin=25mm,
	            a4paper,
		        ignoreheadfoot}%

\newcommand{\titulo}[1]{\gdef\@portuguesetitle{#1}} %


%Resumos e Abstract
\newenvironment{resumo}{\noindent\hspace*{4mm}\normalsize{\bf{\em Resumo --}}\normalsize\bf}{\par\rm\small\medskip\medskip}

\renewenvironment{abstract}{\noindent\hspace*{4mm}\normalsize{\bf{\em Abstract --}}\normalsize\bf}{\par\rm\small\medskip\medskip}

\newenvironment{keywords}{\noindent\hspace*{4mm}\normalsize{\bf{\em Keywords --}}\normalsize\bf}{\par\rm\small\medskip}

\newenvironment{palavraschave }{\noindent\hspace*{4mm}\normalsize{\bf{\em Palavras-chave --}}\normalsize\bf}{\par\rm\small\medskip\medskip}

%Seções
\setcounter{secnumdepth}{3}
%\def\thesection {\Roman{section}.\hskip-7.2pt}
%\def\thesubsection {\Alph{subsection}.\hskip-7.2pt}
\def\thesubsubsection {\arabic{subsubsection})\hskip-7.2pt}

\renewcommand\section{\@startsection {section}{1}{\z@}{2.0ex plus
									    0.5ex minus .2ex}{2.0ex plus 0.3ex minus .2ex}{\centering\MakeUppercase}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}{1.8ex plus
		                                0.5ex minus .2ex}{0.2ex plus .0ex}{\it\raggedright}}
\renewcommand\subsubsection[1]{\@startsection{subsubsection}{3}{4mm}{-2.5ex plus
								       -1ex minus-.2ex}{-0.6ex}{\it\raggedright}{#1:}}



\def\maketitle{\par % \MakeUppercase 
	\begingroup %
		\twocolumn[\@maketitle]
	\endgroup %   
	\let\maketitle\relax \let\@maketitle\relax
} %

\def\@maketitle{ \centering
	{\Large \bf  {\ifnum \configlanguage = 1 \@title	\else  \@portuguesetitle \fi}  \par} 
	\vskip 16.75pt
	{\large\@author}
	\vskip 9mm}

\def\englishtitle{ {\centering\large\bf\@title \par} \medskip\medskip }


%footnote rule
\renewcommand\footnoterule{\noindent\rule{5.075cm}{0.85pt}\vskip 6pt}

%nomenclature
\newcommand{\symbolnomenclature}[2]{\indent\parbox{16mm}{#1}{#2\par}}

\newcommand{\symboldescription}[2]{\indent\parbox{8.5mm}{#1}{- #2\par}}

%Table
\renewcommand{\thetable}{\Roman{table}}
\captionsetup[table]{labelsep = newline, labelfont=bf,  justification=centering}
\captionsetup[figure]{labelsep = period, font=small, justification=justified, singlelinecheck=off}
\addto\captionsenglish{\renewcommand{\figurename}{Fig.}}
\addto\captionsbrazil{\renewcommand{\figurename}{Fig.}}
\addto\captionsenglish{\renewcommand{\tablename}{\bf TABLE}}
\addto\captionsbrazil{\renewcommand{\tablename}{\bf TABELA}}
\addto\captionsenglish{\renewcommand{\refname}{REFERENCES}}
\addto\captionsbrazil{\renewcommand{\refname}{REFERÊNCIAS}}

% Macros for Cross-reference
\ifnum \configlanguage = 1 % english
\newcommand{\figref}[1]{Figure~\ref{#1}}   % Cross-reference of figures
\newcommand{\tabref}[1]{Table~\ref{#1}}    % Cross-reference of tables
\newcommand{\eqnref}[1]{\eqref{#1}}      % Cross-reference of equations
\newcommand{\secref}[1]{Section~\ref{#1} \space }  % Cross-reference of equations
\newcommand{\defref}[1]{Definition~\ref{#1}} % 
\else
\newcommand{\figref}[1]{Figura~\ref{#1}}   % Cross-reference of figures
\newcommand{\tabref}[1]{Tabela~\ref{#1}}    % Cross-reference of tables
\newcommand{\eqnref}[1]{\eqref{#1}}      % Cross-reference of equations
\newcommand{\secref}[1]{Seção~\ref{#1}}  % Cross-reference of equations
\newcommand{\defref}[1]{Definição~\ref{#1}} % 
\fi

\newcommand{\editorfootnote}[1]{\let\thefootnote\relax\footnotetext{\hspace*{-5mm} #1}}   % Editor footnote

%Elimina a numeração de página
\pagestyle{empty}

%Espaçamento entre paragrafos
\setlength{\parskip}{0pt}

%indent config
\setlength\parindent{4.0mm}

%Configura espaçamento entre colunas
\setlength\columnsep{6.0mm}

%Configura espaçamento entre linhas
\renewcommand{\baselinestretch}{0.985}

%Configuração de Listas
\def\@listI{\leftmargin 7.5mm \leftmargini\parsep  \topsep 0pt  \itemsep -1.25mm \partopsep 10pt \listparindent 0pt 
	              \labelsep 4.5mm }


\setlength{\textfloatsep}{7pt} 
\setlength{\intextsep}{7pt} 
\setlength{\abovecaptionskip}{3pt}
\setlength{\belowcaptionskip}{3pt}

	\setlength{\abovedisplayskip}{1cm}
	\setlength{\belowdisplayskip}{1cm}


\sloppy
\hyphenpenalty=10000
\hyphenchar\font=-1

\hbadness=10000
\vbadness=\maxdimen

\newtheorem{theorem}{Theorem}
\newtheorem{acknowledgement}[theorem]{Acknowledgement}
\newtheorem{algorithm}[theorem]{Algorithm}
\newtheorem{axiom}[theorem]{Axiom}
\newtheorem{case}[theorem]{Case}
\newtheorem{claim}[theorem]{Claim}
\newtheorem{conclusion}[theorem]{Conclusion}
\newtheorem{condition}[theorem]{Condition}
\newtheorem{conjecture}[theorem]{Conjecture}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{criterion}[theorem]{Criterion}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\newtheorem{exercise}[theorem]{Exercise}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{notation}[theorem]{Notation}
\newtheorem{problem}[theorem]{Problem}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{remark}[theorem]{Remark}
\newtheorem{solution}[theorem]{Solution}
\newtheorem{summary}[theorem]{Summary}
\renewenvironment{proof}[1][Proof]{\textbf{#1.} }{\ \rule{0.5em}{0.5em}}

\renewcommand\citeform[1]{[#1]}
\renewcommand\citeleft{}
\renewcommand\citeright{}

\AtBeginDocument{

	
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%% End of IEEEtran.cls  %%%%%%%%%%%%%%%%%%%%%%%%%%%%
% That's all folks!