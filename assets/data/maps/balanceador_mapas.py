
import json
from pathlib import Path
from collections import Counter


def fmt(value):
    return "No definido" if value is None else str(value)


def analyze_map(data, filename):
    waves = data.get("waves") or []
    visual = data.get("visual") or {}
    reward = data.get("reward") or {}
    unlock = data.get("unlock") or {}

    total_enemies = 0
    all_types = Counter()
    wave_reports = []
    wave_summaries = []

    for index, wave in enumerate(waves, start=1):
        enemies = wave.get("enemies") or []

        wave_total = 0
        types = []
        intervals = []
        formations = Counter()
        wave_types = Counter()

        for enemy in enemies:
            enemy_type = enemy.get("type", "Desconocido")
            count = enemy.get("count", 0)
            interval = enemy.get("interval")
            formation = enemy.get("formation", "No definida")

            if not isinstance(count, (int, float)):
                count = 0

            wave_total += count
            wave_types[enemy_type] += count
            all_types[enemy_type] += count
            formations[formation] += 1

            if isinstance(interval, (int, float)):
                intervals.append(interval)

        total_enemies += wave_total

        average_interval = (
            sum(intervals) / len(intervals)
            if intervals else 0
        )

        fastest_interval = min(intervals) if intervals else 0

        for enemy_type, count in wave_types.items():
            types.append(f"{enemy_type} x{count}")

        formations_text = ", ".join(
            f"{name} ({count})"
            for name, count in formations.items()
        )

        report = [
            "",
            f"OLEADA {index}: {wave.get('id', 'Sin ID')}",
            "-" * 55,
            f"Total enemigos: {wave_total}",
            f"Tipos: {', '.join(types) if types else 'Ninguno'}",
            f"Formaciones: {formations_text or 'No definidas'}",
            f"Intervalo medio: {average_interval:.2f} segundos",
            f"Intervalo mas rapido: {fastest_interval:.2f} segundos",
        ]

        wave_reports.extend(report)

        wave_summaries.append({
            "id": wave.get("id", f"wave_{index}"),
            "total": wave_total,
            "types": wave_types,
            "average_interval": average_interval,
            "fastest_interval": fastest_interval,
            "formations": formations,
        })

    # Comparativa de oleadas.
    counts = [wave["total"] for wave in wave_summaries]

    average_enemies = (
        sum(counts) / len(counts)
        if counts else 0
    )

    max_enemies = max(counts) if counts else 0
    min_enemies = min(counts) if counts else 0

    # Variación de enemigos entre oleadas consecutivas.
    progression = []

    for i in range(1, len(wave_summaries)):
        previous = wave_summaries[i - 1]["total"]
        current = wave_summaries[i]["total"]
        difference = current - previous

        progression.append(
            f"{wave_summaries[i - 1]['id']} -> "
            f"{wave_summaries[i]['id']}: "
            f"{difference:+}"
        )

    # Composición global.
    type_lines = [
        f"{enemy_type}: {count} apariciones previstas"
        for enemy_type, count in all_types.most_common()
    ]

    lines = [
        "=" * 70,
        f"MAPA: {data.get('name', 'Sin nombre')}",
        f"Archivo: {filename}",
        f"ID: {data.get('id', 'No definido')}",
        "-" * 70,

        "[INFORMACION GENERAL]",
        f"Descripcion: {fmt(data.get('description'))}",
        f"Dificultad configurada: {fmt(data.get('difficulty'))}",
        f"Numero de oleadas: {len(waves)}",
        f"Jefe final: {fmt(data.get('bossId'))}",

        "",
        "[RESUMEN DE ENEMIGOS]",
        f"Total de enemigos previstos: {total_enemies}",
        f"Media por oleada: {average_enemies:.2f}",
        f"Oleada con mas enemigos: {max_enemies}",
        f"Oleada con menos enemigos: {min_enemies}",

        "",
        "[COMPOSICION GLOBAL]",
        *type_lines,

        "",
        "[PROGRESION DE CANTIDAD]",
        *(progression or ["No hay suficientes oleadas para comparar"]),

        "",
        "[RECOMPENSAS Y DESBLOQUEO]",
        f"Monedas recompensa: {fmt(reward.get('coins'))}",
        f"Coste desbloqueo: {fmt(unlock.get('coins'))}",
        f"Licencia necesaria: {fmt(unlock.get('license'))}",

        "",
        "[ASPECTO Y ESCENARIO]",
        f"Fondo: {fmt(visual.get('background'))}",
        f"Musica: {fmt(visual.get('music'))}",
        f"Velocidad scroll: {fmt(visual.get('scrollSpeed'))}",

        "",
        "[DETALLE DE OLEADAS]",
        *wave_reports,
        "",
    ]

    return "\n".join(lines), {
        "name": data.get("name", "Sin nombre"),
        "id": data.get("id", "No definido"),
        "difficulty": data.get("difficulty", 0),
        "waves": len(waves),
        "total_enemies": total_enemies,
        "average_enemies": average_enemies,
        "max_enemies": max_enemies,
        "min_enemies": min_enemies,
        "boss": data.get("bossId", "No definido"),
        "types": all_types,
    }


def main():
    print("======================================")
    print(" ANALIZADOR DE MAPAS - ASTRO ARCADE")
    print("======================================")

    folder_input = input("\nRuta de la carpeta de mapas: ").strip()
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

            maps = data if isinstance(data, list) else [data]

            for map_data in maps:
                if not isinstance(map_data, dict):
                    continue

                if "waves" not in map_data or "difficulty" not in map_data:
                    continue

                report, summary = analyze_map(map_data, file.name)
                reports.append(report)
                summaries.append(summary)

        except Exception as error:
            errors.append(f"{file}: {error}")

    summaries.sort(key=lambda x: x["difficulty"])

    output = [
        "ASTRO ARCADE - INFORME DE MAPAS",
        f"Archivos JSON encontrados: {len(json_files)}",
        f"Mapas analizados: {len(summaries)}",
        "",
        "RESUMEN COMPARATIVO",
        "-" * 100,
        f"{'MAPA':25} {'DIFICULTAD':>11} {'OLEADAS':>9} "
        f"{'ENEMIGOS':>10} {'MEDIA':>8} {'MAXIMO':>8} {'JEFE':>15}",
        "-" * 100,
    ]

    for map_data in summaries:
        output.append(
            f"{map_data['name'][:25]:25} "
            f"{str(map_data['difficulty']):>11} "
            f"{map_data['waves']:>9} "
            f"{map_data['total_enemies']:>10} "
            f"{map_data['average_enemies']:>8.2f} "
            f"{map_data['max_enemies']:>8} "
            f"{str(map_data['boss'])[:15]:>15}"
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
        "La cantidad de enemigos es la suma de los count de cada oleada.",
        "El intervalo medio es una media de los intervalos configurados.",
        "No representa necesariamente el tiempo real entre todos los enemigos.",
        "No se calcula la vida o el daño total sin consultar los JSON de enemigos.",
        "La dificultad real depende tambien de armas, movimiento y jefe final.",
    ])

    if errors:
        output.extend(["", "ERRORES DE LECTURA"])
        output.extend(errors)

    report_path = folder / "resumen_mapas.txt"
    report_path.write_text("\n".join(output), encoding="utf-8")

    print("\nAnalisis terminado.")
    print(f"Mapas analizados: {len(summaries)}")
    print(f"Errores: {len(errors)}")
    print(f"\nInforme generado en:\n{report_path}")

    input("\nPulsa ENTER para salir...")


if __name__ == "__main__":
    main()
