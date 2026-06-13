"""Mock register data for device-1 — 3-phase grid-tied solar inverter.

Holding registers 1400–1431 (32 total).
All multi-decimal values use ×10 scaling unless noted otherwise.
32-bit energy counters are stored as a single high-word register (low word not modelled).
Each base value has ±10% variance to simulate realistic fluctuation.
"""
from __future__ import annotations

UNIT_ID = 1
HOST = "0.0.0.0"
PORT = 5020
HOLDING_REGISTERS: dict[int, dict[str, int]] = {
    1400: {"base": 105,  "min": 105,  "max": 105},#
    1401: {"base": 125,  "min": 125,  "max": 125},
    1402: {"base": 145,  "min": 145,  "max": 145},
    1403: {"base": 165,  "min": 165,  "max": 165},
    1404: {"base": 1,  "min": 2,  "max": 4},
    1405: {"base": 205,  "min": 0,  "max": 205},
    1406: {"base": 225,  "min": 220,  "max": 230},
    1407: {"base": 245,  "min": 240,  "max": 250},
    1408: {"base": 265,  "min": 260,  "max": 270},
    1409: {"base": 285,  "min": 280,  "max": 290},
    1410: {"base": 305,  "min": 300,  "max": 310},
    1411: {"base": 325,  "min": 320,  "max": 330},
    1412: {"base": 345,  "min": 340,  "max": 350},
    1413: {"base": 365,  "min": 360,  "max": 370},
    1414: {"base": 385,  "min": 380,  "max": 390},
    1415: {"base": 405,  "min": 400,  "max": 410},
    1416: {"base": 425,  "min": 420,  "max": 430},
    1417: {"base": 445,  "min": 440,  "max": 450},
    1418: {"base": 465,  "min": 460,  "max": 470},
    1419: {"base": 485,  "min": 480,  "max": 490},
    1420: {"base": 505,  "min": 500,  "max": 510},
    1421: {"base": 525,  "min": 520,  "max": 530},
    1422: {"base": 545,  "min": 540,  "max": 550},
    1423: {"base": 565,  "min": 560,  "max": 570},
    1424: {"base": 585,  "min": 580,  "max": 590},
    1425: {"base": 605,  "min": 600,  "max": 610},
    1426: {"base": 625,  "min": 620,  "max": 630},
    1427: {"base": 645,  "min": 640,  "max": 650},
    1428: {"base": 665,  "min": 660,  "max": 670},
    1429: {"base": 685,  "min": 680,  "max": 690},
    1430: {"base": 705,  "min": 700,  "max": 710},
    1431: {"base": 725,  "min": 720,  "max": 730},
}