# MANUAL VISUAL DE ASTRO ARCADE
## Guía para crear naves del jugador, enemigos y jefes finales

Este documento recoge los identificadores, parámetros y posibilidades visuales de los tres sistemas de renderizado de Astro Arcade.

Su objetivo es servir como referencia para crear nuevos diseños mediante archivos JSON sin introducir propiedades que el código no reconozca o que no produzcan ningún efecto visual.

---

# 1. NAVES DEL JUGADOR — ShipRenderer

Las naves del jugador utilizan `ShipConfig`, `ShipVisualConfig` y `ShipRenderer`.

El renderizador trabaja sobre un espacio de referencia de **64 × 76 píxeles**. La nave se construye mediante diferentes capas, dibujadas en este orden:

1. Motores.
2. Aletas.
3. Alas.
4. Cuerpo.
5. Cañones.
6. Cabina.
7. Detalles.

Este orden es importante porque determina qué elementos quedan por delante de otros.

## 1.1. Formas del cuerpo (`visual.shape`)

El método `_buildBodyPath()` reconoce las siguientes formas:

| Identificador | Diseño | Características |
|---|---|---|
| `interceptor` | Interceptor | Fuselaje estrecho y puntiagudo. |
| `rocket` | Cohete | Cuerpo estrecho y alargado. |
| `fighter` | Caza | Fuselaje de combate con hombros anchos. |
| `bomber` | Bombardero | Cuerpo ancho y robusto. |
| `heavy` | Pesado | Laterales gruesos y parte trasera amplia. |
| `drone` | Dron | Geometría compacta y angular. |
| `stealth` | Sigilo | Silueta afilada y alas integradas visualmente. |
| `assault` | Asalto | Fuselaje agresivo con extremos pronunciados. |
| `diamond` | Diamante | Geometría romboidal. |
| `manta` | Manta | Silueta inspirada en una mantarraya. |
| `saucer` | Platillo | Cuerpo redondeado y simétrico. |
| `twin_hull` | Doble fuselaje | Cuerpo central y dos módulos laterales. |
| Valor desconocido | Interceptor | Se utiliza la geometría predeterminada. |

**Importante:** el valor predeterminado no es una geometría independiente. Si se introduce una forma no reconocida, se utiliza el diseño de `interceptor`.

## 1.2. Estilos de alas (`wings.style`)

| Identificador | Diseño |
|---|---|
| `swept` | Alas inclinadas hacia atrás. |
| `delta` | Alas triangulares. |
| `wide` | Alas anchas y extendidas. |
| `heavy` | Alas gruesas y robustas. |
| `split` | Alas divididas con una punta secundaria. |
| `curved` | Alas con varios ángulos que simulan un perfil curvado. |
| `angular` | Alas agresivas con múltiples quiebros. |
| `winglets` | Alas con pequeñas extensiones en los extremos. |

Si se introduce un estilo desconocido, se utiliza `swept`.

**Parámetros:**

| Campo | Función |
|---|---|
| `enabled` | Activa o desactiva las alas. |
| `span` | Anchura o extensión de las alas. |
| `frontPosition` | Posición longitudinal de la parte delantera. |
| `rearPosition` | Posición longitudinal de la parte trasera. |
| `tipLength` | Longitud adicional de las puntas. |
| `style` | Geometría de las alas. |

## 1.3. Aletas (`fins.style`)

| Identificador | Diseño |
|---|---|
| `standard` | Aleta convencional. |
| `swept` | Aleta inclinada hacia atrás. |
| `wide` | Aleta ancha. |
| `delta` | Aleta triangular. |

**Parámetros:**

| Campo | Función |
|---|---|
| `enabled` | Activa o desactiva las aletas. |
| `count` | Cantidad de aletas, limitada entre 0 y 4. |
| `position` | Posición longitudinal. |
| `size` | Tamaño de las aletas. |
| `style` | Geometría de las aletas. |

Si se introduce un estilo desconocido, se utiliza `standard`.

## 1.4. Cabinas (`cockpit.style`)

