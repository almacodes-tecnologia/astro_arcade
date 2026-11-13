
import json
from pathlib import Path


def value(data, *keys, default="No definido"):
    current = data

    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)

        if current is None:
            return default

    return current


def analyze_ship(data, filename):
    stats = data.get("stats") or {}
    weapon = data.get("weapon") or {}
    unlock = data.get("unlock") or {}
    visual = data.get("visual") or {}
    dimensions = visual.get("dimensions") or {}

    speed = stats.get("speed", 0)
    health = stats.get("health", 0)
    fire_rate = stats.get("fireRate", 0)
    damage = stats.get("damage", 0)

    # FireRate representa el tiempo entre disparos.
    # DPS teórico sin tener en cuenta impactos fallidos.
    dps = damage / fire_rate if fire_rate and fire_rate > 0 else 0

    # Resistencia básica: vida de la nave.
    # No contempla habilidades defensivas ni invulnerabilidad.
    durability = health

    # Potencia de fuego teórica durante 10 segundos.
    damage_10s = dps * 10

    lines = [
        "=" * 65,
        f"NAVE: {data.get('name', 'Sin nombre')}",
        f"Archivo: {filename}",
        f"ID: {data.get('id', 'No definido')}",
        "-" * 65,

        "[ESTADISTICAS PRINCIPALES]",
        f"Velocidad: {speed}",
        f"Vida: {health}",
        f"Intervalo de disparo: {fire_rate} segundos",
        f"Daño por impacto: {damage}",
        f"DPS teorico: {dps:.2f}",
        f"Daño teorico en 10 segundos: {damage_10s:.2f}",
        f"Resistencia base (vida): {durability}",

        "",
        "[ARMAMENTO]",
        f"Tipo: {value(weapon, 'type')}",
        f"Velocidad proyectil: {value(weapon, 'projectileSpeed')}",
        f"Ancho proyectil: {value(weapon, 'projectileWidth')}",
        f"Alto proyectil: {value(weapon, 'projectileHeight')}",

        "",
        "[DESBLOQUEO]",
        f"Coste monedas: {value(unlock, 'coins')}",
        f"Licencia: {value(unlock, 'license')}",

        "",
        "[DIMENSIONES VISUALES]",
        f"Tipo: {value(visual, 'type')}",
        f"Forma: {value(visual, 'shape')}",
        f"Escala: {value(visual, 'scale')}",
        f"Ancho: {value(dimensions, 'width')}",
        f"Alto: {value(dimensions, 'height')}",

        "",
        "[DESCRIPCION]",
        data.get("description", "Sin descripción"),
        "",
    ]

    return "\n".join(lines), {
        "name": data.get("name", "Sin nombre"),
        "id": data.get("id", "No definido"),
        "speed": speed,
        "health": health,
        "fireRate": fire_rate,
        "damage": damage,
        "dps": dps,
        "unlockCoins": unlock.get("coins", "No definido"),
        "license": unlock.get("license", "No definido"),
    }


def main():
    print("======================================")
    print(" ANALIZADOR DE NAVES - ASTRO ARCADE")
    print("======================================")

    folder_input = input("\nRuta de la carpeta de naves: ").strip()
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

            ships = data if isinstance(data, list) else [data]

            for ship in ships:
                if not isinstance(ship, dict):
                    continue

                # Ignorar JSON que no sean configuraciones de naves.
                if "stats" not in ship or "weapon" not in ship:
                    continue

                report, summary = analyze_ship(ship, file.name)
                reports.append(report)
                summaries.append(summary)

        except Exception as error:
            errors.append(f"{file}: {error}")

    # Orden alfabético para facilitar la comparación.
    summaries.sort(key=lambda x: x["name"].lower())

    output = [
        "ASTRO ARCADE - INFORME DE NAVES",
        f"Archivos JSON encontrados: {len(json_files)}",
        f"Naves analizadas: {len(summaries)}",
        "",
        "RESUMEN COMPARATIVO",
        "-" * 100,
        f"{'NAVE':22} {'VELOCIDAD':>10} {'VIDA':>7} "
        f"{'INTERVALO':>11} {'DANO':>7} {'DPS':>8} "
        f"{'MONEDAS':>9} {'LICENCIA':>10}",
        "-" * 100,
    ]

    for ship in summaries:
        output.append(
            f"{ship['name'][:22]:22} "
            f"{str(ship['speed']):>10} "
            f"{str(ship['health']):>7} "
            f"{str(ship['fireRate']):>11} "
            f"{str(ship['damage']):>7} "
            f"{ship['dps']:>8.2f} "
            f"{str(ship['unlockCoins']):>9} "
            f"{str(ship['license']):>10}"
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
        "-" * 65,
        "El DPS se calcula como daño / intervalo de disparo.",
        "No contempla proyectiles fallidos, alcance ni patrones.",
        "La velocidad y vida se muestran como valores configurados.",
        "El tamaño visual no equivale necesariamente al area real de colision.",
        "El equilibrio final depende tambien de los proyectiles y enemigos.",
    ])

    if errors:
        output.extend(["", "ERRORES DE LECTURA"])
        output.extend(errors)

    report_path = folder / "resumen_naves.txt"
    report_path.write_text("\n".join(output), encoding="utf-8")

    print("\nAnalisis terminado.")
    print(f"Naves analizadas: {len(summaries)}")
    print(f"Errores: {len(errors)}")
    print(f"\nInforme generado en:\n{report_path}")

    input("\nPulsa ENTER para salir...")


if __name__ == "__main__":
    main()
