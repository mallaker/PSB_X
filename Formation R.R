# Les differentes aides -------------------------------------------------

getwd() #aller dans un repertoire
setwd() #permet de se positionner dans un repertoire
help("mean")
?mean() #equivalent de help


# Les Objets R ------------------------------------------------------------


#objet numerique
tasse<-12
tasse <- 14 #raccourci de l'affectation ALT+6
x <- 12
y <- 10
z <- 11
(x+y+z)/3 #moyenne en calcul
vecteurnum <- c(x,y,z) #creation vecteur
mean(vecteurnum)#moyenne de ce vecteur, pour faire la moyenne en utilisant mean, on est obligé de creer un vecteur

Section <- c("part 1","part 2","part3") #creation vecteur chaines de caractere
print("ici je test ma variable chaine de caratere") #afficher le contenu
rm(tasse) #supprimer un objet
rm(Section)
NA #Not available=information manquante ou non disponible
Datedenaissance <- c("12/04","02/03",NA)
moyenne <- c(13,14,15,NA,16)
mean(moyenne, na.rm = TRUE)#calcul de la moyenne en indiquant qu'il existe une valeur manquante en faisant na.rm=true
x <- 14:50
mean(x)
matrix(data = 1:4, nrow = 2,ncol = 2, byrow = TRUE)


# Les Matrices ------------------------------------------------------------

# Creation des matrices

x <- matrix(c(1:6),nrow=2,ncol=3,byrow=TRUE) #matrice 2lignes et 3colonnes

y <- matrix(1:2,ncol=1) #matrice 1 colonne et 2 lignes

z<- matrix(1:2, nrow=1) #matrice 1 ligne et 2 colonnes

f <- matrix(3:1,ncol=3)
f
m <- matrix(1:4,nrow=3,ncol=3)

#des fonctionnalites des matrices 

#Il est cependant possible de transformer un vecteur en une matrice unicolonne avec la fonction  as.matrix

matrix(c("A","B","C","A"),ncol=2) #matrice de caractere

#operations mathematiques entre les matrices

m <- matrix(1:4,ncol=2) #on crée cette matrice m

n <- matrix(3:6,ncol=2,byrow=T) #on crée la matrice n
n
m+n #addition de deux matrices de meme dimension

m*n # produit élément par élément
m%*%n #produit scalaire
sin(m) # sinus élément par élément
exp(m) # exponentielle élément par élément
m^4 # puissance quatrième élément par élément
t(m) #transposition de la matrice m

#Autres operations maths

#diag(5):matrice identité d'ordre 5

#diag(vec):matrice diagonale avec les valeurs du vecteur  vec  dans la diagonale

#crossprod(X, Y):produit croisé (t(X)%*%Y)

#det(X):déterminant de la matrice X

#svd(X):décomposition en valeurs singulières

#eigen(X):diagonalisation d'une matrice

#solve(X):inversion de matrice

#solve(A, b):résolution de système linéaire

#chol(Y):décomposition de Cholesky

#qr(Y) : décomposition QR


# Les Facteurs ------------------------------------------------------------

#Creation des facteurs pour les variables qualitatives

y <- c("H","F","H","F","H") #on attribue a Y les variables qualitatives

yf <- factor(y) #on crée le facteur yf comptenant les valeurs de y

levels(yf)<- c("femme", "homme") #permet de renommer les modalités de y
yf
# Creation des facteurs avec des variables quantitatives

monfact<-c(1,2,3,4,5,6,7,4,2) #creation des modalités numeriques
monfact
monfact<- as.factor(salto) #changement des modes ou modalités en facteu

#La fonction  ordered  va quant à elle nous permettre de créer des facteurs ordonnés

niveau<-ordered(c("debutant","champion","debutant","moyen","moyen","champion"),levels=c("debutant","moyen","champion"))
niveau
                
                
#on peut transformer les chaines de caratere en facteur, des facteurs en numerique en utilisant les fonctions as.factor(), as.character(), as.numeric()


# Les listes --------------------------------------------------------------

#Création d'une liste
maliste <- list(c("A","B","C","A"),matrix(1:4,2,2))
maliste[[1]] #afficher premier element de la liste
maliste[[1]] [1]#afficher le premier contenu du premier element de la liste
maliste[[2]]#afficher le second element de la liste
length(maliste)
mode(maliste)
is.list(maliste)
#la liste peut contenir un vecteur, une matrice et un dataframe


