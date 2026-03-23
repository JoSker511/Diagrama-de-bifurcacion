

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator

# ──────────────────────────────────────────────
# Parámetros globales
# ──────────────────────────────────────────────
WARMUP    = 500    
PLOTPTS   = 300    
R_MIN     = 1.0
R_MAX     = 4.0
STEPS     = 2000  

PALETTE = {
    "estable":  "#1D9E75",
    "periodo":  "#3B8BD4",
    "borde":    "#EF9F27",
    "caos":     "#E24B4A",
    "gray":     "#888780",
    "bg":       "#F8F7F4",
    "bg_dark":  "#1C1C1A",
    "text":     "#2C2C2A",
}

plt.rcParams.update({
    "figure.facecolor":  PALETTE["bg"],
    "axes.facecolor":    PALETTE["bg"],
    "axes.edgecolor":    "#C8C6BE",
    "axes.labelcolor":   PALETTE["text"],
    "axes.titlecolor":   PALETTE["text"],
    "xtick.color":       PALETTE["text"],
    "ytick.color":       PALETTE["text"],
    "grid.color":        "#DDDBD2",
    "grid.linewidth":    0.5,
    "grid.alpha":        0.8,
    "font.family":       "DejaVu Sans",
    "font.size":         10,
    "axes.titlesize":    11,
    "axes.labelsize":    10,
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "lines.linewidth":   1.2,
})


# ──────────────────────────────────────────────
# Funciones base
# ──────────────────────────────────────────────

def logistic(r, x):
    """Un paso del mapeo logístico."""
    return r * x * (1.0 - x)


def iterate(r, x0=0.5, warmup=WARMUP, n=PLOTPTS):
    """Retorna los n atractores luego del transitorio."""
    x = x0
    for _ in range(warmup):
        x = logistic(r, x)
    xs = []
    for _ in range(n):
        x = logistic(r, x)
        xs.append(x)
    return np.array(xs)


def time_series(r, x0=0.5, n=80):
    """Serie temporal de n pasos desde x0."""
    xs = [x0]
    for _ in range(n - 1):
        xs.append(logistic(r, xs[-1]))
    return np.array(xs)


def lyapunov(r_values, warmup=WARMUP, n=2000):
    """Exponente de Lyapunov para cada r."""
    exponents = []
    for r in r_values:
        x = 0.5
        for _ in range(warmup):
            x = logistic(r, x)
        le = 0.0
        for _ in range(n):
            x = logistic(r, x)
            deriv = abs(r * (1 - 2 * x))
            if deriv > 0:
                le += np.log(deriv)
            else:
                le = -np.inf
                break
        exponents.append(le / n)
    return np.array(exponents)


def region_color(r):
    """Color de región para un valor de r."""
    if r < 3.0:
        return PALETTE["estable"]
    elif r < 3.57:
        return PALETTE["periodo"]
    elif r < 3.62:
        return PALETTE["borde"]
    else:
        return PALETTE["caos"]


def bifurcation_data(r_min, r_max, steps=STEPS):
    """Computa datos del diagrama de bifurcación."""
    rs = np.linspace(r_min, r_max, steps)
    data = []
    for r in rs:
        pts = iterate(r)
        data.append((r, pts))
    return data


# ──────────────────────────────────────────────
# Función de anotación de régimen
# ──────────────────────────────────────────────

def shade_regimes(ax, y_min=0, y_max=1):
    """Sombrea las regiones del diagrama."""
    regimes = [
        (1.0,  3.0,   PALETTE["estable"], 0.07, "Estable\nr < 3"),
        (3.0,  3.57,  PALETTE["periodo"], 0.07, "Periódico\n3 ≤ r < 3.57"),
        (3.57, 3.62,  PALETTE["borde"],   0.15, "Borde\ndel caos"),
        (3.62, 4.0,   PALETTE["caos"],    0.07, "Caótico\nr > 3.57"),
    ]
    for (r1, r2, color, alpha, label) in regimes:
        ax.axvspan(r1, r2, alpha=alpha, color=color, zorder=0)
    ax.axvline(3.0,  color=PALETTE["periodo"], lw=0.8, ls="--", alpha=0.6)
    ax.axvline(3.57, color=PALETTE["borde"],   lw=0.8, ls="--", alpha=0.8)


