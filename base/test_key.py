from .models import Key
import os


def test_load_key():
    key = Key()
    assert key.key == 0

    key.load_key()
    assert key.key.any()


def test_load_templates():
    key = Key()
    assert key.templates == []

    key.load_templates()
    assert len(key.templates) != 0


def test_verify_key_model():
    key = Key()

    key.load_key()
    key.load_templates()

    match = key.verify_key_model()
    assert match is True


def test_define_contours():
    key = Key()
    assert key.contour == 0

    key.load_key()

    key.define_contour()
    assert key.contour.any()


def test_define_scale():
    key = Key()
    assert key.scale == 0

    key.load_key()

    key.define_scale()
    assert key.scale != 0


def test_g_code():
    if os.path.isfile('./media/gcode.nc'):
        os.remove('./media/gcode.nc')

    key = Key()

    key.load_key()
    key.define_contour()

    key.gcode()
    assert os.path.isfile('./media/gcode.nc') is True

    os.remove('./media/gcode.nc')
    assert os.path.isfile('./media/gcode.nc') is not True