# Les Data Frame ----------------------------------------------------------

#Création du dataframe (est un tableau qui ressemble à une matrice mais dans lequel on peut avoir differents types de tableaux de données avec des numeriques et des caracteres)

x <- c("A","B","C","A")
y <- 1:4
mondatafr <- data.frame(x,y) #création du dataframe a partir des deux vecteurs
data.matrix<- data.frame(x,y)
#as.data.frame : transformation d'une matrice en dataframe
#data.matrix : transformation d'une dataframe en matrice

str(mondatafr) #visualisation de mon dataframe
View(mondatafr) #visualisation en tableau de mon datafr



# Manipuler les données ---------------------------------------------------


# Importer les données ----------------------------------------------------

setwd("C:/Users/allak/Desktop/R fichiers") #set as work directory ou en tapant setwd() appuyer sur tabulation pour selectionner un repertoire


# Importation d'un fichier text -------------------------------------------

table <- read.table(file = "Data/donnees.txt", header = TRUE, sep = ";", dec = ",", row.names=1)
table1 <- read.table(file = "Data/alimentation.txt", header = TRUE, sep = " ")
summary(table) #verification des types de variables #str(table)
table2 <- read.csv(file="Data/Pima_wNA.csv")
summary(table2)


# Manipuler les variables --------------------------------


# Changer de type ---------------------------------------------------------

is.factor(table$boursier)
is.numeric(table$boursier)

table$boursier <- as.factor(table$boursier)
table$boursier <- as.numeric(as.character(table$boursier))


# Decoupage en classe -----------------------------------------------------

#decoupage réalisé selon les seuils choisis par l'utilisateur
set.seed(654) #on fixe la graine
X <- rnorm(15,mean = 0, sd = 1)# creation d'un vecteur avec loi normale centrée reduite
print(X)

# ]minimum, -0.2]  ]-0.2, 0.2]  ]0.2, maximum] #Decoupage en trois classes
Xqual <- cut(X, breaks = c(min(X), -0.2, 0.2, max(X)),include.lowest = TRUE)
Xqual
table(Xqual) #Résume du nombre d'observation de decoupage

## CCL : Effectif desequilibré

#Decoupage automatique pour avoir des effectifs equlibrés et representatifs d'une population
#Il est important d'equilibrer pour faire une bonne analyse
decoupe <- quantile(X)# les elements qui divisent une distribution statistique en 4 parties d'effectif egal
decoupe
decoupe1 <- quantile(X,probs = seq(0,1, length = 4)) #length sort la longueur du vecteur
decoupe1
Xqual <- cut(X, breaks = decoupe1, include.lowest = TRUE)
Xqual
?include.lowest
?cut
table(Xqual) #Les intervalles qui departagent les effectifs decoupés


# Travail sur le niveau des facteurs --------------------------------------

##Changer les intitulés des niveaux
levels(Xqual) <- c("niv1","niv2","niv3")
levels(Xqual)

##Fusionner deux niveaux
levels(Xqual) <- c("niv1","niv2","niv1") #On a fusionner le niveau 1 et l'ancien niveau 3
levels(Xqual)
table(Xqual)

#Changer de reference de niveau
X <- c(1,2,2,2,3)
Xqual <- factor(X,labels = c("classique","nouveau","placebo"))
Xqual 


# Manipuler les individus -------------------------------------------------

### Repérer les données manquantes
set.seed(23)
variable <- rnorm(10, 0, 1)
variable[c(3,4,5)] <- NA
variable
select <- is.na(variable)
select
which(select) #donne les indices des TRUE
variable2 <- variable[!select]#Selectionne les valeurs qui ne comprennent pas les NA #C'est la negation
variable2
variable3 <- variable[-which(select)]#Negation toujours mais avec la fonction which pour afficher toutes les valeurs sans prendre en compte les NA
variable3
###Reperer les individus aberants univariés
#installation d'une librairie| bibliotheque |module
library(rpart)
data(kyphosis)
boxplot(kyphosis[, "Number"]) #boites à mouches #affiche la variable number et les individus aberants
kyphosis$Number #Selectionne la variable "number" et affiche cette variable
resultat <- boxplot(kyphosis[, "Number"])
val_aberant <- resultat$out #afficher les valeurs aberantes sans savoir quelles sont les individus aberants
val_aberant
which(kyphosis$Number %in% val_aberant)#la fonction nous permet d'afficher cette fois ci les individus aberants