# ══════════════════════════════════════════════
# FIGURA 1 – Diagrama de bifurcación completo
# ══════════════════════════════════════════════

def plot_bifurcation_full():
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor(PALETTE["bg"])

    data = bifurcation_data(R_MIN, R_MAX, steps=2000)

    for r, pts in data:
        color = region_color(r)
        ax.plot([r] * len(pts), pts, ",", color=color, alpha=0.35, markersize=0.6)

    shade_regimes(ax)

    # Anotaciones
    annotations = [
        (2.0,  0.85, "Punto fijo único\n(equilibrio de carga)",   PALETTE["estable"]),
        (3.25, 0.85, "Ciclos de congestión\n2 → 4 → 8 estados",  PALETTE["periodo"]),
        (3.83, 0.85, "Ventana\nperiodo 3",                        PALETTE["borde"]),
        (3.75, 0.15, "Cascadas\ncaóticas",                        PALETTE["caos"]),
    ]
    for rx, ry, txt, col in annotations:
        ax.annotate(txt, xy=(rx, ry), fontsize=8, color=col, ha="center",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=PALETTE["bg"],
                              edgecolor=col, alpha=0.85, linewidth=0.8))

    ax.set_xlim(R_MIN, R_MAX)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Parámetro r  (agresividad del tráfico)", labelpad=8)
    ax.set_ylabel("Utilización normalizada del enlace  $x_n$", labelpad=8)
    ax.set_title("Diagrama de bifurcación — Mapeo logístico aplicado a Internet", pad=12)
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.xaxis.set_minor_locator(MultipleLocator(0.1))
    ax.grid(True, which="major")
    ax.grid(True, which="minor", alpha=0.3)

    legend_patches = [
        mpatches.Patch(color=PALETTE["estable"], label="Estable  (r < 3)"),
        mpatches.Patch(color=PALETTE["periodo"], label="Periódico  (3 ≤ r < 3.57)"),
        mpatches.Patch(color=PALETTE["borde"],   label="Borde del caos  (r ≈ 3.57)"),
        mpatches.Patch(color=PALETTE["caos"],    label="Caótico  (r > 3.57)"),
    ]
    ax.legend(handles=legend_patches, loc="lower left", fontsize=8,
              framealpha=0.9, edgecolor="#C8C6BE")

    fig.tight_layout()
    fig.savefig("fig1_bifurcacion_completo.png", dpi=180, bbox_inches="tight")
    plt.close()
    print("✓  fig1_bifurcacion_completo.png")


# ══════════════════════════════════════════════
# FIGURA 2 – Zoom: borde del caos
# ══════════════════════════════════════════════

def plot_bifurcation_zoom():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.patch.set_facecolor(PALETTE["bg"])

    zooms = [
        (2.8, 4.0, 2000, "Zoom: cascada de bifurcaciones"),
        (3.5, 3.7, 3000, "Zoom: borde del caos (r ≈ 3.57)"),
    ]

    for ax, (r1, r2, steps, title) in zip(axes, zooms):
        data = bifurcation_data(r1, r2, steps=steps)
        for r, pts in data:
            color = region_color(r)
            ax.plot([r] * len(pts), pts, ",", color=color, alpha=0.4, markersize=0.7)

        ax.axvspan(3.57, 3.62, alpha=0.18, color=PALETTE["borde"], zorder=0)
        ax.axvline(3.57, color=PALETTE["borde"], lw=1.0, ls="--", alpha=0.9,
                   label="r = 3.57  (inicio del caos)")
        ax.set_xlim(r1, r2)
        ax.set_ylim(0, 1)
        ax.set_title(title, pad=10)
        ax.set_xlabel("Parámetro r")
        ax.set_ylabel("Utilización $x_n$")
        ax.grid(True)
        ax.legend(fontsize=8)

    fig.suptitle("Estructura de bifurcación — Detalle del borde del caos", y=1.01)
    fig.tight_layout()
    fig.savefig("fig2_zoom_borde_caos.png", dpi=180, bbox_inches="tight")
    plt.close()
    print("✓  fig2_zoom_borde_caos.png")


