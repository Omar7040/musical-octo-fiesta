"""VIN Scanner module for Toyota Car Service Application.

Módulo de escaneo de VIN para la aplicación de servicio de autos Toyota.
Este módulo permite decodificar el número de identificación vehicular (VIN)
y obtener información del vehículo.
"""

from dataclasses import dataclass
from typing import Optional, Dict


# Toyota World Manufacturer Identifier (WMI) codes
TOYOTA_WMI_CODES = {
    "JTD": "Toyota (Japan)",
    "JTE": "Toyota (Japan)",
    "JTK": "Toyota (Japan)",
    "JTL": "Toyota (Japan)",
    "JTM": "Toyota (Japan)",
    "JTN": "Toyota (Japan)",
    "JT1": "Toyota (Japan)",
    "JT2": "Toyota (Japan)",
    "JT3": "Toyota (Japan)",
    "JT4": "Toyota (Japan)",
    "JT5": "Toyota (Japan)",
    "JT6": "Toyota (Japan)",
    "JT7": "Toyota (Japan)",
    "JT8": "Toyota (Japan)",
    "1NX": "Toyota (USA - NUMMI)",
    "2T1": "Toyota (Canada)",
    "2T2": "Toyota (Canada)",
    "2T3": "Toyota (Canada)",
    "4T1": "Toyota (USA)",
    "4T3": "Toyota (USA)",
    "4T4": "Toyota (USA)",
    "5TD": "Toyota (USA)",
    "5TF": "Toyota (USA)",
    "5YF": "Toyota (USA)",
    "MR0": "Toyota (Thailand)",
    "MR1": "Toyota (Thailand)",
}

# Toyota model codes (position 4-8 in VIN)
TOYOTA_MODEL_CODES = {
    "A": "Supra",
    "B": "Corolla",
    "C": "Camry",
    "D": "Avalon",
    "E": "Celica",
    "F": "FJ Cruiser",
    "G": "Highlander",
    "H": "4Runner",
    "J": "Land Cruiser",
    "K": "Tacoma",
    "L": "Prius",
    "M": "MR2",
    "N": "Sequoia",
    "P": "Sienna",
    "R": "RAV4",
    "S": "Solara",
    "T": "Tundra",
    "U": "Matrix",
    "V": "Venza",
    "W": "Yaris",
    "X": "C-HR",
    "Y": "Yaris Cross",
    "Z": "bZ4X",
}

# Engine type codes
ENGINE_CODES = {
    "A": "1.5L 4-Cylinder",
    "B": "1.8L 4-Cylinder",
    "C": "2.0L 4-Cylinder",
    "D": "2.4L 4-Cylinder",
    "E": "2.5L 4-Cylinder",
    "F": "2.7L 4-Cylinder",
    "G": "3.0L V6",
    "H": "3.5L V6",
    "J": "4.0L V6",
    "K": "4.6L V8",
    "L": "4.7L V8",
    "M": "5.7L V8",
    "N": "Hybrid",
    "P": "Electric",
    "R": "1.6L Turbo",
    "S": "2.0L Turbo",
    "T": "3.0L Turbo",
}

# Body style codes
BODY_STYLE_CODES = {
    "1": "Sedán 2 puertas",
    "2": "Sedán 4 puertas",
    "3": "Hatchback 3 puertas",
    "4": "Hatchback 5 puertas",
    "5": "Station Wagon",
    "6": "SUV",
    "7": "Pickup",
    "8": "Van/Minivan",
    "9": "Convertible",
    "0": "Coupe",
}

# Year codes (position 10 in VIN)
YEAR_CODES = {
    "A": 2010, "B": 2011, "C": 2012, "D": 2013, "E": 2014,
    "F": 2015, "G": 2016, "H": 2017, "J": 2018, "K": 2019,
    "L": 2020, "M": 2021, "N": 2022, "P": 2023, "R": 2024,
    "S": 2025, "T": 2026, "V": 2027, "W": 2028, "X": 2029,
    "Y": 2030,
    "1": 2001, "2": 2002, "3": 2003, "4": 2004, "5": 2005,
    "6": 2006, "7": 2007, "8": 2008, "9": 2009,
}

# Plant codes (position 11 in VIN)
PLANT_CODES = {
    "0": "Japan - Tahara",
    "1": "Japan - Takaoka",
    "2": "Japan - Tsutsumi",
    "3": "Japan - Yoshiwara",
    "4": "Japan - Shimoyama",
    "5": "Japan - Miyata",
    "6": "USA - Kentucky",
    "7": "USA - Indiana",
    "8": "USA - Texas",
    "9": "Canada - Cambridge",
    "A": "Thailand",
    "B": "Mexico",
    "C": "China",
    "D": "Indonesia",
    "E": "UK",
}


@dataclass
class VINInfo:
    """Information decoded from a VIN number."""
    vin: str
    is_valid: bool
    manufacturer: str
    country: str
    model: str
    year: int
    engine: str
    body_style: str
    plant: str
    serial_number: str
    error_message: str = ""
    
    def to_dict(self) -> dict:
        """Convert VIN info to dictionary."""
        return {
            "vin": self.vin,
            "is_valid": self.is_valid,
            "manufacturer": self.manufacturer,
            "country": self.country,
            "model": self.model,
            "year": self.year,
            "engine": self.engine,
            "body_style": self.body_style,
            "plant": self.plant,
            "serial_number": self.serial_number,
            "error_message": self.error_message
        }


