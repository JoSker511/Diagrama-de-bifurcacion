# Análisis del Comportamiento de las Conexiones a Internet mediante el Mapeo Logístico

**Autores:** Juan Niño, Oscar Mateo Arrubla y Jose Santiago Gonzalez

En este Taller se analiza el comportamiento de las conexiones a internet mediante el uso de Mapeo Logístico, a través de un diagrama de bifurcación y el cálculo del exponente Lyapunov. Se analizará el comportamiento del sistema hasta llegar al caos y se discutirá el hecho de que internet sea un sistema al borde del caos.

Para este proyecto usamos un script Python el cual genera 5 gráficas distintas las cuales nos ayudan a analizar las conexiones de internet.

---

## Figura 1 — Diagrama de Bifurcación

En este diagrama podemos ver en el eje vertical la utilización del enlace `x` y en el eje horizontal se puede ver el valor de `r` el cual va incrementando desde 1 hasta 4. En este caso se puede ver que cuando el valor de `r` tiene un valor de 1–3 existe una sola línea curva, esto nos indica que la red converge en el mismo estado de carga sin importar donde empieza. Cuando llegamos a `r = 3` se puede ver la primera bifurcación donde se divide en dos. Una vez llegamos a `r = 3.57` llegamos al caos; se puede evidenciar una nube de puntos generada por las continuas bifurcaciones.

Este diagrama nos permite ver cómo la red se comporta de manera única y su característica emergencia, siendo esta más evidente cuando vemos la ecuación de donde sale el diagrama:

$$x_{n+1} = r x_n (1 - x_n)$$

Como se puede ver, esta es la ecuación de una sola línea; no se puede evidenciar en ningún punto algo indicativo sobre el caos que se genera en la Figura 1.

---

## Figura 2 — Estructura de Bifurcación: Detalle del Borde del Caos

Se dice que los fenómenos emergentes se generan en la ausencia de cualquier controlador central. Esto lo demuestra porque ningún valor de `x_n` "decide" hacia dónde va el sistema; cada punto simplemente aplica la misma regla local y el atractor global emerge de esa interacción. No hay un punto especial que controle a los demás. La estructura del diagrama —las ramas, las bifurcaciones, las ventanas— aparecen sin que nadie la coordine.

---

## Figura 3 — Series de Tiempo: Sensibilidad a Condiciones Iniciales por Régimen

En estas gráficas tenemos una versión ampliada de porciones específicas de la gráfica para valores de `r` a lo largo del tiempo. Podemos observar el estado estable con `r = 2.5` y cómo, acercándonos a `3.57`, la gráfica comienza a variar más hasta bifurcarse en diferentes periodos; es decir, que progresivamente se pierde toda estabilidad haciendo que mínimos cambios en `r` sean suficientes para traer mayores cambios a la gráfica, siendo un sistema cada vez más sensible a sus condiciones iniciales.

De forma resumida:

| Régimen | Valor de r | Comportamiento |
|---|---|---|
| **Estable** | r ≈ 2.5 | La carga converge a un único valor fijo, sin importar la condición inicial. |
| **Período 2** | r ≈ 3.2 | La carga alterna entre dos valores, generando una oscilación constante. |
| **Período 4** | r ≈ 3.5 | La carga sigue un ciclo repetitivo de cuatro estados, aumentando la complejidad. |
| **Borde del caos** | r ≈ 3.57 | El sistema presenta máxima sensibilidad; pequeñas variaciones generan cambios grandes. |
| **Caótico** | r ≈ 3.75 | La carga no sigue un patrón definido y se vuelve impredecible. |
| **Caos máximo** | r = 4.0 | El sistema es completamente inestable, sin repetición ni posibilidad de predicción. |

---

## Figura 4 — Exponente de Lyapunov: Cuantificación del Caos en Internet

Esta figura tiene dos paneles que se leen juntos. El panel superior es el diagrama de bifurcación de referencia y el panel inferior es el **Exponente de Lyapunov (λ)**.

`λ` mide qué tan rápido se separan dos trayectorias que comenzaron casi en el mismo punto, como por ejemplo dos conexiones de internet con una diferencia inicial de apenas `0.001`.

- **Cuando λ < 0** (zona verde): las trayectorias convergen; el sistema olvida sus condiciones iniciales. Los valles que se hunden hasta -2 ocurren exactamente en los puntos de bifurcación, donde el sistema cambia de ciclo y se vuelve momentáneamente estable.
- **Cuando λ cruza el 0** (línea naranja punteada): una diferencia inicial de `0.001` comienza a crecer exponencialmente (caos matemático).
- **Cuando λ > 0** (zona roja): se puede ver un pico negativo alrededor de `3.83`; es una isla de orden dentro del caos donde el sistema vuelve a ser predecible temporalmente, antes de caer de nuevo en el caos.

Como ejemplo, si `r` cae en `3.57`, variaciones mínimas como un paquete retrasado se amplifican y producen cascadas de congestión que pueden experimentarse como internet lento. El exponente de Lyapunov convierte esa intuición en un número preciso.

---

## Figura 5 — Diagramas de Telaraña (Cobweb)

Los diagramas de telaraña (*cobweb*) muestran la dinámica iterativa visualmente. Cada paso del sistema es un rebote: vas a la curva logística, luego a la diagonal, luego a la curva otra vez.

- Para el **régimen estable**: el rebote converge a un punto fijo.
- Para **período 2**: queda un cuadrado.
- Para el **caos**: el rebote llena toda la curva sin repetirse.

Es útil para explicar *cómo* el sistema llega a sus atractores, no solo dónde están.