# ══════════════════════════════════════════════
# FIGURA 3 – Series de tiempo por régimen
# ══════════════════════════════════════════════

def plot_time_series():
    configs = [
        (2.5,  PALETTE["estable"], "r = 2.5 — Estable\nCarga converge a un punto fijo"),
        (3.2,  PALETTE["periodo"], "r = 3.2 — Período 2\nCongestión oscila entre 2 estados"),
        (3.5,  PALETTE["periodo"], "r = 3.5 — Período 4\nCiclo TCP slow-start amplificado"),
        (3.57, PALETTE["borde"],   "r = 3.57 — Borde del caos\nMáxima complejidad / adaptabilidad"),
        (3.75, PALETTE["caos"],    "r = 3.75 — Caótico\nCascadas de congestión impredecibles"),
        (4.0,  PALETTE["caos"],    "r = 4.0 — Caos máximo\nColapso total de la predictibilidad"),
    ]

    fig, axes = plt.subplots(3, 2, figsize=(13, 9))
    fig.patch.set_facecolor(PALETTE["bg"])
    axes = axes.flatten()

    n = 80
    t = np.arange(n)

    for ax, (r, color, title) in zip(axes, configs):
        xs = time_series(r, x0=0.5, n=n)
        xs2 = time_series(r, x0=0.501, n=n) 

        ax.fill_between(t, xs, xs2, color=color, alpha=0.15, label="Diferencia")
        ax.plot(t, xs,  color=color, lw=1.3, label="$x_0 = 0.500$")
        ax.plot(t, xs2, color=color, lw=1.0, ls="--", alpha=0.7, label="$x_0 = 0.501$")
        ax.set_ylim(0, 1)
        ax.set_xlim(0, n - 1)
        ax.set_title(title, fontsize=9, pad=6)
        ax.set_xlabel("Tiempo (paquetes / RTT)", fontsize=8)
        ax.set_ylabel("Utilización $x_n$", fontsize=8)
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(True)

    fig.suptitle("Series de tiempo — Sensibilidad a condiciones iniciales por régimen\n"
                 "(línea continua vs punteada: diferencia de $x_0 = 0.001$)", y=1.01)
    fig.tight_layout()
    fig.savefig("fig3_series_tiempo.png", dpi=180, bbox_inches="tight")
    plt.close()
    print("✓  fig3_series_tiempo.png")


# ══════════════════════════════════════════════
# FIGURA 4 – Exponente de Lyapunov
# ══════════════════════════════════════════════