El renderizador admite estos estilos:

| Identificador | Diseño |
|---|---|
| `armored` | Cabina convencional blindada. |
| `panoramic` | Cabina más ancha. |
| `bubble` | Cabina ovalada y redondeada. |
| `recessed` | Cabina con marco interior reforzado. |
| `compact` | Cabina reducida. |
| `elongated` | Cabina alargada. |
| `cockpitless` | Sin cabina. |

**Parámetros:**

| Campo | Función |
|---|---|
| `enabled` | Activa o desactiva la cabina. |
| `position` | Posición de la cabina. |
| `width` | Anchura. |
| `length` | Longitud. |
| `style` | Estilo visual. |

Los estilos desconocidos utilizan la geometría convencional.

## 1.5. Motores (`engines`)

Los motores tienen una animación de llama basada en `elapsedTime`.

| Campo | Función |
|---|---|
| `count` | Número de motores, limitado entre 0 y 8. |
| `position` | Posición vertical. |
| `separation` | Separación horizontal entre motores. |
| `size` | Tamaño de los motores. |
| `glow` | Activa o desactiva el resplandor exterior. |

La llama cambia de longitud durante la animación y utiliza un degradado entre el color del motor, el núcleo y el blanco.

## 1.6. Cañones (`cannons`)

| Campo | Función |
|---|---|
| `count` | Número de cañones, limitado entre 0 y 6. |
| `position` | Posición vertical. |
| `separation` | Separación horizontal. |
| `size` | Tamaño de los cañones. |

Los cañones son elementos exclusivamente visuales. El tipo de arma, su daño y sus estadísticas se configuran mediante los campos de armamento de la nave, no mediante este apartado.

## 1.7. Cuerpo (`body`)

| Campo | Función |
|---|---|
| `length` | Longitud del fuselaje. |
| `width` | Anchura del fuselaje. |
| `noseLength` | Longitud o referencia de la punta. |
| `rearWidth` | Anchura relativa de la parte trasera. |
| `armorPlates` | Activa los detalles de blindaje. |

Los parámetros numéricos tienen límites internos para evitar proporciones excesivas.

**Matiz técnico:** `length`, `width`, `rearWidth` y `noseLength` no afectan por igual a todas las formas. Algunas geometrías tienen trazados especiales y no utilizan todos los parámetros del trazado genérico.

## 1.8. Detalles (`details`)

| Campo | Función |
|---|---|
| `panelLines` | Dibuja líneas de paneles. |
| `wingLights` | Añade luces en las alas. |
| `armorSegments` | Dibuja segmentos de blindaje. |
| `engineGlow` | Añade resplandor decorativo a los motores. |
| `cockpitReflection` | Añade reflejos a la cabina. |
| `rivets` | Añade remaches decorativos. |

`rivets` también está soportado por el renderizador, aunque no aparecía en el JSON inicial.

## 1.9. Colores de la nave

`ShipVisualConfig` contempla los siguientes colores:

| Campo | Función |
|---|---|
| `primaryColor` | Color principal del fuselaje. |
| `secondaryColor` | Superficies secundarias. |
| `tertiaryColor` | Tercer color de la nave. |
| `cockpitColor` | Color de la cabina. |
| `cockpitGlassColor` | Color del cristal de la cabina. |
| `outlineColor` | Color del contorno. |
| `engineColor` | Color exterior de los motores. |
| `engineCoreColor` | Color del núcleo de la llama. |
| `weaponColor` | Color de los elementos de armamento. |
| `detailColor` | Color de los detalles. |

---

# 2. ENEMIGOS — EnemyRenderer

Los enemigos utilizan `EnemyVisualConfig` y `EnemyRenderer`.

Su estructura visual es más sencilla que la de las naves del jugador. Utiliza una silueta principal y diferentes elementos configurables para personalizar alas, cabina, motores, aletas y detalles.

## 2.1. Geometrías disponibles (`shape`)

El renderizador que hemos trabajado incorpora estas 13 siluetas:

