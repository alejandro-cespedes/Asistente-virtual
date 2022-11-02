# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe

setup(
    name="Asistente de voz",
    version="1.0",
    description="Este asistente se llama Helena",
    author="Alejandro Cespedes",
    author_email="alejandroc3001@gmail.com",
    url="url del proyecto",
    license="tipo de licencia",
    scripts=["asistente_virtual.py"],
    console=["asistente_virtual.py"],
    options={"py2exe": {"bundle_files": 1}},
    zipfile=None,
)