def plot_lyapunov():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True,
                                    gridspec_kw={"height_ratios": [1, 1.8]})
    fig.patch.set_facecolor(PALETTE["bg"])

    rs = np.linspace(R_MIN, R_MAX, 1500)
    le = lyapunov(rs, warmup=300, n=1000)

    # Panel superior: diagrama de bifurcación resumido
    data = bifurcation_data(R_MIN, R_MAX, steps=1000)
    for r, pts in data:
        ax1.plot([r] * len(pts), pts, ",", color=region_color(r), alpha=0.3, markersize=0.5)
    shade_regimes(ax1)
    ax1.set_ylim(0, 1)
    ax1.set_ylabel("Utilización $x_n$")
    ax1.set_title("Diagrama de bifurcación (referencia)")
    ax1.grid(True)

    # Panel inferior: exponente de Lyapunov
    pos_mask = le >= 0
    neg_mask = le < 0
    ax2.fill_between(rs, 0, le, where=pos_mask, color=PALETTE["caos"],
                     alpha=0.35, label="λ > 0  (caos)")
    ax2.fill_between(rs, 0, le, where=neg_mask, color=PALETTE["estable"],
                     alpha=0.35, label="λ < 0  (orden)")
    ax2.plot(rs, le, color=PALETTE["text"], lw=0.7, alpha=0.8)
    ax2.axhline(0, color=PALETTE["text"], lw=1.0, ls="-", alpha=0.5)
    ax2.axvline(3.57, color=PALETTE["borde"], lw=1.0, ls="--", alpha=0.9,
                label="r ≈ 3.57  (λ → 0)")
    shade_regimes(ax2, y_min=-2, y_max=1)

    ax2.set_ylim(-2, 0.8)
    ax2.set_xlim(R_MIN, R_MAX)
    ax2.set_xlabel("Parámetro r  (agresividad del tráfico)")
    ax2.set_ylabel("Exponente de Lyapunov  λ")
    ax2.set_title("Exponente de Lyapunov — Medida cuantitativa del caos")
    ax2.legend(fontsize=8)
    ax2.grid(True)

    # Anotaciones Lyapunov
    ax2.annotate("λ = 0\nborde del caos", xy=(3.57, 0.02), xytext=(3.4, 0.45),
                 arrowprops=dict(arrowstyle="->", color=PALETTE["borde"], lw=1),
                 fontsize=8, color=PALETTE["borde"])
    ax2.annotate("Ventana\nperiodo 3", xy=(3.83, -0.4), xytext=(3.88, -1.2),
                 arrowprops=dict(arrowstyle="->", color=PALETTE["periodo"], lw=1),
                 fontsize=8, color=PALETTE["periodo"])

    fig.suptitle("Exponente de Lyapunov — Cuantificación del caos en Internet", y=1.01)
    fig.tight_layout()
    fig.savefig("fig4_lyapunov.png", dpi=180, bbox_inches="tight")
    plt.close()
    print("✓  fig4_lyapunov.png")


# ══════════════════════════════════════════════
# FIGURA 5 – Mapa de retorno (cobweb) por régimen
# ══════════════════════════════════════════════