| Identificador | Geometría | Uso orientativo |
|---|---|---|
| `interceptor` | Caza estrecho y puntiagudo. | Enemigo rápido. |
| `fighter` | Caza convencional. | Enemigo básico. |
| `bomber` | Cuerpo ancho. | Enemigo de ataque pesado. |
| `drone` | Estructura compacta. | Unidad ligera. |
| `heavy` | Fuselaje robusto. | Unidad resistente. |
| `rocket` | Forma alargada. | Unidad veloz. |
| `stealth` | Silueta angular. | Unidad especializada. |
| `cruiser` | Estructura ancha. | Enemigo grande. |
| `manta` | Forma extendida. | Unidad alienígena. |
| `twin_hull` | Doble fuselaje. | Unidad especial. |
| `saucer` | Forma redondeada. | Unidad extraterrestre. |
| `diamond` | Geometría romboidal. | Unidad ligera. |
| `assault` | Cuerpo de ataque reforzado. | Unidad ofensiva. |

Estos identificadores corresponden a las formas incorporadas en la versión del renderizador que hemos trabajado.

## 2.2. Dimensiones

Ejemplo:

```json
"dimensions": {
  "width": 46,
  "height": 38
}
```

| Campo | Función |
|---|---|
| `width` | Anchura de referencia del dibujo. |
| `height` | Altura de referencia del dibujo. |

Son las dimensiones utilizadas para construir el dibujo. No representan necesariamente el tamaño final del enemigo en pantalla, ya que este puede depender también de la escala aplicada por el juego.

## 2.3. Colores

| Campo | Función |
|---|---|
| `primary` | Cuerpo principal. |
| `secondary` | Superficies secundarias. |
| `accent` | Detalles luminosos y elementos destacados. |
| `cockpit` | Cabina u ojo. |
| `engine` | Motores. |
| `outline` | Contorno. |

Los enemigos pueden utilizar un lenguaje de color propio para distinguirlos de las naves del jugador.

## 2.4. Alas (`wings`)

Ejemplo:

```json
"wings": {
  "enabled": true,
  "style": "swept",
  "span": 1.15
}
```

**Parámetros:**

| Campo | Función |
|---|---|
| `enabled` | Activa o desactiva las alas. |
| `style` | Geometría de las alas. |
| `span` | Extensión lateral. |

**Estilos incorporados:**

| Identificador | Diseño |
|---|---|
| `swept` | Inclinadas hacia atrás. |
| `delta` | Triangulares. |
| `wide` | Anchas. |
| `heavy` | Gruesas y robustas. |
| `angular` | Angulosas. |
| `split` | Divididas. |
| `curved` | Curvadas. |
| `winglets` | Con extensiones en los extremos. |

## 2.5. Cabina (`cockpit`)

Ejemplo:

```json
"cockpit": {
  "enabled": true
}
```

El campo `enabled` permite mostrar u ocultar la cabina.

En el modelo actual no tenemos definidos parámetros independientes de posición, longitud o anchura como en las naves del jugador.

## 2.6. Motores (`engines`)

Ejemplo:

```json
"engines": {
  "enabled": true,
  "count": 1
}
```

| Campo | Función |
|---|---|
| `enabled` | Muestra u oculta los motores. |
| `count` | Número de motores. |

## 2.7. Aletas (`fins`)

Ejemplo:

```json
"fins": {
  "enabled": true
}
```

El campo `enabled` permite activar o desactivar las aletas.

## 2.8. Detalles (`details`)

Ejemplo:

```json
"details": {
  "enabled": true,
  "armorSegments": false
}
```

| Campo | Función |
|---|---|
| `enabled` | Activa o desactiva los detalles visuales. |
| `armorSegments` | Muestra divisiones de blindaje. |

## 2.9. Ejemplo completo de configuración visual de enemigo

