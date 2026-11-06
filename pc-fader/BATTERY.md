# Battery power for the PC fader

Makes the fader fully wireless: a rechargeable LiPo cell, a board that charges it and boosts it to 5 V, and an on/off switch. No code changes; the sketch already runs on Bluetooth.

## Shopping list (all new)

| Qty | Part | Why this one | About |
|---|---|---|---|
| 1 | **Adafruit PowerBoost 1000C** (product 2465) | Charges the battery from micro-USB *while* powering the fader, boosts 3.7 V to a steady 5 V, and has an EN pin for a switch. One board instead of a charger, protection and boost module wired together | $20 |
| 1 | **3.7 V LiPo, 1200 mAh, with protection circuit and JST-PH 2.0 plug** (Adafruit 258), or 2000 mAh (Adafruit 2011) if it fits | The plug goes straight into the PowerBoost; the built-in protection stops over-discharge | $10–13 |
| 1 | Small SPDT slide switch (e.g. Adafruit 805, 2.54 mm pitch) | On/off | $1 |
| — | Hookup wire (22–26 AWG), heat-shrink | You likely have these | — |

Total about $31–34 plus shipping (Adafruit, DigiKey, Mouser or Amazon). Prices are from memory, so check before you buy. Buy the battery and PowerBoost from the same place if you can so the JST plug polarity matches (Adafruit batteries and boards match; random Amazon batteries sometimes have red/black swapped).

Cheaper option, about $5 but more wiring: a TP4056 charger board **with protection** (it has a DW01 chip and 6 pads) plus an MT3608 boost module set to 5.0 V with a multimeter before connecting. It doesn't power the load properly while charging, so switch off to charge.

## Wiring

```
LiPo ──JST──> PowerBoost BAT
              PowerBoost 5V  ───> ESP32 devkit 5V pin
              PowerBoost GND ───> ESP32 devkit GND pin
              PowerBoost EN  ───> switch middle pin
              PowerBoost GND ───> switch outer pin     (switch closed = OFF)
```

- Solder to the PowerBoost's **5V** and **GND** pads (the 5V output, next to the USB-A footprint), not to **BAT**.
- The EN pin pulled to GND turns the boost off. Put the switch so that "off" connects EN to GND.
- Charge by plugging a phone charger into the PowerBoost's micro-USB. Its orange LED means charging, green means full. The fader keeps working while it charges.

## Before flashing over USB

Switch the battery **off** before plugging a cable into the ESP32 devkit itself. Otherwise the PC's USB 5 V and the PowerBoost's 5 V are tied together and fight. Normal use doesn't need the devkit's USB at all.

## Runtime

The ESP32-S3 with Bluetooth on draws roughly 60–100 mA at 5 V. With the boost about 85 % efficient:

| Battery | Runtime |
|---|---|
| 1200 mAh | about 8–12 hours |
| 2000 mAh | about 14–20 hours |

Estimated, not measured. The PowerBoost's red LBO LED comes on when the battery is nearly empty.

## Not done (later, if wanted)

- Battery % on the PC: a 2-resistor divider from BAT to a free ADC pin, and the sketch sends it to the helper.
- Sleep when idle to stretch runtime.
