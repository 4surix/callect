# Callect

<img align="right" width="100" height="100" src="https://cdn.discordapp.com/attachments/500372755770769408/720442173723770950/callect_logo.png">
   
`Callect` est un petit langage de programmation orienté objet, fonctionnel et événementiel fait en `Python`.    
  
J'essaye de faire en sorte qu'il soit le mieux possible.  
Ce langage m'aide à progresser.  
J'y insère différentes idées/concepts que j'aime bien et que je pense utile.  
  
Merci aux personnes qui prendront le temps de lire, voir même de tester le langage, et feront des retours ! ❤️  
  
Pour en savoir plus, lisez le [wiki](https://github.com/4surix/callect/wiki) ! Bonne lecture ! ✨  

# Aperçu

```lua
math = import{'math'}

pouet = 12

// On fait la factoriel de 12
//
resultat = math.fact{pouet}

if resultat > 100 [
    print{'Cela fait beaucoup.'}
]
elif resultat < 10 [
    print{"Ce n'est pas beaucoup."}
]
else [
    print{'oui'}
]

fruits = {
    'pomme',
    'poire',
    'fraise',
    'orange'
}

panier = {}

for fruit in fruits [
    panier.add{fruit}
]

@'verif_nombre_pair' {valeur:nbr} [
    // Si le résultat du modulo (donc le reste) est égal à 0
        alors il renvoie 1 (vrai) car c'est un nombre pair
        sinon il renvoie 0 (faux) 
    //
    return valeur % 2 == 0
]

pharses = {
    0 = 'Il est impair !',
    1 = 'Il est pair !'
}
resultat = phrases # verif_nombre_pair{13}
resultat == phrases # 0
```

# Temps

Le temps d'exéution n'est vraiment pas le point fort du langage, mais cela vous donne une idée de sa lenteur.  
  
## Fonction d'Ackermann

```lua
@'ackermann' {m, n} [
    if m == 0 [
        return n + 1
    ]
    elif n == 0 [
        return ackermann{m - 1, 1}
    ]
    else [
        return ackermann{m - 1, ackermann{m, n - 1}}
    ]
]

ackermann{3, 3} == 61
```
  
**0.7651 secondes**

## Différence entre `event changevars` et `if`

```lua
event changevars (pomme == "rouge") [
    poire = "verte"
]

pomme = "rouge"
```

**0,0015 secondes**  
  
```lua
pomme = "rouge"

if pomme == "rouge" [
    poire = "verte"
]
```

**0,0015 secondes**

## Différence entre `for` et `repeat`

```lua
for a in 1000 []
```

**0,0156 secondes**  
  
```lua
repeat 1000 []
```

**0,0100 secondes**

## Différence entre une addition normal et personnalisée

```lua
a = 1

a + 1
```

**0,0010 secondes**  
  
```lua
@'objet_avec_addition' {
    @'add__' self parent {b} [return 1 + b]
} []

a = objet_avec_addition{}

a + 1
```

**0,0015 secondes**