```json
"visual": {
  "shape": "heavy",
  "dimensions": {
    "width": 58,
    "height": 48
  },
  "colors": {
    "primary": "#7B344B",
    "secondary": "#C15A70",
    "accent": "#FFB04D",
    "cockpit": "#FF536B",
    "engine": "#FF8C32",
    "outline": "#321525"
  },
  "wings": {
    "enabled": true,
    "style": "heavy",
    "span": 1.35
  },
  "cockpit": {
    "enabled": true
  },
  "engines": {
    "enabled": true,
    "count": 3
  },
  "fins": {
    "enabled": true
  },
  "details": {
    "enabled": true,
    "armorSegments": true
  }
}
```

---

# 3. JEFES FINALES — BossRenderer

Los jefes utilizan `BossVisualConfig` y `BossRenderer`.

Su sistema está diseñado para criaturas de mayor tamaño y complejidad visual. En lugar de utilizar una cabina convencional, pueden presentar ojos, núcleos energéticos, tentáculos, pinzas, espinas y otras estructuras.

## 3.1. Tipos de criaturas (`creatureType`)

En la versión del renderizador que hemos revisado se encuentran implementadas estas cuatro familias:

| Identificador | Diseño | Elementos característicos |
|---|---|---|
| `tentacles` | Criatura tentacular. | Tentáculos, ojo central y ojos secundarios. |
| `armored` | Criatura acorazada. | Pinzas y estructuras defensivas. |
| `multi_eye` | Criatura de múltiples ojos. | Ojos flotantes alrededor del cuerpo. |
| `spiked` | Criatura espinosa. | Espinas y ojos secundarios. |

Además, hemos planteado cuatro familias adicionales para ampliar el catálogo:

| Identificador propuesto | Diseño | Elementos que podría incorporar |
|---|---|---|
| `leviathan` | Leviatán. | Cabeza alargada, aletas y cuerpo segmentado. |
| `insectoid` | Insecto gigante. | Patas articuladas, exoesqueleto y mandíbulas. |
| `demon` | Criatura demoníaca. | Cuernos, brazos, ojos y boca. |
| `core` | Núcleo energético. | Anillos y núcleo luminoso pulsante. |

**Importante:** las cuatro últimas familias son propuestas de ampliación. No deben utilizarse como identificadores implementados hasta comprobar que se han añadido expresamente al `BossRenderer` definitivo.

## 3.2. Dimensiones

Ejemplo:

```json
"width": 220,
"height": 145
```

| Campo | Función |
|---|---|
| `width` | Anchura de referencia del jefe. |
| `height` | Altura de referencia del jefe. |

Son dimensiones de referencia del dibujo. Los jefes pueden ocupar mucho más espacio que los enemigos normales.

## 3.3. Colores

| Campo | Función |
|---|---|
| `primaryColor` | Cuerpo principal. |
| `secondaryColor` | Placas, segmentos y superficies secundarias. |
| `accentColor` | Elementos luminosos y efectos. |
| `cockpitColor` | Ojo, núcleo o elemento central. |
| `outlineColor` | Contorno de la criatura. |

En los jefes no es necesario que exista una cabina convencional. `cockpitColor` puede utilizarse para colorear ojos o núcleos.

## 3.4. Parámetros adicionales

Ejemplo:

```json
"wingSpan": 1.55,
"engineCount": 4
```

| Campo | Función |
|---|---|
| `wingSpan` | Factor de extensión disponible en la configuración visual. |
| `engineCount` | Número de motores configurado. |

**Advertencia técnica:** estos campos existen en `BossVisualConfig`, pero no debemos asumir que el renderizador los utiliza para construir las geometrías de todas las criaturas. Que un parámetro exista en el modelo no significa necesariamente que modificarlo produzca un cambio visual.

## 3.5. Orientación artística de las familias

Estas son propuestas de diseño para mantener variedad entre los jefes:

**Tentáculos**
- Colores: morado, rojo oscuro y rosa.
- Elemento central: ojo luminoso.
- Ideal para criaturas orgánicas y alienígenas.

**Armored**
- Colores: gris, acero y naranja.
- Cuerpo ancho y estructuras defensivas.
- Ideal para jefes resistentes.

