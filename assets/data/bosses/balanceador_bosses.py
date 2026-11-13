
import json
from pathlib import Path


def fmt(value):
    return "No definido" if value is None else str(value)


def analyze_boss(data, filename):
    phases = data.get("phases") or []

    lines = [
        "=" * 70,
        f"JEFE: {data.get('name', 'Sin nombre')}",
        f"Archivo: {filename}",
        f"ID: {data.get('id', 'No definido')}",
        "-" * 70,

        "[ESTADISTICAS PRINCIPALES]",
        f"Tipo de criatura: {fmt(data.get('creatureType'))}",
        f"Vida: {fmt(data.get('health'))}",
        f"Velocidad: {fmt(data.get('speed'))}",
        f"Daño por contacto: {fmt(data.get('contactDamage'))}",
        f"Puntuacion: {fmt(data.get('score'))}",

        "",
        "[MOVIMIENTO]",
        f"Patron: {fmt(data.get('movementPattern'))}",
        f"Amplitud: {fmt(data.get('movementAmplitude'))}",

        "",
        "[ARMAMENTO]",
        f"Daño por proyectil: {fmt(data.get('projectileDamage'))}",
        f"Velocidad proyectil: {fmt(data.get('projectileSpeed'))}",
        f"Intervalo de ataque: {fmt(data.get('attackInterval'))} segundos",
        f"Proyectiles por ataque: {fmt(data.get('projectileCount'))}",
        f"Angulo de dispersion: {fmt(data.get('spreadAngle'))} grados",
    ]

    # DPS teórico de los ataques base.
    damage = data.get("projectileDamage", 0)
    count = data.get("projectileCount", 0)
    interval = data.get("attackInterval", 0)

    if isinstance(damage, (int, float)) and isinstance(count, (int, float)):
        if isinstance(interval, (int, float)) and interval > 0:
            dps = damage * count / interval
        else:
            dps = 0
    else:
        dps = 0

    lines.append(f"DPS teorico base (todos impactan): {dps:.2f}")

    lines.extend([
        "",
        "[FASES]",
        f"Numero de fases adicionales: {len(phases)}",
    ])

    phase_summaries = []

    for index, phase in enumerate(phases, start=1):
        threshold = phase.get("healthThreshold")
        phase_speed = phase.get("speedMultiplier", 1)
        phase_interval = phase.get("attackInterval", interval)
        phase_count = phase.get("projectileCount", count)
        phase_damage = phase.get("projectileDamage", damage)
        phase_spread = phase.get("spreadAngle", data.get("spreadAngle"))
        phase_movement = phase.get(
            "movementPattern",
            data.get("movementPattern")
        )

        # Las propiedades no especificadas heredan las del jefe.
        phase_dps = 0
        if (
            isinstance(phase_damage, (int, float))
            and isinstance(phase_count, (int, float))
            and isinstance(phase_interval, (int, float))
            and phase_interval > 0
        ):
            phase_dps = phase_damage * phase_count / phase_interval

        lines.extend([
            "",
            f"FASE {index}",
            "-" * 40,
            f"Umbral de vida: {fmt(threshold)}",
            f"Patron de movimiento: {fmt(phase_movement)}",
            f"Multiplicador velocidad: {fmt(phase_speed)}",
            f"Velocidad resultante: {fmt(data.get('speed', 0) * phase_speed)}",
            f"Intervalo ataque: {fmt(phase_interval)} segundos",
            f"Proyectiles por ataque: {fmt(phase_count)}",
            f"Daño por proyectil: {fmt(phase_damage)}",
            f"Dispersion: {fmt(phase_spread)} grados",
            f"DPS teorico fase (todos impactan): {phase_dps:.2f}",
        ])

        phase_summaries.append({
            "threshold": threshold,
            "speed_multiplier": phase_speed,
            "dps": phase_dps,
            "attack_interval": phase_interval,
            "projectile_count": phase_count,
        })

    visual = data.get("visual") or {}

    lines.extend([
        "",
        "[DIMENSIONES VISUALES]",
        f"Ancho: {fmt(visual.get('width'))}",
        f"Alto: {fmt(visual.get('height'))}",
        f"Envergadura alas: {fmt(visual.get('wingSpan'))}",
        f"Numero de motores: {fmt(visual.get('engineCount'))}",
        "",
    ])

    return "\n".join(lines), {
        "name": data.get("name", "Sin nombre"),
        "id": data.get("id", "No definido"),
        "health": data.get("health", 0),
        "speed": data.get("speed", 0),
        "contactDamage": data.get("contactDamage", 0),
        "projectileDamage": damage,
        "projectileCount": count,
        "attackInterval": interval,
        "dps": dps,
        "phases": len(phases),
        "phase_summaries": phase_summaries,
    }


def main():
    print("======================================")
    print(" ANALIZADOR DE JEFES - ASTRO ARCADE")
    print("======================================")

    folder_input = input("\nRuta de la carpeta de jefes: ").strip()
    folder = Path(folder_input.strip('"'))

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

            bosses = data if isinstance(data, list) else [data]

            for boss in bosses:
                if not isinstance(boss, dict):
                    continue

                if "health" not in boss or "projectileDamage" not in boss:
                    continue

                report, summary = analyze_boss(boss, file.name)
                reports.append(report)
                summaries.append(summary)

        except Exception as error:
            errors.append(f"{file}: {error}")

    summaries.sort(key=lambda x: x["name"].lower())

    output = [
        "ASTRO ARCADE - INFORME DE JEFES",
        f"Archivos JSON encontrados: {len(json_files)}",
        f"Jefes analizados: {len(summaries)}",
        "",
        "RESUMEN COMPARATIVO",
        "-" * 105,
        f"{'JEFE':25} {'VIDA':>7} {'VEL.':>7} "
        f"{'CONTACTO':>9} {'PROYECT.':>9} "
        f"{'INTERVALO':>10} {'DPS':>8} {'FASES':>7}",
        "-" * 105,
    ]

    for boss in summaries:
        output.append(
            f"{boss['name'][:25]:25} "
            f"{str(boss['health']):>7} "
            f"{str(boss['speed']):>7} "
            f"{str(boss['contactDamage']):>9} "
            f"{str(boss['projectileCount']):>9} "
            f"{str(boss['attackInterval']):>10} "
            f"{boss['dps']:>8.2f} "
            f"{str(boss['phases']):>7}"
        )

    output.extend([
        "",
        "DETALLE INDIVIDUAL",
        "",
    ])

    output.extend(reports)

    output.extend([
        "",
        "NOTAS DE BALANCE",
        "-" * 70,
        "El DPS supone que todos los proyectiles impactan.",
        "No contempla la trayectoria, la dispersion ni la duracion real del ataque.",
        "Las fases heredan las estadisticas base que no sobrescriben.",
        "La dificultad real depende tambien del movimiento y las colisiones.",
    ])

    if errors:
        output.extend(["", "ERRORES DE LECTURA"])
        output.extend(errors)

    report_path = folder / "resumen_bosses.txt"
    report_path.write_text("\n".join(output), encoding="utf-8")

    print("\nAnalisis terminado.")
    print(f"Jefes analizados: {len(summaries)}")
    print(f"Errores: {len(errors)}")
    print(f"\nInforme generado en:\n{report_path}")

    input("\nPulsa ENTER para salir...")


if __name__ == "__main__":
    main()
