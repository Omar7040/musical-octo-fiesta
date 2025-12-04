"""Camera-based VIN Scanner module for Toyota Car Service Application.

Módulo de escaneo de VIN con cámara para la aplicación de servicio de autos Toyota.
Este módulo permite escanear códigos de barras VIN usando la cámara del dispositivo.

Requires:
    - opencv-python: Para captura y procesamiento de imagen
    - pyzbar: Para decodificación de códigos de barras
"""

import sys
from typing import Optional, Callable
from dataclasses import dataclass

# Check for optional dependencies
CAMERA_AVAILABLE = False
try:
    import cv2
    from pyzbar import pyzbar
    CAMERA_AVAILABLE = True
except ImportError:
    cv2 = None
    pyzbar = None


@dataclass
class CameraScanResult:
    """Result from a camera VIN scan."""
    success: bool
    vin: str
    error_message: str = ""
    scan_type: str = ""  # "barcode", "qr", "manual"


def check_camera_dependencies() -> tuple:
    """
    Check if camera scanning dependencies are installed.
    
    Returns:
        Tuple of (available: bool, message: str)
    """
    if not CAMERA_AVAILABLE:
        return False, (
            "Las dependencias de cámara no están instaladas.\n"
            "Instala con: pip install opencv-python pyzbar\n"
            "En Linux también necesitas: sudo apt-get install libzbar0"
        )
    return True, "Dependencias de cámara disponibles"