def validate_vin(vin: str) -> tuple:
    """
    Validate a VIN number.
    
    Args:
        vin: The VIN to validate.
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not vin:
        return False, "El VIN no puede estar vacío"
    
    vin = vin.upper().strip()
    
    if len(vin) != 17:
        return False, f"El VIN debe tener 17 caracteres (tiene {len(vin)})"
    
    # VIN cannot contain I, O, or Q
    invalid_chars = set("IOQ")
    found_invalid = set(vin) & invalid_chars
    if found_invalid:
        return False, f"El VIN contiene caracteres inválidos: {', '.join(found_invalid)}"
    
    # Check if it's alphanumeric
    if not vin.isalnum():
        return False, "El VIN solo puede contener letras y números"
    
    # Check if it's a Toyota VIN
    wmi = vin[:3]
    if wmi not in TOYOTA_WMI_CODES:
        return False, f"El VIN no corresponde a un vehículo Toyota (WMI: {wmi})"
    
    return True, ""


def calculate_check_digit(vin: str) -> str:
    """
    Calculate the check digit for a VIN (position 9).
    
    Args:
        vin: The VIN to calculate check digit for.
        
    Returns:
        The calculated check digit.
    """
    transliteration = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9,
        'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9,
    }
    weights = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
    
    total = 0
    for i, char in enumerate(vin.upper()):
        if char.isdigit():
            value = int(char)
        else:
            value = transliteration.get(char, 0)
        total += value * weights[i]
    
    remainder = total % 11
    return 'X' if remainder == 10 else str(remainder)


def scan_vin(vin: str) -> VINInfo:
    """
    Scan and decode a VIN number to get vehicle information.
    
    Escanea y decodifica un número VIN para obtener información del vehículo.
    
    Args:
        vin: The 17-character VIN to scan.
        
    Returns:
        VINInfo object with decoded vehicle information.
    """
    vin = vin.upper().strip() if vin else ""
    
    # Validate VIN
    is_valid, error_message = validate_vin(vin)
    
    if not is_valid:
        return VINInfo(
            vin=vin,
            is_valid=False,
            manufacturer="",
            country="",
            model="",
            year=0,
            engine="",
            body_style="",
            plant="",
            serial_number="",
            error_message=error_message
        )
    
    # Decode WMI (World Manufacturer Identifier) - positions 1-3
    wmi = vin[:3]
    manufacturer_info = TOYOTA_WMI_CODES.get(wmi, "Toyota")
    
    # Extract country from manufacturer info
    if "Japan" in manufacturer_info:
        country = "Japón"
    elif "USA" in manufacturer_info:
        country = "Estados Unidos"
    elif "Canada" in manufacturer_info:
        country = "Canadá"
    elif "Thailand" in manufacturer_info:
        country = "Tailandia"
    else:
        country = "Desconocido"
    
    # Decode VDS (Vehicle Descriptor Section) - positions 4-9
    model_code = vin[3]
    model = TOYOTA_MODEL_CODES.get(model_code, f"Modelo código {model_code}")
    
    engine_code = vin[4]
    engine = ENGINE_CODES.get(engine_code, f"Motor código {engine_code}")
    
    body_code = vin[5]
    body_style = BODY_STYLE_CODES.get(body_code, f"Carrocería código {body_code}")
    
    # Decode VIS (Vehicle Identifier Section) - positions 10-17
    year_code = vin[9]
    year = YEAR_CODES.get(year_code, 2000)
    
    plant_code = vin[10]
    plant = PLANT_CODES.get(plant_code, f"Planta código {plant_code}")
    
    serial_number = vin[11:17]
    
    return VINInfo(
        vin=vin,
        is_valid=True,
        manufacturer="Toyota",
        country=country,
        model=model,
        year=year,
        engine=engine,
        body_style=body_style,
        plant=plant,
        serial_number=serial_number
    )


def print_vin_info(vin_info: VINInfo) -> None:
    """
    Print formatted VIN information.
    
    Imprime la información del VIN de forma formateada.
    
    Args:
        vin_info: The VINInfo object to print.
    """
    print("\n" + "=" * 60)
    print("          INFORMACIÓN DEL VIN ESCANEADO")
    print("=" * 60)
    
    if not vin_info.is_valid:
        print(f"\n  ❌ VIN INVÁLIDO: {vin_info.vin}")
        print(f"  Error: {vin_info.error_message}")
        print("=" * 60)
        return
    
    print(f"\n  VIN: {vin_info.vin}")
    print(f"  ✓ VIN Válido")
    print()
    print(f"  🚗 Fabricante:    {vin_info.manufacturer}")
    print(f"  🌍 País:          {vin_info.country}")
    print(f"  📋 Modelo:        {vin_info.model}")
    print(f"  📅 Año:           {vin_info.year}")
    print(f"  ⚙️  Motor:         {vin_info.engine}")
    print(f"  🚙 Carrocería:    {vin_info.body_style}")
    print(f"  🏭 Planta:        {vin_info.plant}")
    print(f"  🔢 Número Serie:  {vin_info.serial_number}")
    print()
    print("=" * 60)


def get_vin_summary(vin: str) -> str:
    """
    Get a brief summary of VIN information.
    
    Args:
        vin: The VIN to summarize.
        
    Returns:
        A brief summary string.
    """
    info = scan_vin(vin)
    if not info.is_valid:
        return f"VIN inválido: {info.error_message}"
    
    return f"Toyota {info.model} {info.year} - {info.country}"