**Multi-eye**
- Colores: verde, azul y violeta.
- Múltiples ojos alrededor del cuerpo.
- Ideal para criaturas extrañas.

**Spiked**
- Colores: negro, rojo y púrpura.
- Espinas alrededor del cuerpo.
- Ideal para enemigos agresivos.

**Leviathan — propuesta**
- Colores: azul oscuro, verde y turquesa.
- Cuerpo segmentado y aletas.
- Ideal para jefes de gran tamaño.

**Insectoid — propuesta**
- Colores: verde ácido, amarillo y marrón.
- Patas articuladas y mandíbulas.
- Ideal para criaturas biomecánicas.

**Demon — propuesta**
- Colores: rojo, negro y naranja.
- Cuernos, brazos y rostro.
- Ideal para jefes intimidantes.

**Core — propuesta**
- Colores: azul eléctrico, cian y violeta.
- Núcleo luminoso y anillos.
- Ideal para jefes mecánicos o energéticos.

## 3.6. Ejemplo JSON de jefe

Hay un detalle importante en el modelo actual: `BossVisualConfig.fromJson()` lee `creatureType` dentro de `visual`, no en el nivel superior de `BossConfig`.

Por tanto, la estructura correcta es:

```json
{
  "id": "sector_01_boss",
  "name": "Destructor de la Frontera",
  "health": 500,
  "speed": 85,
  "contactDamage": 2,
  "score": 5000,

  "movementPattern": "patrol",
  "movementAmplitude": 75,

  "projectileDamage": 1,
  "projectileSpeed": 190,
  "attackInterval": 1.8,
  "projectileCount": 3,
  "spreadAngle": 12,

  "visual": {
    "creatureType": "tentacles",
    "width": 220,
    "height": 145,

    "primaryColor": "#642B43",
    "secondaryColor": "#A83C59",
    "accentColor": "#FF536B",
    "cockpitColor": "#55E6FF",
    "outlineColor": "#241323",

    "wingSpan": 1.55,
    "engineCount": 4
  },

  "phases": [
    {
      "healthThreshold": 0.4,
      "movementPattern": "zigzag",
      "speedMultiplier": 1.45,
      "attackInterval": 1.3,
      "projectileCount": 5,
      "spreadAngle": 20
    }
  ]
}
```

---

# 4. DIFERENCIAS ENTRE LOS TRES SISTEMAS

| Característica | Jugador | Enemigo | Jefe |
|---|---|---|---|
| Configuración | `ShipVisualConfig` | `EnemyVisualConfig` | `BossVisualConfig` |
| Renderizador | `ShipRenderer` | `EnemyRenderer` | `BossRenderer` |
| Geometría principal | Fuselaje | Silueta de nave | Criatura |
| Alas | Personalizables | Personalizables | No son alas convencionales |
| Cabina | Varios estilos | Activar/desactivar | Ojo o núcleo |
| Motores | Personalizables | Activar/desactivar | Campo disponible, uso visual por verificar |
| Cañones visuales | Sí | No forman parte de la configuración descrita | No forman parte de la configuración descrita |
| Extremidades | Aletas | Aletas | Tentáculos, pinzas y otras estructuras |
| Detalles | Paneles, blindaje y luces | Detalles y blindaje | Elementos propios de cada criatura |
| Colores configurables | 10 | 6 | 5 |

---

# 5. REGLAS PARA CREAR DISEÑOS VARIADOS

Para evitar que el catálogo termine teniendo muchas naves que parecen iguales, conviene seguir estas reglas:

1. **No repetir siluetas:** dos naves no deberían parecer la misma con colores diferentes.
2. **Identidad visual por categoría:** las naves del jugador deben transmitir tecnología; los enemigos pueden ser cazas militares o alienígenas; los jefes deben resultar mucho más llamativos.
3. **Contraste:** los contornos deben separar claramente las diferentes piezas.
4. **Tamaño proporcional:** no utilizar demasiados detalles pequeños en enemigos de 40 píxeles.
5. **Motores reconocibles:** deben quedar visualmente separados del cuerpo.
6. **Cabinas visibles:** deben distinguirse del color principal.
7. **Jefes diferentes:** variar la silueta, no solamente los ojos y los colores.
8. **Animaciones moderadas:** deben aportar vida sin distraer durante el combate.