###Reperer ou eliminer les doublons

X <- data.frame(C1=rep(c("a","b","a"),times=c(1,2,2)),c2=c(1,2,2,3,1))
out.doublon <- unique(X)#Reunir les doublons en une ligne
duplicated(X)
only_doublon <- X[duplicated(X),] #afficher les doublons


##Concatener les tableaux de données

#On créer des matrices et on surnomme les lignes et les colonnes

X <- matrix(c(1,2,3,4),2,2)
X
row.names(X) <- paste("ligne", 1:2, sep=" ")
X
colnames(X) <- paste("X",1:2,sep="")
X
Y <- matrix(11:16, 3,2)
Y
colnames(Y) <- paste("Y",1:2, sep="")
Y

#Concatener par ligne les deux matrices

Z <- rbind(X,Y)
Z

#Tranformons les matrces X et Y en data frame et concatenons les data frame
Xd <- as.data.frame(X)
Xd
Yd <- as.data.frame(Y)
Yd

Zd <-rbind(Xd,Yd)

#Concatener par colonne

X <- matrix(c(1,2,3,4),2,2)
row.names(X) <- paste("ligne",1:2, sep="")
colnames(X) <- paste("X",1:2, sep="")
X
Y <- matrix(11:16,2,3)
Y
colnames(Y) <- paste("Y",1:3, sep="")
Y
Xd <- as.data.frame(X)
Yd <- as.data.frame(Y)
cbind(Xd,Yd) #concatener par colonne


# Visualisation de données ------------------------------------------------

##Les graphiques conventionnels

data("airquality")
View(head(airquality))
plot(x = airquality$Wind, y = airquality$Ozone)
plot(Ozone~Wind, data = airquality)
plot(Ozone~Wind, data = airquality, xlab= "vent",ylab = "ozone")

#Creer une nouvelle variable dans un dataframe
airquality$Max <- NA
airquality$zone <- cut(airquality$Wind, breaks = quantile(airquality$Wind))
levels(airquality$zone) <- c("Est","Nord","Ouest","Sud")
table(airquality$zone, airquality$Wind) #Nous permet d'avoir une idée sur la quantité de vent dans chaque zone

boxplot(Ozone~zone, data = airquality) #visualisation graphique avec des valeurs aberantes
boxplot(Wind~zone, data = airquality)

#Utilisation d'une seule variable avec plot

plot(airquality[, "Wind"])
plot(airquality$Wind)#Une autre façon d'afficher la ligne précedente.

plot(airquality$Wind, cex=0.5) #Cex permet de modifier les nuages de points en ayant des plus grands ou plus petits
plot(airquality$Wind, cex=0.5, pch=12) #Pch permet de changer des cercles en croix ou point etc..
#on peut rajouter la commande type="o" ou "l" ou "p" pour relier les points graphiques avec des lignes etc..
#on peut changer la couleur de notre graphique en utilisant la fonction col="red" pour la couleur rouge

#Répresentation d'une distribution

#Histogramme
hist(airquality$Wind, main="Histogramme Vent", probability = FALSE, xlab = "vent", col = "lightblue")

#Graphique Barplot
plot(airquality$zone, col=1:4)
plot(airquality$zone, col= c("green", "black","yellow","red")) #On peut preciser les couleurs de chaque barre

library(ggplot2)
data("diamonds")
set.seed(1234)
diamonds2 <- diamonds[sample(nrow(diamonds), 5000),] #selection de 5000 observation au hasard de notre dataframe diamonds
ggplot(diamonds2) + aes(x=cut)+geom_bar()
ggplot(diamonds2) + aes(x=price)+geom_histogram()
ggplot(diamonds2) + aes(x=carat, y=price)+geom_point() #representation de deux elements (carats et prix) en nuage de point.
#S'il faut ajouter des options, il  faut se mettre dans le aes pour y rajouter les options sauf la couleur qui se rajoute au niveau de la geometrie(geom)
