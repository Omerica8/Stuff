# Drone motors in the synth

Omer salvaged 4 small coreless brushed motors (about 7 mm, 2 wires) from a toy quadcopter. Plan: use them as **4 mechanical percussion voices** ("robot drums") played by MIDI notes, with haptic buzz as a side effect. Optional extra, not needed for the synth itself.

## Ideas, best first

| Idea | How | Effort |
|---|---|---|
| **Robot drums** (recommended) | Each motor gets a small plastic flag (zip-tie end, guitar-pick shard) glued on the shaft. A short pulse spins it into something that rings: a tin lid, a bottle cap, a wood block, a rubber band. MIDI notes 36-39 on channel 10 fire motors 1-4, velocity sets the pulse strength | Low |
| Haptic beat / LFO | A blob of hot glue off-center on the shaft makes it a vibration motor. Mount it inside the case and pulse it with the LFO or on every note | Low |
| Hand-spin control | Spin a motor by hand and it makes a small voltage (it's a generator). Read it on an ADC pin as a "flick wheel" for LFO speed or pitch bend. Needs a diode bridge or op-amp because the voltage is tiny and changes sign | Medium, later |

They spin far too fast to make a tone on their own, and the synth's sound engine already does that better.

## Driver (one per motor)

These motors are rated around 3.7 V and can pull 0.5-1 A each when they start. An ESP32 pin gives about 20 mA, so each motor needs a transistor switch.

```
5V ─────────────┬──────── motor (+)
                │         motor (-) ──┬── AO3400 drain
       1N5819 cathode                 │   AO3400 source ── GND
       1N5819 anode ──────────────────┘
GPIO ── 100 Ω ── AO3400 gate ── 100 kΩ ── GND
```

The diode sits across the motor, striped end (cathode) to 5V.

| Part, per motor | Why |
|---|---|
| **AO3400** N-MOSFET (SOT-23; use a SOT-23-to-DIP adapter on perfboard) | Turns fully on at 3.3 V gate, handles 5 A. A 2N7000 is too weak; for breadboard, an IRLZ44N (TO-220) also works |
| 1N5819 Schottky diode across the motor | Catches the voltage spike when the motor switches off, which would otherwise kill the MOSFET |
| 100 Ω gate resistor, 100 kΩ gate to GND | Limits pin current; keeps the motor off while the ESP32 boots |
| One 470 µF capacitor across 5V/GND near the motors | Stops motor start-up current from dipping the ESP32's supply and resetting it |

About $2-3 for all four.

## Pins (provisional)

GPIO38, 39, 40, 41 for motors 1-4. They don't need an ADC (ADC1 pins GPIO1-10 stay for the faders) and avoid GPIO19/20 (USB) and GPIO35-37 (N16R8 PSRAM). Not locked until the board labels are confirmed.

## Firmware plan

LEDC PWM at 20 kHz (above hearing, so no whine) on each motor pin. Duty is capped at about 70% because 5 V is above the motors' 3.7 V rating. A drum hit is one pulse of 20-60 ms, longer and stronger with higher velocity. It runs on core 1 with the MIDI code, so the audio on core 0 is untouched.

## Watch out for

- **USB power limit.** A PC USB port gives about 500 mA. Four motors starting at once can pull more than that and reset the board. Keep the pulses short, stagger hits by a few ms, or power the motors from a separate 5 V supply (shared GND).
- **Noise in the audio.** Brushed motors spark electrically. Run the motor GND wires straight back to the power input, not through the DAC's GND, and keep motor wires away from the line-out jack. A 0.1 µF ceramic soldered across each motor's two pins helps a lot.
- Glue the flags on well, and test with the case open: a flag at 30,000 rpm that comes loose goes far.