## 5.1. Propuesta de catálogo para las naves del jugador

| Nave | Forma del cuerpo | Alas | Características |
|---|---|---|---|
| Scout | `interceptor` | `swept` | Nave equilibrada con dos motores. |
| Phantom | `stealth` | `delta` | Cabina compacta y aspecto furtivo. |
| Titan | `bomber` | `heavy` | Cuerpo ancho y cuatro motores. |
| Viper | `twin_hull` | `split` | Doble fuselaje y diseño agresivo. |

## 5.2. Propuesta de catálogo para enemigos

| Enemigo | Forma recomendada | Identidad |
|---|---|---|
| Caza ligero | `interceptor` | Pequeño y rápido. |
| Bombardero | `bomber` | Grande y robusto. |
| Manta | `manta` | Alienígena y extendido. |
| Platillo | `saucer` | Redondeado y extraterrestre. |
| Crucero | `cruiser` | Grande y resistente. |
| Dron | `drone` | Compacto y mecánico. |

Estas son recomendaciones de diseño, no restricciones del código.

---

# 6. ADVERTENCIAS TÉCNICAS

Hay varios aspectos que conviene tener presentes al crear nuevos JSON.

### 6.1. No todos los parámetros afectan a todas las geometrías

Una propiedad puede existir en el JSON y en el modelo sin que todas las formas la utilicen.

Por ejemplo:
- Algunas geometrías de `ShipRenderer` tienen trazados específicos.
- Los detalles decorativos pueden estar dibujados en coordenadas fijas.
- Los parámetros de `BossVisualConfig` no necesariamente modifican todas las criaturas.

### 6.2. Coordenadas fijas

En `ShipRenderer`, algunos elementos, como determinadas luces de las alas, utilizan posiciones concretas.

Esto significa que no todos los detalles se adaptan automáticamente a cualquier anchura o geometría. Una nave muy ancha o muy estrecha puede necesitar ajustes visuales.

### 6.3. Límites numéricos

No todos los parámetros tienen los mismos límites internos.

Por ejemplo:
- Los motores limitan su cantidad entre 0 y 8.
- Los cañones limitan su cantidad entre 0 y 6.
- Las aletas limitan su cantidad entre 0 y 4.
- Otros parámetros, como `span` o `separation`, pueden no tener límites equivalentes.

Valores excesivos pueden provocar que algunas partes del dibujo salgan del espacio de referencia.

### 6.4. Probar cada combinación

Antes de incorporar una nave o enemigo al catálogo definitivo, conviene comprobar:
- Que la silueta se reconoce correctamente.
- Que no hay piezas superpuestas de forma indeseada.
- Que los motores y las alas quedan dentro del dibujo.
- Que los colores tienen suficiente contraste.
- Que el diseño sigue siendo reconocible durante el combate.

---

# 7. PLANTILLAS PARA CREAR NUEVOS CONTENIDOS

Las siguientes plantillas sirven como referencia visual. Los campos de estadísticas, desbloqueos y comportamiento deben completarse según los modelos JSON correspondientes.

## 7.1. Plantilla visual de nave del jugador