def scan_vin_from_camera(
    timeout_seconds: int = 30,
    on_frame_callback: Optional[Callable] = None,
    camera_index: int = 0
) -> CameraScanResult:
    """
    Scan a VIN barcode using the device camera.
    
    Escanea un código de barras VIN usando la cámara del dispositivo.
    
    Args:
        timeout_seconds: Maximum time to wait for a scan (default 30s)
        on_frame_callback: Optional callback function called on each frame
        camera_index: Camera device index (default 0 for primary camera)
        
    Returns:
        CameraScanResult with the scanned VIN or error message.
    """
    available, message = check_camera_dependencies()
    if not available:
        return CameraScanResult(
            success=False,
            vin="",
            error_message=message
        )
    
    try:
        # Open camera
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            return CameraScanResult(
                success=False,
                vin="",
                error_message="No se pudo abrir la cámara. Verifica que esté conectada."
            )
        
        print("\n" + "=" * 60)
        print("       ESCÁNER DE VIN CON CÁMARA")
        print("=" * 60)
        print("\n  📷 Cámara activa - Apunta al código de barras del VIN")
        print("  ⏱️  Tiempo límite:", timeout_seconds, "segundos")
        print("  ❌ Presiona 'q' para cancelar")
        print()
        
        import time
        start_time = time.time()
        scanned_vin = None
        
        while True:
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > timeout_seconds:
                cap.release()
                cv2.destroyAllWindows()
                return CameraScanResult(
                    success=False,
                    vin="",
                    error_message=f"Tiempo agotado después de {timeout_seconds} segundos"
                )
            
            # Read frame from camera
            ret, frame = cap.read()
            if not ret:
                continue
            
            # Decode barcodes in the frame
            barcodes = pyzbar.decode(frame)
            
            for barcode in barcodes:
                # Extract barcode data
                barcode_data = barcode.data.decode('utf-8').strip()
                barcode_type = barcode.type
                
                # Check if it looks like a VIN (17 characters, alphanumeric)
                if len(barcode_data) == 17 and barcode_data.isalnum():
                    # Check for invalid VIN characters
                    if not any(c in barcode_data.upper() for c in 'IOQ'):
                        scanned_vin = barcode_data.upper()
                        
                        # Draw rectangle around barcode
                        points = barcode.polygon
                        if len(points) == 4:
                            pts = [(p.x, p.y) for p in points]
                            for i in range(4):
                                cv2.line(frame, pts[i], pts[(i+1) % 4], (0, 255, 0), 3)
                        
                        # Display success message on frame
                        cv2.putText(frame, f"VIN: {scanned_vin}", (10, 30),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.putText(frame, "VIN DETECTADO!", (10, 60),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Draw scanning guide
            height, width = frame.shape[:2]
            cv2.rectangle(frame, (50, height//3), (width-50, 2*height//3), (255, 255, 0), 2)
            cv2.putText(frame, "Coloca el codigo de barras aqui", (60, height//3 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            # Show remaining time
            remaining = int(timeout_seconds - elapsed)
            cv2.putText(frame, f"Tiempo: {remaining}s", (width - 120, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            # Callback if provided
            if on_frame_callback:
                on_frame_callback(frame)
            
            # Display the frame
            cv2.imshow('Toyota VIN Scanner - Presiona Q para salir', frame)
            
            # Check for VIN found or user quit
            if scanned_vin:
                # Wait a moment to show the result
                cv2.waitKey(1000)
                break
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                cap.release()
                cv2.destroyAllWindows()
                return CameraScanResult(
                    success=False,
                    vin="",
                    error_message="Escaneo cancelado por el usuario"
                )
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        
        if scanned_vin:
            print(f"\n  ✅ VIN escaneado exitosamente: {scanned_vin}")
            return CameraScanResult(
                success=True,
                vin=scanned_vin,
                scan_type="barcode"
            )
        
        return CameraScanResult(
            success=False,
            vin="",
            error_message="No se detectó ningún VIN válido"
        )
        
    except Exception as e:
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()
        return CameraScanResult(
            success=False,
            vin="",
            error_message=f"Error durante el escaneo: {str(e)}"
        )


def scan_vin_from_image(image_path: str) -> CameraScanResult:
    """
    Scan a VIN barcode from an image file.
    
    Escanea un código de barras VIN desde un archivo de imagen.
    
    Args:
        image_path: Path to the image file containing the VIN barcode.
        
    Returns:
        CameraScanResult with the scanned VIN or error message.
    """
    available, message = check_camera_dependencies()
    if not available:
        return CameraScanResult(
            success=False,
            vin="",
            error_message=message
        )
    
    try:
        # Read image
        image = cv2.imread(image_path)
        
        if image is None:
            return CameraScanResult(
                success=False,
                vin="",
                error_message=f"No se pudo leer la imagen: {image_path}"
            )
        
        # Decode barcodes
        barcodes = pyzbar.decode(image)
        
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8').strip()
            
            # Check if it's a valid VIN
            if len(barcode_data) == 17 and barcode_data.isalnum():
                if not any(c in barcode_data.upper() for c in 'IOQ'):
                    return CameraScanResult(
                        success=True,
                        vin=barcode_data.upper(),
                        scan_type="image"
                    )
        
        return CameraScanResult(
            success=False,
            vin="",
            error_message="No se encontró un VIN válido en la imagen"
        )
        
    except Exception as e:
        return CameraScanResult(
            success=False,
            vin="",
            error_message=f"Error al procesar la imagen: {str(e)}"
        )


def print_camera_scan_instructions():
    """Print instructions for camera VIN scanning."""
    print("\n" + "=" * 60)
    print("    INSTRUCCIONES PARA ESCANEO DE VIN CON CÁMARA")
    print("=" * 60)
    print()
    print("  📍 UBICACIÓN DEL VIN EN EL VEHÍCULO:")
    print("     • Esquina inferior del parabrisas (lado del conductor)")
    print("     • Etiqueta en el marco de la puerta del conductor")
    print("     • Documentos del vehículo (tarjeta de circulación)")
    print()
    print("  📷 CONSEJOS PARA UN BUEN ESCANEO:")
    print("     • Asegúrate de tener buena iluminación")
    print("     • Mantén la cámara estable")
    print("     • Acerca la cámara al código de barras")
    print("     • Evita reflejos y sombras")
    print()
    print("  🔧 DEPENDENCIAS REQUERIDAS:")
    print("     pip install opencv-python pyzbar")
    print("     Linux: sudo apt-get install libzbar0")
    print()
    print("=" * 60)


def interactive_camera_scan():
    """
    Run an interactive camera VIN scan session.
    
    Ejecuta una sesión interactiva de escaneo de VIN con cámara.
    """
    from toyota_service.services.vin_scanner import scan_vin, print_vin_info
    
    print_camera_scan_instructions()
    
    available, message = check_camera_dependencies()
    if not available:
        print(f"\n  ⚠️  {message}")
        print("\n  Usa scan_vin('TU_VIN') para ingresar el VIN manualmente.")
        return None
    
    print("\n  Iniciando cámara...")
    result = scan_vin_from_camera()
    
    if result.success:
        print("\n  Decodificando información del VIN...")
        vin_info = scan_vin(result.vin)
        print_vin_info(vin_info)
        return vin_info
    else:
        print(f"\n  ❌ {result.error_message}")
        return None
