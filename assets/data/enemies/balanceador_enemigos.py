
import json
from pathlib import Path


def get_value(data, *keys, default=None):
    """Obtiene un valor anidado sin provocar errores."""
    current = data

    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)

        if current is None:
            return default

    return current


def format_value(value):
    if value is None:
        return "No definido"
    return str(value)


def analyze_enemy(data, filename):
    weapon = data.get("weapon") or {}
    movement = data.get("movement") or {}
    visual = data.get("visual") or {}
    dimensions = visual.get("dimensions") or {}

    damage = weapon.get("damage", 0)
    cannons = weapon.get("cannonCount", 1)
    burst = weapon.get("burstCount", 1)
    interval = weapon.get("fireInterval", 0)

    # Estimación teórica, suponiendo que todos los cañones
    # disparan en cada ráfaga y que los proyectiles impactan.
    if interval and interval > 0:
        theoretical_dps = damage * cannons * burst / interval
    else:
        theoretical_dps = 0

    abilities = data.get("abilities") or []

    if abilities:
        ability_names = []

        for ability in abilities:
            if isinstance(ability, dict):
                ability_names.append(
                    str(ability.get("name", ability.get("id", ability)))
                )
            else:
                ability_names.append(str(ability))

        abilities_text = ", ".join(ability_names)
    else:
        abilities_text = "Ninguna"

    lines = [
        "=" * 65,
        f"ENEMIGO: {data.get('name', 'Sin nombre')}",
        f"Archivo: {filename}",
        f"ID: {data.get('id', 'No definido')}",
        "-" * 65,

        "[ESTADISTICAS]",
        f"Vida: {format_value(data.get('health'))}",
        f"Velocidad: {format_value(data.get('speed'))}",
        f"Daño por contacto: {format_value(data.get('contactDamage'))}",
        f"Puntuacion: {format_value(data.get('score'))}",
        f"Monedas recompensa: {format_value(data.get('rewardCoins'))}",

        "",
        "[MOVIMIENTO]",
        f"Comportamiento: {format_value(movement.get('behavior'))}",
        f"Patron: {format_value(movement.get('pattern'))}",
        f"Posicion objetivo Y: {format_value(movement.get('targetY'))}",
        f"Amplitud: {format_value(movement.get('amplitude'))}",
        f"Frecuencia: {format_value(movement.get('frequency'))}",
        f"Velocidad patrulla: {format_value(movement.get('patrolSpeed'))}",

        "",
        "[ARMAMENTO]",
        f"Tipo de arma: {format_value(weapon.get('type'))}",
        f"Danio por proyectil: {format_value(damage)}",
        f"Velocidad proyectil: {format_value(weapon.get('projectileSpeed'))}",
        f"Intervalo disparo: {format_value(interval)} segundos",
        f"Numero de canones: {format_value(cannons)}",
        f"Proyectiles por rafaga: {format_value(burst)}",
        f"DPS teorico maximo: {theoretical_dps:.2f}",
        f"Posicion canon: {format_value(weapon.get('cannonPosition'))}",
        f"Separacion canones: {format_value(weapon.get('cannonSeparation'))}",

        "",
        "[ASPECTO Y TAMANO]",
        f"Forma: {format_value(visual.get('shape'))}",
        f"Ancho: {format_value(dimensions.get('width'))}",
        f"Alto: {format_value(dimensions.get('height'))}",

        "",
        "[HABILIDADES]",
        abilities_text,
        "",
    ]

    return "\n".join(lines), {
        "name": data.get("name", "Sin nombre"),
        "id": data.get("id", "No definido"),
        "health": data.get("health", 0),
        "speed": data.get("speed", 0),
        "contactDamage": data.get("contactDamage", 0),
        "score": data.get("score", 0),
        "dps": theoretical_dps,
    }


def main():
    print("======================================")
    print(" ANALIZADOR DE ENEMIGOS - ASTRO ARCADE")
    print("======================================")

    folder_input = input("\nRuta de la carpeta de enemigos: ").strip()
    folder_input = folder_input.strip('"')

    folder = Path(folder_input)

    if not folder.exists() or not folder.is_dir():
        print("\nERROR: La carpeta no existe.")
        input("Pulsa ENTER para salir...")
        return

    json_files = sorted(folder.rglob("*.json"))

    if not json_files:
        print("\nNo se han encontrado archivos JSON.")
        input("Pulsa ENTER para salir...")
        return

    reports = []
    summaries = []
    errors = []

    for file in json_files:
        try:
            with file.open("r", encoding="utf-8-sig") as f:
                data = json.load(f)

            # Admite tanto un enemigo por archivo como
            # varios enemigos dentro de un array JSON.
            enemies = data if isinstance(data, list) else [data]

            for enemy in enemies:
                if not isinstance(enemy, dict):
                    continue

                report, summary = analyze_enemy(
                    enemy,
                    file.name
                )

                reports.append(report)
                summaries.append(summary)

        except Exception as error:
            errors.append(f"{file.name}: {error}")

    # Ordenar por puntuacion, de menor a mayor.
    summaries.sort(key=lambda x: x["score"])

    output = []

    output.append("ASTRO ARCADE - INFORME DE ENEMIGOS")
    output.append(f"Archivos JSON encontrados: {len(json_files)}")
    output.append(f"Enemigos analizados: {len(summaries)}")
    output.append("")

    output.append("RESUMEN COMPARATIVO")
    output.append("-" * 90)
    output.append(
        f"{'NOMBRE':25} {'VIDA':>6} {'VEL.':>7} "
        f"{'CONTACTO':>9} {'SCORE':>8} {'DPS':>8}"
    )
    output.append("-" * 90)

    for enemy in summaries:
        output.append(
            f"{enemy['name'][:25]:25} "
            f"{str(enemy['health']):>6} "
            f"{str(enemy['speed']):>7} "
            f"{str(enemy['contactDamage']):>9} "
            f"{str(enemy['score']):>8} "
            f"{enemy['dps']:>8.2f}"
        )

    output.append("")
    output.append("DETALLE INDIVIDUAL")
    output.append("")

    output.extend(reports)

    output.append("")
    output.append("NOTAS")
    output.append("-" * 65)
    output.append(
        "El DPS es una estimacion teorica: no contempla "
        "fallos, trayectoria, tiempo de rafaga ni impactos reales."
    )
    output.append(
        "La dificultad real tambien depende del movimiento, "
        "la formacion y la cantidad de enemigos simultaneos."
    )

    if errors:
        output.append("")
        output.append("ARCHIVOS CON ERRORES")
        for error in errors:
            output.append(error)

    report_path = folder / "resumen_enemigos.txt"

    report_path.write_text(
        "\n".join(output),
        encoding="utf-8"
    )

    print("\nAnalisis terminado.")
    print(f"Enemigos analizados: {len(summaries)}")
    print(f"Errores: {len(errors)}")
    print(f"\nInforme generado en:\n{report_path}")

    input("\nPulsa ENTER para salir...")


if __name__ == "__main__":
    main()