```json
{
  "visual": {
    "shape": "interceptor",
    "scale": 1.0,

    "primaryColor": "#55DFFF",
    "secondaryColor": "#267FA8",
    "tertiaryColor": "#163D5A",
    "cockpitColor": "#8BEAFF",
    "cockpitGlassColor": "#D9FAFF",
    "outlineColor": "#071B30",
    "engineColor": "#55DFFF",
    "engineCoreColor": "#FFFFFF",
    "weaponColor": "#FFB04D",
    "detailColor": "#A4EFFF",

    "body": {
      "width": 0.65,
      "length": 1.0,
      "noseLength": 0.25,
      "rearWidth": 0.35,
      "armorPlates": true
    },

    "wings": {
      "enabled": true,
      "style": "swept",
      "span": 0.8,
      "frontPosition": 0.35,
      "rearPosition": 0.75,
      "tipLength": 0.15
    },

    "fins": {
      "enabled": true,
      "style": "standard",
      "count": 2,
      "position": 0.8,
      "size": 0.15
    },

    "cockpit": {
      "enabled": true,
      "style": "armored",
      "position": 0.3,
      "width": 0.25,
      "length": 0.2
    },

    "engines": {
      "count": 2,
      "position": 0.9,
      "separation": 0.25,
      "size": 0.8,
      "glow": true
    },

    "cannons": {
      "count": 2,
      "position": 0.55,
      "separation": 0.6,
      "size": 0.8
    },

    "details": {
      "panelLines": true,
      "wingLights": true,
      "armorSegments": true,
      "engineGlow": true,
      "cockpitReflection": true,
      "rivets": false
    }
  }
}
```

## 7.2. Plantilla visual de enemigo

```json
{
  "visual": {
    "shape": "fighter",

    "dimensions": {
      "width": 46,
      "height": 38
    },

    "colors": {
      "primary": "#7B344B",
      "secondary": "#C15A70",
      "accent": "#FFB04D",
      "cockpit": "#FF536B",
      "engine": "#FF8C32",
      "outline": "#321525"
    },

    "wings": {
      "enabled": true,
      "style": "swept",
      "span": 1.15
    },

    "cockpit": {
      "enabled": true
    },

    "engines": {
      "enabled": true,
      "count": 2
    },

    "fins": {
      "enabled": true
    },

    "details": {
      "enabled": true,
      "armorSegments": false
    }
  }
}
```

## 7.3. Plantilla visual de jefe

```json
{
  "visual": {
    "creatureType": "tentacles",

    "width": 220,
    "height": 145,

    "primaryColor": "#642B43",
    "secondaryColor": "#A83C59",
    "accentColor": "#FF536B",
    "cockpitColor": "#55E6FF",
    "outlineColor": "#241323",

    "wingSpan": 1.55,
    "engineCount": 4
  }
}
```

**Nota:** las plantillas son referencias basadas en los modelos y renderizadores que hemos revisado. Antes de utilizar un campo nuevo, hay que confirmar que su nombre y estructura coinciden con el `fromJson()` correspondiente.

---

# 8. LISTA OFICIAL DE IDENTIFICADORES

Esta sección debe mantenerse actualizada cuando se modifique alguno de los renderizadores.

## ShipRenderer

- Shapes: `interceptor`, `rocket`, `fighter`, `bomber`, `heavy`, `drone`, `stealth`, `assault`, `diamond`, `manta`, `saucer`, `twin_hull`.
- Wings: `swept`, `delta`, `wide`, `heavy`, `split`, `curved`, `angular`, `winglets`.
- Fins: `standard`, `swept`, `wide`, `delta`.
- Cockpit: `armored`, `panoramic`, `bubble`, `recessed`, `compact`, `elongated`, `cockpitless`.

## EnemyRenderer

- Shapes: `interceptor`, `fighter`, `bomber`, `drone`, `heavy`, `rocket`, `stealth`, `cruiser`, `manta`, `twin_hull`, `saucer`, `diamond`, `assault`.
- Wings: `swept`, `delta`, `wide`, `heavy`, `angular`, `split`, `curved`, `winglets`.

## BossRenderer

- Familias confirmadas en la versión revisada: `tentacles`, `armored`, `multi_eye`, `spiked`.
- Familias propuestas para futuras ampliaciones: `leviathan`, `insectoid`, `demon`, `core`.

---

# 9. REGLA FINAL PARA EL DESARROLLO

La regla más importante para mantener Astro Arcade es la siguiente:

**El JSON no define por sí solo lo que el juego puede dibujar. El renderizador es quien determina qué identificadores y parámetros tienen efecto real.**

