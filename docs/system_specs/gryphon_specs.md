# Gryphon Spacecraft Specifications

## Overview

The Gryphon is a reusable hypersonic lifting body designed for atmospheric ascent following maglev launch and unpowered glide return.

## Mass Properties

| Property | Value | Notes |
|----------|-------|-------|
| Dry Mass | 15,000 kg | Structure + systems |
| Payload Capacity | 5,000 kg | To 400 km LEO |
| Propellant Mass | 30,000 kg | LOX/RP-1 |
| **Total Launch Mass** | **50,000 kg** | Fully loaded |

## Dimensions

| Property | Value |
|----------|-------|
| Length | 25 m |
| Wingspan (deployed) | 15 m |
| Wingspan (retracted) | 6 m |
| Height | 4 m |

## Aerodynamics

### Wing Configuration
- **Type:** Blended wing body with variable geometry
- **Retracted Mode:** Streamlined for tube transit (40 m² reference area)
- **Deployed Mode:** Full lifting surface (120 m² reference area)
- **Deployment Time:** 3 seconds (pneumatic actuation)

### Aerodynamic Coefficients
| Regime | C_D0 | dC_L/dα | L/D |
|--------|------|---------|-----|
| Hypersonic (M>5) | 0.015 | 0.03/deg | 4.5 |
| Supersonic (M 1.2-5) | 0.020 | 0.05/deg | 5.5 |
| Transonic (M 0.8-1.2) | 0.035 | 0.08/deg | 4.0 |
| Subsonic (M<0.8) | 0.025 | 0.10/deg | 8.0 |

## Propulsion

### Main Engine
- **Type:** Pump-fed bipropellant rocket
- **Propellants:** LOX / RP-1
- **Thrust (vacuum):** 500 kN
- **Thrust (sea level):** 450 kN
- **Isp (vacuum):** 350 s
- **Isp (sea level):** 310 s
- **Throttle Range:** 50% - 100%
- **Restart Capability:** 3 restarts

### Reaction Control System (RCS)
- **Type:** Hypergolic (MMH/NTO)
- **Thrust:** 400 N per thruster
- **Configuration:** 16 thrusters (4 pods × 4)
- **Propellant Mass:** 200 kg

## Thermal Protection System (TPS)

### Nose Cone
- **Material:** C-C composite with active transpiration cooling
- **Max Temperature:** 1,650°C
- **Coolant:** Water (phase change cooling)
- **Flow Rate:** 0.5 kg/s at peak heating

### Leading Edges
- **Material:** Inconel 718
- **Max Temperature:** 980°C
- **Cooling:** Radiative + conductive sink

### Windward Surface
- **Material:** Ti-6Al-4V tiles
- **Max Temperature:** 870°C
- **Insulation:** Aerogel blankets

### Leeward Surface
- **Material:** Aluminum with ceramic coating
- **Max Temperature:** 400°C

## Avionics

### Flight Computer
- **Type:** Triple-redundant fault-tolerant
- **Processor:** Radiation-hardened ARM Cortex-A72
- **Update Rate:** 100 Hz

### Inertial Navigation
- **Type:** Ring laser gyro + accelerometer triad
- **Drift Rate:** < 0.01°/hr
- **GPS Backup:** Yes (below 60 km altitude)

### Communication
- **S-Band:** Telemetry/command (2 Mbps)
- **X-Band:** High-rate data (50 Mbps)
- **TDRSS Compatible:** Yes

## Structural Design

### Primary Structure
- **Material:** Ti-6Al-4V frames + C-C composite skin
- **Design Load:** 6g axial, 3g lateral
- **Safety Factor:** 1.4 ultimate

### Wing Structure
- **Material:** Titanium spars + composite skins
- **Actuation:** Hydraulic (3,000 psi)
- **Design Load:** 4g at Mach 0.8

## Environmental Control

### Payload Bay
- **Volume:** 50 m³
- **Pressure:** Unpressurized (payload provides)
- **Temperature Range:** -20°C to +50°C
- **Vibration Isolation:** Active (10 Hz cutoff)

### Crew Module (Future Option)
- **Capacity:** 4 crew
- **Atmosphere:** 70% N₂ / 30% O₂ at 10 psi
- **CO₂ Removal:** LiOH canisters
- **Duration:** 8 hours

## Operational Envelope

| Parameter | Minimum | Maximum |
|-----------|---------|---------|
| Altitude | 0 km | 400 km |
| Velocity | 0 m/s | 8,000 m/s |
| Dynamic Pressure | 0 kPa | 80 kPa |
| Angle of Attack | -5° | +30° |
| Bank Angle | -60° | +60° |

## Recovery and Reuse

### Landing
- **Mode:** Unpowered glide (like Space Shuttle)
- **Runway Requirement:** 3,000 m minimum
- **Approach Speed:** 250 knots
- **Touchdown Speed:** 180 knots

### Turnaround
- **Target:** 48 hours between flights
- **Inspections:** Automated + spot manual
- **Refurbishment:** TPS tiles (as needed)