def plot_cobweb():
    configs = [
        (2.8,  PALETTE["estable"], "r = 2.8 — Estable"),
        (3.2,  PALETTE["periodo"], "r = 3.2 — Periodo 2"),
        (3.5,  PALETTE["periodo"], "r = 3.5 — Periodo 4"),
        (3.57, PALETTE["borde"],   "r = 3.57 — Borde del caos"),
        (3.75, PALETTE["caos"],    "r = 3.75 — Caótico"),
        (3.83, PALETTE["borde"],   "r = 3.83 — Ventana periodo 3"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(13, 8))
    fig.patch.set_facecolor(PALETTE["bg"])
    axes = axes.flatten()

    x_line = np.linspace(0, 1, 300)

    for ax, (r, color, title) in zip(axes, configs):
        # Curva logística y diagonal
        y_logistic = r * x_line * (1 - x_line)
        ax.plot(x_line, y_logistic, color=color, lw=1.5, label=f"$f(x) = {r}x(1-x)$")
        ax.plot(x_line, x_line, color=PALETTE["gray"], lw=0.8, ls="--", alpha=0.7,
                label="$y = x$")

        # Diagrama de telaraña (cobweb)
        x = 0.2
        xs_cob = [x]
        ys_cob = [0]
        n_steps = 60
        for _ in range(n_steps):
            y = logistic(r, x)
            xs_cob += [x, y]
            ys_cob += [y, y]
            x = y
            xs_cob.append(x)
            ys_cob.append(x)

        ax.plot(xs_cob, ys_cob, color=color, lw=0.7, alpha=0.6)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(title, fontsize=9, pad=6)
        ax.set_xlabel("$x_n$  (utilización actual)", fontsize=8)
        ax.set_ylabel("$x_{n+1}$ (siguiente paso)", fontsize=8)
        ax.grid(True)

    fig.suptitle("Diagramas de telaraña (cobweb) — Convergencia de la dinámica por régimen", y=1.01)
    fig.tight_layout()
    fig.savefig("fig5_cobweb.png", dpi=180, bbox_inches="tight")
    plt.close()
    print("✓  fig5_cobweb.png")


# ══════════════════════════════════════════════
# FIGURA 6 – Panel resumen (poster)
# ══════════════════════════════════════════════

def plot_summary_panel():
    fig = plt.figure(figsize=(14, 10))
    fig.patch.set_facecolor(PALETTE["bg"])
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.32)

    # — Panel A: bifurcación completa
    ax_a = fig.add_subplot(gs[0, :])
    data = bifurcation_data(R_MIN, R_MAX, steps=2000)
    for r, pts in data:
        ax_a.plot([r] * len(pts), pts, ",", color=region_color(r), alpha=0.35, markersize=0.5)
    shade_regimes(ax_a)
    ax_a.set_xlim(R_MIN, R_MAX)
    ax_a.set_ylim(0, 1)
    ax_a.set_xlabel("Parámetro r  (agresividad del tráfico)")
    ax_a.set_ylabel("Utilización $x_n$")
    ax_a.set_title("A — Diagrama de bifurcación del mapeo logístico / Internet")
    ax_a.grid(True)
    legend_patches = [
        mpatches.Patch(color=PALETTE["estable"], label="Estable"),
        mpatches.Patch(color=PALETTE["periodo"], label="Periódico"),
        mpatches.Patch(color=PALETTE["borde"],   label="Borde del caos"),
        mpatches.Patch(color=PALETTE["caos"],    label="Caótico"),
    ]
    ax_a.legend(handles=legend_patches, loc="lower left", fontsize=8, framealpha=0.9)

    # — Panel B: Lyapunov
    ax_b = fig.add_subplot(gs[1, 0])
    rs = np.linspace(R_MIN, R_MAX, 1200)
    le = lyapunov(rs, warmup=200, n=600)
    pos_mask = le >= 0
    neg_mask = le < 0
    ax_b.fill_between(rs, 0, le, where=pos_mask, color=PALETTE["caos"], alpha=0.4, label="λ > 0 caos")
    ax_b.fill_between(rs, 0, le, where=neg_mask, color=PALETTE["estable"], alpha=0.4, label="λ < 0 orden")
    ax_b.plot(rs, le, color=PALETTE["text"], lw=0.6, alpha=0.8)
    ax_b.axhline(0, color=PALETTE["text"], lw=1.0, alpha=0.5)
    ax_b.axvline(3.57, color=PALETTE["borde"], lw=0.9, ls="--", alpha=0.9)
    ax_b.set_xlim(R_MIN, R_MAX); ax_b.set_ylim(-2, 0.8)
    ax_b.set_xlabel("Parámetro r"); ax_b.set_ylabel("Exponente de Lyapunov λ")
    ax_b.set_title("B — Exponente de Lyapunov"); ax_b.grid(True)
    ax_b.legend(fontsize=8)

    # — Panel C: series de tiempo comparadas
    ax_c = fig.add_subplot(gs[1, 1])
    n = 60
    t = np.arange(n)
    for r, color, label in [
        (2.8,  PALETTE["estable"], "r=2.8 estable"),
        (3.2,  PALETTE["periodo"], "r=3.2 periodo 2"),
        (3.57, PALETTE["borde"],   "r=3.57 borde"),
        (3.8,  PALETTE["caos"],    "r=3.8 caótico"),
    ]:
        xs = time_series(r, x0=0.5, n=n)
        ax_c.plot(t, xs, color=color, lw=1.1, label=label, alpha=0.85)
    ax_c.set_xlim(0, n - 1); ax_c.set_ylim(0, 1)
    ax_c.set_xlabel("Tiempo (RTT / paso)"); ax_c.set_ylabel("Utilización $x_n$")
    ax_c.set_title("C — Series de tiempo por régimen"); ax_c.grid(True)
    ax_c.legend(fontsize=7.5)

    fig.suptitle("Internet como sistema dinámico no lineal — Modelo del mapeo logístico",
                 fontsize=13, y=1.01, fontweight="normal")

    fig.savefig("fig6_panel_resumen.png", dpi=180, bbox_inches="tight")
    plt.close()
    print("✓  fig6_panel_resumen.png")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("Generando gráficas...\n")
    plot_bifurcation_full()   # Figura 1
    plot_bifurcation_zoom()   # Figura 2
    plot_time_series()        # Figura 3
    plot_lyapunov()           # Figura 4
    plot_cobweb()             # Figura 5
    plot_summary_panel()      # Figura 6
    print("\nTodas las figuras guardadas en el directorio actual.")