Por tanto, cada vez que añadamos una geometría, un estilo o una característica visual:

1. Se incorpora su implementación al renderizador.
2. Se comprueba que el modelo JSON puede recibir sus parámetros.
3. Se verifica que el `fromJson()` los interpreta correctamente.
4. Se añade el nuevo identificador a este manual.
5. Se crea un JSON de prueba.
6. Se comprueba visualmente en el juego.

Así tendremos un catálogo de naves, enemigos y jefes coherente, ampliable y documentado, sin propiedades ficticias ni configuraciones que parezcan funcionar pero que el código ignore.



1. Fondos procedurales — BackgroundRenderer
Hay 24 tipos de fondo disponibles. Todos se generan mediante Canvas, sin necesitar imágenes externas.
Identificador JSON	Nombre para el manual
estrellas	Campo de estrellas
nebulosa	Nebulosa espacial
asteroides	Campo de asteroides
desierto	Desierto
alienigena	Mundo alienígena
industrial	Complejo industrial
volcanico	Mundo volcánico
congelado	Mundo congelado
oceano	Mundo oceánico
jungla	Jungla
ciudad	Ciudad futurista
cementerio	Cementerio espacial
tormenta	Tormenta
cristal	Mundo de cristal
toxico	Mundo tóxico
digital	Entorno digital
galaxia	Galaxia
eclipse	Eclipse
ruinas	Ruinas
metal	Superficie metálica
nuclear	Zona nuclear
tormenta_arena	Tormenta de arena
profundo	Espacio profundo
dimensional	Dimensión desconocida

Configuración en el JSON:
"visual": {
  "background": "nebulosa",
  "music": "assets/audio/music/sector_01.mp3",
  "scrollSpeed": 35
}


El valor de background debe coincidir con uno de los identificadores anteriores. Si se introduce uno desconocido, el renderizador utiliza estrellas como fondo alternativo.



# Formaciones de enemigos

Astro Arcade dispone de ocho formaciones diferentes. Se seleccionan desde el JSON de cada oleada mediante el campo `formation`.

Todas las formaciones son estáticas en el momento de aparición. Una vez colocados, los enemigos continúan con su movimiento habitual.

## 1. line — Línea horizontal

Distribuye los enemigos horizontalmente por la pantalla, manteniendo una separación uniforme.

## 2. v — Formación en V

Coloca los enemigos formando una V alrededor del centro, alternando sus posiciones a izquierda y derecha.

## 3. random — Aleatoria

Genera una posición horizontal aleatoria para cada enemigo dentro de los límites de la pantalla.

## 4. columns — Columnas

Distribuye los enemigos en varias columnas verticales, formando una cuadrícula.

## 5. diamond — Rombo

Distribuye los enemigos siguiendo el perímetro de un rombo, alrededor de un punto central.

## 6. circle — Círculo

Coloca los enemigos alrededor de una circunferencia, formando un anillo.

## 7. diagonal — Diagonal

Distribuye los enemigos siguiendo una línea diagonal oblicua, desde la parte inferior izquierda hacia la superior derecha.

## 8. cross — Cruz

Distribuye los enemigos en dos brazos perpendiculares: uno horizontal y otro vertical.

## Configuración JSON

Cada grupo de enemigos puede utilizar una formación diferente.

Ejemplo:

{
  "type": "scout_enemy",
  "count": 8,
  "formation": "diamond",
  "interval": 0.8
}

### Parámetros

- `type`: identificador del enemigo.
- `count`: cantidad de enemigos del grupo.
- `formation`: formación que utilizarán.
- `interval`: intervalo de aparición entre enemigos.

### Compatibilidad

- Las ocho formaciones funcionan con el sistema de oleadas.
- También pueden utilizarse en el modo Supervivencia.
- Los enemigos conservan su movimiento, disparos y colisiones habituales.
- Las posiciones horizontales se limitan a los márgenes de pantalla.
- Si se indica una formación desconocida, se utiliza `random`.
