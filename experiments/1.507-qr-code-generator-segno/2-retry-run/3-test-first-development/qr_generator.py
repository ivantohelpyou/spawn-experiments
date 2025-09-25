"""
QR Code Generator using segno library.
"""
import segno
import segno.consts
from typing import Dict, Any, Optional, Union
import io
import os

# Constants
VALID_ERROR_LEVELS = ['L', 'M', 'Q', 'H']
ERROR_LEVEL_MAPPING = {
    'L': segno.consts.ERROR_LEVEL_L,
    'M': segno.consts.ERROR_LEVEL_M,
    'Q': segno.consts.ERROR_LEVEL_Q,
    'H': segno.consts.ERROR_LEVEL_H
}


def _validate_input(data: str, error_level: Optional[str] = None) -> None:
    """Validate input parameters."""
    if not data or not isinstance(data, str):
        raise ValueError("Data must be a non-empty string")

    if error_level and error_level not in VALID_ERROR_LEVELS:
        raise ValueError(f"Invalid error correction level: {error_level}. Must be one of {VALID_ERROR_LEVELS}")


def _extract_options(options: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and validate options from keyword arguments."""
    return {
        'error_level': options.get('error'),
        'scale': options.get('scale', 1),
        'dark_color': options.get('dark_color'),
        'light_color': options.get('light_color'),
        'border': options.get('border'),
        'output_format': options.get('output_format', 'png'),
        'output_path': options.get('output_path')
    }


def _create_qr_code(data: str, error_level: Optional[str]) -> segno.QRCode:
    """Create QR code with specified error correction level."""
    qr_kwargs = {}
    if error_level:
        qr_kwargs['error'] = ERROR_LEVEL_MAPPING[error_level]
        qr_kwargs['micro'] = False  # Force non-micro mode for consistent behavior

    return segno.make(data, **qr_kwargs)


def _generate_data(qr: segno.QRCode, options: Dict[str, Any]) -> tuple[Any, Optional[str]]:
    """Generate QR code data based on options."""
    output_path = options['output_path']
    output_format = options['output_format']

    if output_path:
        return _save_to_file(qr, output_path, options)
    else:
        return _generate_in_memory(qr, output_format, options)


def _save_to_file(qr: segno.QRCode, output_path: str, options: Dict[str, Any]) -> tuple[Any, str]:
    """Save QR code to file and return data and file path."""
    # Determine format from file extension
    file_format = 'svg' if output_path.lower().endswith('.svg') else 'png'

    save_kwargs = {'kind': file_format}
    _add_save_options(save_kwargs, options, file_format)

    qr.save(output_path, **save_kwargs)

    # Read back the data for the response
    mode = 'rb' if file_format == 'png' else 'r'
    with open(output_path, mode) as f:
        qr_data = f.read()

    return qr_data, output_path


def _generate_in_memory(qr: segno.QRCode, output_format: str, options: Dict[str, Any]) -> tuple[Any, None]:
    """Generate QR code data in memory."""
    if output_format.lower() == 'svg':
        return _generate_svg_data(qr, options), None
    else:
        return _generate_png_data(qr, options), None


def _generate_svg_data(qr: segno.QRCode, options: Dict[str, Any]) -> str:
    """Generate SVG data."""
    dark_color = options.get('dark_color')
    light_color = options.get('light_color')

    if dark_color or light_color:
        buffer = io.BytesIO()
        save_kwargs = {'kind': 'svg'}
        _add_save_options(save_kwargs, options, 'svg')
        qr.save(buffer, **save_kwargs)
        return buffer.getvalue().decode('utf-8')
    else:
        return qr.svg_inline()


def _generate_png_data(qr: segno.QRCode, options: Dict[str, Any]) -> bytes:
    """Generate PNG data."""
    buffer = io.BytesIO()
    save_kwargs = {'kind': 'png'}
    _add_save_options(save_kwargs, options, 'png')
    qr.save(buffer, **save_kwargs)
    return buffer.getvalue()


def _add_save_options(save_kwargs: Dict[str, Any], options: Dict[str, Any], file_format: str) -> None:
    """Add visual customization options to save kwargs."""
    scale = options.get('scale', 1)
    dark_color = options.get('dark_color')
    light_color = options.get('light_color')
    border = options.get('border')

    if scale > 1 and file_format == 'png':
        save_kwargs['scale'] = scale
    if dark_color:
        save_kwargs['dark'] = dark_color
    if light_color:
        save_kwargs['light'] = light_color
    if border is not None:
        save_kwargs['border'] = border


def _build_properties(data: str, qr: segno.QRCode, options: Dict[str, Any]) -> Dict[str, Any]:
    """Build properties dictionary for response."""
    properties = {
        'data': data,
        'version': qr.version,
        'error_correction': str(qr.error),
        'matrix_size': qr._matrix_size
    }

    # Add visual customization properties if they were specified
    scale = options.get('scale', 1)
    if scale > 1:
        properties['scale'] = scale
    if options.get('dark_color'):
        properties['dark_color'] = options['dark_color']
    if options.get('light_color'):
        properties['light_color'] = options['light_color']
    if options.get('border') is not None:
        properties['border'] = options['border']
    if options.get('output_format', 'png') != 'png':
        properties['output_format'] = options['output_format']

    return properties


def generate_qr_code(data: str, **options) -> Dict[str, Any]:
    """
    Generate a QR code from input data using segno library.

    Args:
        data (str): The text/URL to encode in the QR code
        **options: Additional customization options
            - error (str): Error correction level ('L', 'M', 'Q', 'H')
            - scale (int): Scale factor for the QR code
            - dark_color (str): Color for dark modules
            - light_color (str): Color for light modules
            - border (int): Border size in modules
            - output_format (str): Output format ('png' or 'svg')
            - output_path (str): File path to save QR code

    Returns:
        Dict containing:
            - success (bool): Whether QR generation was successful
            - qr_data (bytes|str|None): QR code data as bytes or string
            - file_path (str|None): Path if file was saved
            - properties (dict): QR code properties
    """
    try:
        # Extract and validate options
        opts = _extract_options(options)
        _validate_input(data, opts['error_level'])

        # Create QR code
        qr = _create_qr_code(data, opts['error_level'])

        # Generate QR code data
        qr_data, file_path = _generate_data(qr, opts)

        # Build response properties
        properties = _build_properties(data, qr, opts)

        return {
            'success': True,
            'qr_data': qr_data,
            'file_path': file_path,
            'properties': properties
        }

    except Exception as e:
        return {
            'success': False,
            'qr_data': None,
            'file_path': None,
            'properties': {'error': str(e)}
        }